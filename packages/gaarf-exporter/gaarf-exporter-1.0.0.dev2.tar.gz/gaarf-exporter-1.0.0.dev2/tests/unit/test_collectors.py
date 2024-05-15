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
from __future__ import annotations

import pytest

from gaarf_exporter import collectors
from gaarf_exporter import query_elements
from gaarf_exporter import target as query_target


class TestRegistry:

  @pytest.fixture(scope='class')
  def registry(self):
    return collectors.Registry.from_collector_definitions()

  def test_default_collectors_returns_correct_target_names(self, registry):
    default_collectors = registry.default_collectors
    expected = {
        'conversion_action',
        'ad_disapprovals',
        'mapping',
        'performance',
    }

    assert {collector.name for collector in default_collectors} == expected

  def test_extract_collector_targets_returns_correct_collectors_from_registry(
      self, registry):
    actual = registry.find_collectors('performance,mapping')
    expected = {
        'mapping',
        'performance',
    }

    assert {collector.name for collector in actual} == expected

  def test_extract_collector_targets_returns_all_collectors_from_subregistry(
      self, registry):
    actual = registry.find_collectors('default')
    expected = {
        'conversion_action',
        'ad_disapprovals',
        'mapping',
        'performance',
    }

    assert {collector.name for collector in actual} == expected

  def test_extract_collector_targets_returns_unique_collectors_from_registry_and_sub_registry(
      self, registry):
    actual = registry.find_collectors('default,performance,mapping')
    expected = {
        'conversion_action',
        'ad_disapprovals',
        'mapping',
        'performance',
    }

    assert {collector.name for collector in actual} == expected

  def test_extract_collector_targets_returns_empty_set_when_collectors_are_not_found(
      self, registry):
    actual = registry.find_collectors('non-existing-collector')

    assert actual == collectors.CollectorSet()


class TestCollectorSet:

  @pytest.fixture
  def simple_target(self):
    return query_target.Collector(
        name='simple',
        metrics='impressions',
        level=query_target.CollectorLevel.AD_GROUP)

  @pytest.fixture
  def simple_target_at_customer_level(self):
    return query_target.Collector(
        name='simple_customer_level',
        metrics='impressions',
        level=query_target.CollectorLevel.CUSTOMER)

  @pytest.fixture
  def no_metric_target(self):
    return query_target.ServiceCollector(
        name='mapping',
        metrics=[
            query_elements.Field(name='1', alias='info'),
        ],
        dimensions=[
            query_elements.Field(name='ad_group.id', alias='ad_group_id'),
            query_elements.Field(name='ad_group.name', alias='ad_group_name'),
            query_elements.Field(name='campaign.id', alias='campaign_id'),
            query_elements.Field(name='campaign.name', alias='campaign_name'),
            query_elements.Field(name='customer.id', alias='customer_id'),
            query_elements.Field(
                name='customer.descriptive_name', alias='account_name'),
        ],
        filters=('ad_group.status = ENABLED'
                 ' AND campaign.status = ENABLED'
                 ' AND customer.status = ENABLED'))

  @pytest.fixture
  def collector_set(self):
    return collectors.CollectorSet(
        {query_target.Collector(name='test', metrics='clicks')},
        service_collectors=False)

  def test_collector_set_performs_deduplication(
      self, simple_target, simple_target_at_customer_level):
    collector_set = collectors.CollectorSet(
        {simple_target, simple_target_at_customer_level})
    assert simple_target_at_customer_level not in collector_set
    assert simple_target in collector_set

  def test_collector_set_generatees_service_target(self, simple_target,
                                                   no_metric_target):
    collector_set = collectors.CollectorSet({
        simple_target,
    })
    assert no_metric_target in collector_set

  def test_customize_returns_modified_target_start_end_date(
      self, collector_set):
    start_date = '2024-01-01'
    end_date = '2024-01-01'
    customize_dict = {
        'start_date': start_date,
        'end_date': end_date,
    }
    collector_set.customize(customize_dict)
    customized_collector = collector_set.collectors.pop()

    assert f"segments.date BETWEEN '{start_date}' AND '{end_date}'" in (
        customized_collector.query)

  @pytest.mark.parametrize('level', ['ad_group', 'campaign', 'customer'])
  def test_customize_returns_modified_target_level(self, collector_set, level):
    customize_dict = {
        'level': level,
    }
    collector_set.customize(customize_dict)
    customized_collector = collector_set.collectors.pop()

    assert f'FROM {level}' in customized_collector.query

  def test_customize_raises_key_error_on_incorrect_level(self, collector_set):
    customize_dict = {
        'level': 'unknown-level',
    }

    with pytest.raises(KeyError):
      collector_set.customize(customize_dict)


class TestNewRegistry:

  @pytest.fixture(scope='class')
  def registry(self):
    return collectors.Registry.from_collector_definitions()

  def test_load_collectors_gets_collector_by_name(self, registry):
    perf = registry.collectors.get('performance')
    assert perf.name == 'performance'
    assert perf.query

  def test_load_collectors_gets_collector_by_subregistry_name(self, registry):
    default_registry = registry.collectors.get('default')
    assert len(default_registry) == 3
    assert default_registry.get('performance').name == 'performance'

  def test_load_collectors_gets_conversion_split_collector(self, registry):
    perf = registry.collectors.get('performance_conversion_split')
    assert perf.query

  def test_load_collectors_gets_correct_collector_query(self, registry):
    collector = registry.find_collectors('performance')
    assert collector
