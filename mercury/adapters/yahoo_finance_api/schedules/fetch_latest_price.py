from dagster import DefaultScheduleStatus, ScheduleDefinition
from strenum import StrEnum

from mercury._utils.errors import CategoryKeyError
from mercury.adapters.yahoo_finance_api.category import YahooFinanceApiCategory
from mercury.adapters.yahoo_finance_api.jobs import YahooFinanceApiFetchLatestPriceJobFactory
from mercury.base.base_schedule import BaseCategorizedScheduleFactory
from mercury.base.config.providers import Provider
from mercury.schedules.fetch_latest_price_schedule import BaseFetchLatestPriceSchedule


class YahooFinanceApiFetchLatestPriceSchedule(BaseFetchLatestPriceSchedule):
    def __init__(
        self,
        category: StrEnum,
        cron_schedule: str,
    ) -> None:
        self._default_status = DefaultScheduleStatus.STOPPED
        super().__init__(
            category=category,
            provider=Provider.YAHOO_FINANCE_API,
            cron_schedule=cron_schedule,
            default_status=DefaultScheduleStatus.STOPPED,
            fetch_latest_price_job_factory=YahooFinanceApiFetchLatestPriceJobFactory(),
        )


class YahooFinanceApiFetchLatestPriceScheduleFactory(BaseCategorizedScheduleFactory):
    """Schedule Factory for creating Fetch Latest Price schedule for specified category"""

    def create_schedule(self, category: YahooFinanceApiCategory, cron_schedule: str, **kwargs) -> ScheduleDefinition:
        try:
            category = YahooFinanceApiCategory[category.upper()]
        except KeyError:
            raise CategoryKeyError(YahooFinanceApiCategory) from KeyError
        fetch_latest_price_schedule = YahooFinanceApiFetchLatestPriceSchedule(category, cron_schedule).build(**kwargs)
        return fetch_latest_price_schedule
