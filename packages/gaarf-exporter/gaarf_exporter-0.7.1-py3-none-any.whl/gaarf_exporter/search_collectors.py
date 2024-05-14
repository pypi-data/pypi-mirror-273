from gaarf_exporter.query_elements import Field
from gaarf_exporter.target import Target
from gaarf_exporter.target import TargetLevel
from gaarf_exporter import collectors


@collectors.collector('search')
@collectors.register_conversion_split_collector
class SearchTermsCollector(collectors.CollectorCustomizerMixin):
  """Gets basic performance metrics for search terms on ad_group level."""
  name = 'search_terms'
  target = Target(
      name=name,
      metrics=_DEFAULT_METRICS,
      level=TargetLevel.AD_GROUP,
      resource_name='search_term_view',
      dimensions=[Field('search_term_view.search_term', 'search_term')],
      filters=('segments.date DURING TODAY '
               "AND campaign.status = 'ENABLED' "
               'AND metrics.clicks > 0'))

  def __init__(self, **kwargs):
    self.targets = collectors.CollectorCustomizerMixin.customize_target(
        self.target, **kwargs)
