from typing import Any, Dict, List, Optional, Set, Union

from dagster import OpDefinition, get_dagster_logger, op
import requests
from mercury._utils import CategoryKeyError, PhantomOp, build_id
from mercury.adapters.yh_finance_api import YHFinanceApiCategory
from mercury.base.base_op import BaseCategorizedOp, BaseCategorizedOpFactory
from mercury.base.config.providers import Provider


class YHFinanceApiFetchLatestPriceOp(BaseCategorizedOp):
    def __init__(
        self,
        category: YHFinanceApiCategory,
        provider: Provider = Provider.YH_FINANCE_API,
        required_resource_keys: Optional[Set[str]] = None,
        config_schema: Optional[Union[Dict[str, Any], List]] = None,
    ) -> None:
        super().__init__(category, provider, required_resource_keys, config_schema)

    def _get_price(self, key: str, ticker: str) -> str:
        """Crawl price data from API operation
        
        Args:
            page_url (str): the url link of the api
            headers (str): the key for your api
            ticker (str): the stock ticker
        Returns: the current price of the stock ticker"""
        get_dagster_logger().info('Begin crawling...')
        page_url = "https://real-time-finance-data.p.rapidapi.com/stock-quote"
        headers = {"X-RapidAPI-Key": key,
            "X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"}
        querystring = {"symbol": ticker,"language":"en"}
        response = requests.request("GET", page_url, headers=headers, params=querystring)
        price = response.json()['data']['price']
        get_dagster_logger().info('Finish crawling!')
        return f"{ticker}:{price}"    

    def build(self, **kwargs) -> OpDefinition:
        @op(
            name=build_id(provider=self.provider, identifier=f"fetch_{self.category}_stock_db_op"),
            config_schema=self.config_schema,
            required_resource_keys=self.required_resource_keys,
            **kwargs,
        )
        def _op():
            # Main log to fetch data from data source goes here
            return self._get_price("70f59a384fmsh1cfc6e9694781c3p1107f5jsna9f6206b0c3d", "NFLX")
        
        return _op


class YHFinanceApiFetchLatestPriceOpFactory(BaseCategorizedOpFactory):
    def create_op(self, category: YHFinanceApiCategory, **kwargs) -> OpDefinition:
        try:
            category = YHFinanceApiCategory[category.upper()]
        except KeyError as key_err:
            raise CategoryKeyError(YHFinanceApiCategory) from key_err
        return YHFinanceApiFetchLatestPriceOp(category).build(**kwargs)
