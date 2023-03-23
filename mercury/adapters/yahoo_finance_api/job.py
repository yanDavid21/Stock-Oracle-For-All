from dagster import JobDefinition

from mercury._utils.errors import CategoryKeyError
from mercury.adapters.yahoo_finance_api.category import YahooFinanceApiCategory
from mercury.adapters.yahoo_finance_api.ops import YahooFinanceApiOpFactory
from mercury.base.base_adapter_job import BaseAdapterJob
from mercury.base.base_jobs import BaseCategorizedJobFactory
from mercury.base.config.providers import Provider


class YahooFinanceApiJob(BaseAdapterJob):
    def __init__(
        self,
        category: YahooFinanceApiCategory,
    ) -> None:
        super().__init__(
            category=category,
            provider=Provider.YAHOO_FINANCE_API,
            adapter_op_factory=YahooFinanceApiOpFactory,
            resource_defs=None,
        )


class YahooFinanceApiJobFactory(BaseCategorizedJobFactory):
    def create_job(self, category: YahooFinanceApiCategory, **kwargs) -> JobDefinition:
        try:
            category = YahooFinanceApiCategory[category.upper()]
        except KeyError as key_err:
            raise CategoryKeyError(YahooFinanceApiCategory) from key_err
        adapter_job = YahooFinanceApiJob(category).build(**kwargs)
        return adapter_job
