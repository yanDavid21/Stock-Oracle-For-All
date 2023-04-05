from typing import Any, Dict, List, Optional, Set, Union

from dagster import OpDefinition, get_dagster_logger, op

from mercury._utils import CategoryKeyError, build_id
from mercury.adapters.yahoo_finance_api import YahooFinanceApiCategory
from mercury.base.base_op import BaseCategorizedOp, BaseCategorizedOpFactory
from mercury.base.config.providers import Provider


class YahooFinanceApiFetchLatestPriceOp(BaseCategorizedOp):
    def __init__(
        self,
        category: YahooFinanceApiCategory,
        provider: Provider = Provider.YAHOO_FINANCE_API,
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


class YahooFinanceApiFetchLatestPriceOpFactory(BaseCategorizedOpFactory):
    def create_op(self, category: YahooFinanceApiCategory, **kwargs) -> OpDefinition:
        try:
            category = YahooFinanceApiCategory[category.upper()]
        except KeyError as key_err:
            raise CategoryKeyError(YahooFinanceApiCategory) from key_err
        return YahooFinanceApiFetchLatestPriceOp(category).build(**kwargs)
