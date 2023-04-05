from dagster import DefaultScheduleStatus, ScheduleDefinition
from strenum import StrEnum

from mercury._utils.errors import CategoryKeyError
from mercury.adapters.yh_finance_api.category import YHFinanceApiCategory
from mercury.adapters.yh_finance_api.jobs import YHFinanceApiFetchLatestPriceJobFactory
from mercury.base.base_schedule import BaseCategorizedScheduleFactory
from mercury.base.config.providers import Provider
from mercury.schedules.fetch_latest_price_schedule import BaseFetchLatestPriceSchedule


class YHFinanceApiFetchLatestPriceSchedule(BaseFetchLatestPriceSchedule):
    def __init__(
        self,
        category: StrEnum,
        cron_schedule: str,
    ) -> None:
        self._default_status = DefaultScheduleStatus.STOPPED
        super().__init__(
            category=category,
            provider=Provider.YH_FINANCE_API,
            cron_schedule=cron_schedule,
            default_status=DefaultScheduleStatus.STOPPED,
            fetch_latest_price_job_factory=YHFinanceApiFetchLatestPriceJobFactory(),
        )


class YHFinanceApiFetchLatestPriceScheduleFactory(BaseCategorizedScheduleFactory):
    """Schedule Factory for creating Fetch Latest Price schedule for specified category"""

    def create_schedule(self, category: YHFinanceApiCategory, cron_schedule: str, **kwargs) -> ScheduleDefinition:
        try:
            category = YHFinanceApiCategory[category.upper()]
        except KeyError:
            raise CategoryKeyError(YHFinanceApiCategory) from KeyError
        fetch_latest_price_schedule = YHFinanceApiFetchLatestPriceSchedule(category, cron_schedule).build(**kwargs)
        return fetch_latest_price_schedule
