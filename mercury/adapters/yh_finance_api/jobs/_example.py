from dagster import JobDefinition

from mercury._utils.errors import CategoryKeyError
from mercury.adapters.yh_finance_api.category import YHFinanceApiCategory
from mercury.adapters.yh_finance_api.ops import YHFinanceApiOpFactory
from mercury.base.base_adapter_job import BaseAdapterJob
from mercury.base.base_jobs import BaseCategorizedJobFactory
from mercury.base.config.providers import Provider


class YHFinanceApiJob(BaseAdapterJob):
    def __init__(
        self,
        category: YHFinanceApiCategory,
    ) -> None:
        super().__init__(
            category=category,
            provider=Provider.YH_FINANCE_API,
            adapter_op_factory=YHFinanceApiOpFactory,
            resource_defs=None,
        )


class YHFinanceApiJobFactory(BaseCategorizedJobFactory):
    def create_job(self, category: YHFinanceApiCategory, **kwargs) -> JobDefinition:
        try:
            category = YHFinanceApiCategory[category.upper()]
        except KeyError as key_err:
            raise CategoryKeyError(YHFinanceApiCategory) from key_err
        adapter_job = YHFinanceApiJob(category).build(**kwargs)
        return adapter_job
