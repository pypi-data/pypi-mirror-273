# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Defines Collector class and corresponding helper methods.

Collector serves an important roles of building Google Ads queries from set of
diverse elements: metrics, dimensions, filters, resource names, etc.

Collector can be:
  * similar (sharing the same metrics, dimensions and filters) which allows
    to perform similar target deduplication with the lowest common level.
  * equal (sharing the same attributes) - useful for checking target presence
    in the sets.

Metrics, dimensions and filters of a Collector can be dynamically changed thus
allowing Collector customization at the runtime.
"""
from __future__ import annotations

import dataclasses
import enum
from collections.abc import Mapping
from collections.abc import MutableSequence
from collections.abc import Sequence
from datetime import datetime

from gaarf.cli import utils as gaarf_utils

from gaarf_exporter import query_elements
from gaarf_exporter import util

_DEFAULT_METRICS = [
    query_elements.Field('clicks'),
    query_elements.Field('impressions'),
    query_elements.Field('conversions'),
    query_elements.Field('cost_micros / 1e6', 'cost')
]

_DEFAULT_CONVERSION_SPLIT_METRICS = [
    query_elements.Field('all_conversions'),
    query_elements.Field('all_conversions_value'),
]

_DEFAULT_CONVERSION_SPLIT_DIMENSIONS = [
    query_elements.Field('segments.conversion_action_category',
                         'conversion_category'),
    query_elements.Field('segments.conversion_action_name', 'conversion_name'),
    query_elements.Field(
        'segments.conversion_action', 'conversion_id',
        query_elements.Customizer(query_elements.CustomizerTypeEnum.INDEX, '0'))
]

_DEFAULT_CONVERSION_SPLIT_FILTERS = [
    'metrics.all_conversions > 0',
    'segments.date DURING TODAY',
]


class CollectorLevel(enum.IntEnum):
  """Represents minimal level of entity.

  CollectorLevel regulates which entity id (ad_id, ad_group_id, campaign_id, etc.)
  is associated with metrics and dimensions for a given target.
  Collector levels are ordered hierarchically to support comparison operations.
  """
  UNKNOWN = 0
  AD_GROUP_AD_ASSET = 1
  AD_GROUP_AD = 2
  AD_GROUP = 3
  CAMPAIGN = 4
  CUSTOMER = 5
  MCC = 6

  @classmethod
  def contains(cls, *keys: str) -> bool:
    """Checks whether supplied keys are valid enum names."""
    return all(key.upper() in cls.__members__ for key in keys)


@dataclasses.dataclass
class LevelInfo:
  """Stores meta information for a particular CollectorLevel.

  This meta information is used to correctly build query in the Collector.

  Attributes:
    resource_name: Name of Google Ads reporting resource.
    id: Field name for entity id (i.e. ad_group.id, campaign.id) .
    id_alias: Alias for entity_id (i.e ad_group_id, campaign_id).
    name: Field name for entity content (i.e ad_group.name, campaign.name).
    name_alias: Alias for entity content (i.e ad_group_name, campaign_name).
    active_entities_filter: Filter to get only active entities.
  """
  resource_name: str
  id: str
  id_alias: str
  name: str
  name_alias: str
  active_entities_filter: str

  def to_query_field(self) -> str:
    """Returns field name with alias."""
    return f'{self.id} AS {self.id_alias}'

  def to_field(self) -> query_elements.Field:
    """Builds Field from level meta information."""
    return query_elements.Field(name=self.id, alias=self.id_alias)


LEVELS = {
    CollectorLevel.AD_GROUP_AD_ASSET:
        LevelInfo('ad_group_ad_asset_view', 'asset.id', 'asset_id',
                  'asset.name', 'asset',
                  'ad_group_ad_asset_view.enabled = TRUE'),
    CollectorLevel.AD_GROUP_AD:
        LevelInfo('ad_group_ad', 'ad_group_ad.ad.id', 'ad_id',
                  'ad_group_ad.ad.name', 'ad_name',
                  'ad_group_ad.status = ENABLED'),
    CollectorLevel.AD_GROUP:
        LevelInfo('ad_group', 'ad_group.id', 'ad_group_id', 'ad_group.name',
                  'ad_group_name', 'ad_group.status = ENABLED'),
    CollectorLevel.CAMPAIGN:
        LevelInfo('campaign', 'campaign.id', 'campaign_id', 'campaign.name',
                  'campaign_name', 'campaign.status = ENABLED'),
    CollectorLevel.CUSTOMER:
        LevelInfo('customer', 'customer.id', 'customer_id',
                  'customer.descriptive_name', 'account_name',
                  'customer.status = ENABLED'),
    CollectorLevel.MCC:
        LevelInfo('customer', 'customer.id', 'customer_id',
                  'customer.descriptive_name', 'account_name',
                  'customer.status = ENABLED'),
}


class Collector:
  """Represents collection of query elements needed to build a Google Ads query.

  Attributes:
    name: Unique identifier of a target.
    level: Minimal entity level in the target (ad_group, campaign, customer).
    metrics: All metrics (started with `metrics.`) associated with the target.
    dimensions: All segments and resources associated with the target.
    filters: Text conditions for limiting the query.
    resource_name: Name of resource to get data from (used in FROM statement).
    query: Full text of the query to be sent to Google Ads API.
    suffix: Optional custom identifier to the target.
  """

  def __init__(self,
               name: str | None = None,
               metrics: str | Sequence[query_elements.Field] | None = None,
               level: CollectorLevel | None = CollectorLevel.AD_GROUP,
               resource_name: str | None = None,
               dimensions: str | Sequence[query_elements.Field] | None = None,
               filters: str | Sequence[str] | None = None,
               suffix: str | None = None,
               query: str | None = None) -> None:
    """Initializes Collector.

    Args:
      name: Unique identifier of a target.
      metrics: All metrics (started with `metrics.`) associated with the target.
      level: Minimal entity level in the target (ad_group, campaign, customer).
      resource_name: Name of resource to get data from (used in FROM statement).
      dimensions: All segments and resources associated with the target.
      filters: Text conditions for limiting the query.
      suffix: Optional custom identifier to the target.
      query: Full query_text.
    """
    self.name = name
    self._level = level
    self._resource_name = resource_name
    self._filters = filters or set()
    self._metrics = self._init_fields(metrics, 'metrics')
    self._dimensions = self._init_fields(dimensions)
    self.suffix = suffix if suffix else name
    self._query = query

  @classmethod
  def from_definition(cls, definition: dict) -> Collector:
    query_spec = definition.get('query_spec', {})
    # query = definition.get('query')
    if level_string := query_spec.get('level'):
      level = CollectorLevel[level_string.upper()]
    else:
      level = CollectorLevel.AD_GROUP
    return cls(
        name=definition.get('name'),
        suffix=definition.get('suffix'),
        metrics=query_spec.get('metrics'),
        dimensions=query_spec.get('dimensions'),
        filters=query_spec.get('filters'),
        resource_name=query_spec.get('resource_name'),
        level=level)

  def create_conv_collector(self) -> Collector:
    return Collector(
        name=f'{self.name}_conversion_split',
        suffix=self.suffix,
        level=self.level,
        metrics=_DEFAULT_CONVERSION_SPLIT_METRICS,
        dimensions=_DEFAULT_CONVERSION_SPLIT_DIMENSIONS,
        resource_name=self.resource_name,
        filters=_DEFAULT_CONVERSION_SPLIT_FILTERS)

  @property
  def level(self) -> CollectorLevel | None:
    """Represents entity level of a target."""
    return self._level

  @level.setter
  def level(self, value: CollectorLevel) -> None:
    """Changes saved level of a target."""
    self._level = value

  @property
  def metrics(self) -> set[query_elements.Field]:
    """Returns unique metrics."""
    return set(self._metrics)

  @metrics.setter
  def metrics(self, values: Sequence[query_elements.Field]) -> None:
    """Changes saved metrics of a target."""
    self._metrics = set(values)

  @property
  def dimensions(self) -> set[query_elements.Field]:
    """Returns unique metrics."""
    return set(self._dimensions)

  @dimensions.setter
  def dimensions(self, values: Sequence[query_elements.Field]) -> None:
    """Changes saved dimensions of a target."""
    self._dimensions = values

  @property
  def filters(self) -> set[str]:
    """Returns filters or default placeholder."""
    if isinstance(self._filters, str):
      self._filters = set(self._filters.split(' AND '))
    else:
      self._filters = set(self._filters)
    if isinstance(self, ServiceCollector):
      return self._filters
    # TODO (amarkin): Adding default filter hurts customization by dates. And wierd.
    if not self._filters:
      self._filters.add('segments.date DURING TODAY')
    elif not any('segments.date' in _filter for _filter in self._filters):
      self._filters.add('segments.date DURING TODAY')
    return self._filters

  @filters.setter
  def filters(self, values: str) -> None:
    """Changes saved dimensions of a target."""
    self._filters = values

  def _init_fields(self,
                   fields: str | list[query_elements.Field],
                   prefix: str = '') -> list[query_elements.Field]:
    """Transforms fields to proper Field format based on optional prefix.

    Args:
      fields: Query fields that needs to be initialized.
      prefix: Optional prefix that needs to be added before each field.

    Returns:
      Formatted list of Fields.

    Raises:
      ValueError: If fields has non-aliased virtual column.
    """
    if not fields:
      return []

    if isinstance(fields, str):
      field_list = [
          query_elements.Field(name=field) for field in fields.split(',')
      ]
    elif isinstance(fields, MutableSequence):
      field_list = []
      for field in fields:
        if isinstance(field, query_elements.Field):
          element = field
        elif isinstance(field, Mapping):
          for alias, values in field.items():
            element = query_elements.Field(
                name=values.get('field'), alias=alias)
        else:
          element = query_elements.Field(name=field)
        field_list.append(element)
    else:
      field_list = fields

    if not prefix:
      return field_list

    for field in field_list:
      raw_tokens = util.tokenize(field.name)
      if not field.alias:
        if len(raw_tokens) > 1:
          raise ValueError('virtual column need an alias.')
        field.alias = field.name

      processed_tokens = []
      for value, token_type in raw_tokens:
        identifier = value
        if token_type == 'IDENTIFIER':
          identifier = f'{prefix}.{value}'
        processed_tokens.append(identifier)

      field.name = ' '.join(processed_tokens)

    return field_list

  @property
  def level_info(self) -> LevelInfo | None:
    """Returns meta information related to a target level."""
    return LEVELS.get(self.level)

  @property
  def _formatted_level(self) -> str:
    """Returns formatted level as field name with alias."""
    if level_info := self.level_info:
      return f'{level_info.to_query_field()},\n'
    return ''

  @property
  def _formatted_metrics(self) -> str:
    """Returns formatted metrics as field names with aliases."""
    if not self.metrics:
      return '\n'
    metrics_info = ',\n'.join(
        [field.to_query_field() for field in sorted(self.metrics)])
    return f'{metrics_info},\n'

  @property
  def _formatted_dimensions(self) -> str:
    """Returns formatted metrics as field names with aliases."""
    if not (dimensions := self.dimensions):
      return '\n'
    if level_info := self.level_info:
      dimensions = set(dimensions).difference(set([level_info.to_field()]))
    if not dimensions:
      return '\n'
    dimensions_info = ',\n'.join(
        [field.to_query_field() for field in sorted(dimensions)])
    return f'{dimensions_info},\n'

  @property
  def _formatted_filters(self) -> str:
    return ' AND '.join(self.filters)

  @property
  def resource_name(self) -> str:
    """Gets resource_name or infers it from target level."""
    if self._resource_name:
      return self._resource_name
    if level_info := self.level_info:
      return level_info.resource_name.lower()
    return self.level.name

  @property
  def query(self) -> str:
    """Formats query based on elements."""
    if self._query:
      return self._query
    return (f'SELECT {self._formatted_level}{self._formatted_metrics}'
            f'{self._formatted_dimensions}'
            f'FROM {self.resource_name}\n'
            f'WHERE {self._formatted_filters}')

  def customize(self, kwargs: dict[str, str]) -> None:
    if level := kwargs.get('level'):
      self.level = CollectorLevel[level.upper()]
    if (start_date := kwargs.get('start_date')) and (end_date :=
                                                     kwargs.get('end_date')):
      start_date = gaarf_utils.convert_date(start_date)
      end_date = gaarf_utils.convert_date(end_date)
      if not self.filters or 'segments.date DURING TODAY' in self.filters:
        self.filters.remove('segments.date DURING TODAY')
        self.filters.add(f"segments.date BETWEEN '{start_date}' AND '{end_date}'")
      n_days = (datetime.strptime(end_date, '%Y-%m-%d') -
                datetime.strptime(start_date, '%Y-%m-%d')).days + 1
      self.dimensions.add(query_elements.Field(str(n_days), 'n_days'))

  def is_similar(self, other: Collector) -> bool:
    """Compares similarity between two collectors.

    Similarity first checks whether two collectors are coming from different
    non CollectorLevel specific resource_names, if they are different then
    collectors are not similar.
    Then is compares all  metrics, dimensions and filters between two collectors.

    Returns:
      Whether two collectors are similar.
    """
    if not other or not isinstance(other, Collector):
      return False

    if (self.resource_name != other.resource_name and
        not (CollectorLevel.contains(self.resource_name, other.resource_name))):
      return False
    if (self.metrics, self.dimensions,
        self.filters) == (other.metrics, other.dimensions, other.filters):
      return True
    return False

  def generate_service_collector(self) -> ServiceCollector | None:
    """Generates correct ServiceCollector based on provided level.

     Based on level (AD_GROUP, CAMPAIGN, ACCOUNT, etc.) corresponding
     ServiceCollector is created that contains all necessary mapping information
     downstream. I.e. if 'level=AD_GROUP' then information on ad_group, campaign
     and customer will be included in to the mapping.

     Returns:
      ServiceCollector called 'mapping' for an appropriate level.

    """
    if isinstance(self, ServiceCollector):
      return None
    if self.level == CollectorLevel.MCC:
      level = CollectorLevel.CUSTOMER
    else:
      level = self.level
    dimensions = []
    filters = ''

    for target_level in CollectorLevel:
      if (target_level
          not in (CollectorLevel.MCC, CollectorLevel.AD_GROUP_AD_ASSET) and
          self.level <= target_level and
          (level_info := LEVELS.get(target_level))):
        dimensions.extend([
            query_elements.Field(name=level_info.id, alias=level_info.id_alias),
            query_elements.Field(
                name=level_info.name, alias=level_info.name_alias),
        ])
        if filters:
          filters = filters + ' AND ' + level_info.active_entities_filter
        else:
          filters = level_info.active_entities_filter

    return ServiceCollector(
        name='mapping', dimensions=dimensions, level=level, filters=filters)

  def __eq__(self, other: Collector) -> bool:
    """Compares two targets based on similarity, resource_name and level."""
    if not self.is_similar(other):
      return False
    if self.level != other.level:
      return False
    return True

  def __lt__(self, other: Collector) -> bool:
    """Compares targets by level values."""
    if self.level.value < other.level.value:
      return True
    return False

  def __gt__(self, other: Collector) -> bool:
    """Compares targets by level values."""
    if self.level.value > other.level.value:
      return True
    return False

  def __hash__(self):
    return hash(self.query)

  def __repr__(self) -> str:
    return f'Collector(name="{self.name}")'


class ServiceCollector(Collector):
  """Helper class for targets without metrics."""

  @property
  def metrics(self) -> set[query_elements.Field]:
    """Returns default info metric."""
    return {
        query_elements.Field(name='1', alias='info'),
    }

  @metrics.setter
  def metrics(self, value: query_elements.Field) -> None:
    """Ensures that metrics cannot be overwritten."""
    raise ValueError('Cannot change value of "metrics"!')


def create_default_service_collector(
    level: CollectorLevel) -> ServiceCollector | None:
  """Generates correct ServiceCollector based on provided level.

   Based on level (AD_GROUP, CAMPAIGN, ACCOUNT, etc.) corresponding
   ServiceCollector is created that contains all necessary mapping information
   downstream. I.e. if 'level=AD_GROUP' then information on ad_group, campaign
   and customer will be included in to the mapping.

   Returns:
    ServiceCollector called 'mapping' for an appropriate level.

  """
  if level == CollectorLevel.MCC:
    level = CollectorLevel.CUSTOMER
  dimensions = set()
  filters = set()

  for target_level in CollectorLevel:
    if (target_level
        not in (CollectorLevel.MCC, CollectorLevel.AD_GROUP_AD_ASSET) and
        level <= target_level and (level_info := LEVELS.get(target_level))):
      dimensions.update([
          query_elements.Field(name=level_info.id, alias=level_info.id_alias),
          query_elements.Field(
              name=level_info.name, alias=level_info.name_alias)
      ])
      filters.add(level_info.active_entities_filter)

  return ServiceCollector(
      name='mapping', dimensions=dimensions, level=level, filters=filters)
