from typing import Any, Dict, List, Optional, Set, Union

from dagster import OpDefinition, get_dagster_logger, op

from mercury._utils import CategoryKeyError, PhantomOp, build_id
from mercury.adapters.yh_finance_api import YHFinanceApiCategory
from mercury.base.base_op import BaseCategorizedOp, BaseCategorizedOpFactory
from mercury.base.config.providers import Provider


class YHFinanceApiOp(BaseCategorizedOp):
    def __init__(
        self,
        category: YHFinanceApiCategory,
        provider: Provider = Provider.YH_FINANCE_API,
        required_resource_keys: Optional[Set[str]] = None,
        config_schema: Optional[Union[Dict[str, Any], List]] = None,
    ) -> None:
        super().__init__(category, provider, required_resource_keys, config_schema)

    def build(self, **kwargs) -> OpDefinition:
        @op(
            name=build_id(provider=self.provider, identifier=f"fetch_{self.category}_stock_db_op"),
            config_schema=self.config_schema,
            required_resource_keys=self.required_resource_keys,
            **kwargs,
        )
        def _op():
            # Main log to fetch data from data srouce goes here
            data = ""
            get_dagster_logger().log(data)

        return _op


class YHFinanceApiOpFactory(BaseCategorizedOpFactory):
    def create_op(self, category: YHFinanceApiCategory, **kwargs) -> OpDefinition:
        try:
            category = YHFinanceApiCategory[category.upper()]
        except KeyError as key_err:
            raise CategoryKeyError(YHFinanceApiCategory) from key_err
        if category == YHFinanceApiCategory.LATEST_PRICE:
            return YHFinanceApiOp(category).build(**kwargs)
        return PhantomOp().build()
