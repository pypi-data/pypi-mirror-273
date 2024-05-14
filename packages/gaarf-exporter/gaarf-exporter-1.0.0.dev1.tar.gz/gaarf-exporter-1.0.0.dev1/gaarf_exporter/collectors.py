# Copyright 2023 Google LLC
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
"""Module for defining collectors.

Collectors are converted to gaarf queries that are sent to Ads API.
"""
from __future__ import annotations

import glob
import itertools
import pathlib
from collections import defaultdict
from collections.abc import MutableSet

import yaml

from gaarf_exporter import target as query_target

_SCRIPT_DIR = pathlib.Path(__file__).parent


class Registry:
  """Maps collector names to corresponding classes.

  Registry simplifies searching for collectors as well as adding new ones.

  Attributes:
    collectors: Mapping between collector names and corresponding class.
  """

  def __init__(self, collectors: dict | None = None) -> None:
    """Creates Registry based on module level variable _REGISTRY."""
    self.collectors = dict(collectors) or dict()

  @classmethod
  def from_collector_definitions(
      cls,
      path_to_definitions: str = f'{_SCRIPT_DIR}/collector_definitions/*.yaml'
  ) -> Registry:
    collectors = define_collectors(path_to_definitions)
    return cls(collectors)

  @property
  def default_collectors(self) -> CollectorSet:
    """Helper for getting only default collectors from the registry."""
    return CollectorSet(collectors=set(self.collectors.get('default').values()))

  @property
  def all_subregistries(self) -> CollectorSet:
    """Helper for getting only sub-registries. """
    collector_names = set()
    for name, collector in self.collectors.items():
      if isinstance(collector, dict):
        collector_names.add(name)
    subregistries_collector_names = ','.join(collector_names)
    return self.find_collectors(collector_names=subregistries_collector_names)

  @property
  def all_collectors(self) -> CollectorSet:
    """Helper for getting all collectors from the registry."""
    all_collector_names = ','.join(self.collectors.keys())
    return self.find_collectors(collector_names=all_collector_names)

  def find_collectors(self, collector_names: str | None = None) -> CollectorSet:
    """Extracts collectors from registry and returns their initialized collectors.

    Args:
      collector_names:
        Names of collectors that need to be fetched from registry.

    Returns:
      Found collectors.
    """
    if not collector_names:
      return CollectorSet()
    if collector_names == 'all':
      return self.all_collectors
    collectors_subset = [
        collector for name, collector in self.collectors.items()
        if name in collector_names.strip().split(',')
    ]
    found_collectors = set()
    for collector in collectors_subset:
      if isinstance(collector, dict):
        for collector_ in collector.values():
          found_collectors.add(collector_)
      else:
        found_collectors.add(collector)
    return CollectorSet(collectors=set(found_collectors))

  def add_collectors(self, collectors: query_target.Collector) -> None:
    """Ads collectors to the registry.

    Args:
      collectors: Collectors classes to be added to registry.
    """
    for collector in collectors:
      self.collectors[collector.name] = collector


class CollectorSet(MutableSet):
  """Represent a set of collectors returned from Registry."""

  def __init__(self,
               collectors: set[query_target.Collector] | None = None,
               service_collectors: bool = True) -> None:
    """Initializes CollectorSet based on provided collectors."""
    self._collectors = collectors or set()
    self._service_collectors = service_collectors

  @property
  def collectors(self) -> set[query_target.Collector]:
    """Return customized or original collectors of the CollectorSet."""
    if self._service_collectors:
      _service_collectors = set()
      for collector in self._collectors:
        if service_collector := collector.generate_service_collector():
          _service_collectors.add(service_collector)
      self._collectors = self._collectors.union(_service_collectors)
    self.deduplicate_collectors()
    return self._collectors

  def deduplicate_collectors(self) -> None:
    """Dedupicates collectors in the set.

    If there are similar collectors in the list return only those with
    the lowest level.
    """
    combinations = itertools.combinations(self._collectors, 2)
    for collector_1, collector_2 in combinations:
      if collector_1.is_similar(collector_2):
        max_collector = max(collector_1, collector_2)
        self._collectors.remove(max_collector)

  def customize(self, kwargs: dict) -> None:
    """Changes collectors in the set based on provided arguments mapping.

    Args:
      kwargs:
        Mapping between name and values of elements in collector to be
        customized.
    """
    for collector in self.collectors:
      collector.customize(kwargs)

  def __bool__(self):
    return bool(self.collectors)

  def __eq__(self, other) -> bool:
    return self.collectors == other.collectors

  def __contains__(self, key: query_target.Collector) -> bool:
    return key in self.collectors

  def __iter__(self):
    return iter(self.collectors)

  def __len__(self) -> int:
    return len(self.collectors)

  def add(self, collector) -> None:
    self._collectors.add(collector)

  def discard(self, collector) -> None:
    self._collectors.discard(collector)


def _read_files(path):
  with open(path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
  return data


def define_collectors(path: str):
  _registry: dict = defaultdict(dict)
  files = [file for file in glob.glob(path)]
  results = [_read_files(file) for file in files]
  for data in results:
    for collector_data in data:
      coll = query_target.Collector.from_definition(collector_data)
      _registry[coll.name] = coll
      for subregistry in collector_data.get('registries'):
        _registry[subregistry].update({coll.name: coll})
      if 'has_conversion_split' in collector_data:
        conv_coll = coll.create_conv_collector()
        _registry[conv_coll.name] = conv_coll
  return _registry
