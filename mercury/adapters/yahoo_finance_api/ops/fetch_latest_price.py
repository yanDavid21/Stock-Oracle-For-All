from typing import Any, Dict, List, Optional, Set, Union
from redis.api import RedisStockAPI
from dagster import OpDefinition, get_dagster_logger, op
import requests
import json
from datetime import datetime
from mercury._utils import CategoryKeyError, build_id
from mercury._utils.stock_list import StockList
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
        self.list_stock = StockList().data,

    def _get_price(self, key: str, ticker: str) -> str:
        """Crawl price data from API operation

        Args:
            page_url (str): the url link of the api
            headers (str): the key for your api
            ticker (str): the stock ticker
        Returns: the current price of the stock ticker"""
        current_time = datetime.now() \
            .replace(hour=datetime.now().hour, minute=0, second=0, microsecond=0) \
            .strftime('%Y-%m-%d %H:%M:%S')
        get_dagster_logger().info('Begin crawling...')
        page_url = f"https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{ticker}/financial-data"
        headers = {"X-RapidAPI-Key": key,
                   "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"}
        response = requests.request("GET", page_url, headers=headers)
        price = response.json()['financialData']['currentPrice']['raw']
        message = json.dumps({"ticker": ticker,
                              "price": price,
                              "datetime": current_time, }
                             )
        get_dagster_logger().info('Finish crawling!')
        return message

    def build(self, **kwargs) -> OpDefinition:
        @op(
            name=build_id(provider=self.provider, identifier=f"fetch_{self.category}_stock_db_op"),
            config_schema=self.config_schema,
            required_resource_keys=self.required_resource_keys,
            **kwargs,
        )
        def _op():
            redis = RedisStockAPI()
            for stock in self.list_stock:
                # Main log to fetch data from data source goes here
                price = self._get_price("70f59a384fmsh1cfc6e9694781c3p1107f5jsna9f6206b0c3d", stock)
                redis.publish_stock(self.provider, price)

        return _op


class YahooFinanceApiFetchLatestPriceOpFactory(BaseCategorizedOpFactory):
    def create_op(self, category: YahooFinanceApiCategory, **kwargs) -> OpDefinition:
        try:
            category = YahooFinanceApiCategory[category.upper()]
        except KeyError as key_err:
            raise CategoryKeyError(YahooFinanceApiCategory) from key_err
        return YahooFinanceApiFetchLatestPriceOp(category).build(**kwargs)
