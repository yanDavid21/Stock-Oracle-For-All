from enum import Enum
from typing import Any, Dict, Optional

from dagster import JobDefinition, job

from mercury._utils import build_id

from .base_jobs import BaseCategorizedJob
from .base_op import BaseCategorizedOpFactory
from .config.providers import Provider


class BaseAdapterJob(BaseCategorizedJob):
    def __init__(
        self,
        category: Enum,
        provider: Provider,
        adapter_op_factory: BaseCategorizedOpFactory,
        resource_defs: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            category,
            provider,
        )
        self._resource_defs = resource_defs
        self._adapter_op_factory = adapter_op_factory

    @property
    def adapter_op_factory(self) -> BaseCategorizedOpFactory:
        return self._adapter_op_factory

    def build(self, **kwargs) -> JobDefinition:
        adapter_op = self.adapter_op_factory().create_op(category=self.category)

        @job(
            name=build_id(provider=self.provider, identifier=f"{self.category}_stock_job"),
            resource_defs=self.resource_defs,
            **kwargs,
        )
        def _job():
            adapter_op()

        return _job
