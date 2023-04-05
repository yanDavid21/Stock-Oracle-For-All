from typing import Optional

from dagster import DefaultScheduleStatus, RunRequest, ScheduleDefinition, get_dagster_logger, schedule
from strenum import StrEnum

from mercury._utils.id import build_id
from mercury.base.base_jobs import BaseCategorizedJobFactory
from mercury.base.base_schedule import BaseCategorizedSchedule
from mercury.base.config.providers import Provider


class BaseFetchLatestPriceSchedule(BaseCategorizedSchedule):
    def __init__(
        self,
        category: StrEnum,
        provider: Provider,
        cron_schedule: str,
        default_status: DefaultScheduleStatus,
        fetch_latest_price_job_factory: BaseCategorizedJobFactory,
        execution_timezone: Optional[str] = None,
    ) -> None:
        self._category = category
        self._fetch_latest_price_job_factory = fetch_latest_price_job_factory
        self._job = self.fetch_latest_price_job_factory.create_job(self.category)
        super().__init__(
            category=self.category,
            provider=provider,
            cron_schedule=cron_schedule,
            job=self.job,
            default_status=default_status,
            execution_timezone=execution_timezone,
        )

    @property
    def fetch_latest_price_job_factory(self) -> BaseCategorizedJobFactory:
        return self._fetch_latest_price_job_factory

    def build(self, **kwargs) -> ScheduleDefinition:
        """Build a Schedule for fetch latest price

        Returns:
            ScheduleDefinition: Dagster's Schedule Definition
        """

        @schedule(
            name=build_id(self.provider, f"fetch_{self.category}_schedule"),
            cron_schedule=self.cron_schedule,
            job=self.job,
            execution_timezone=self.execution_timezone,
            default_status=self.default_status,
            **kwargs,
        )
        def _schedule(context) -> RunRequest:
            get_dagster_logger().info(f"Trigger schedule of fetch latest price {self.category}.")
            return RunRequest(run_key=None)

        return _schedule
