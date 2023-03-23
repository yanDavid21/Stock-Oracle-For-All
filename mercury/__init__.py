import warnings

from dagster import Definitions, ExperimentalWarning
from dotenv import load_dotenv

from mercury.adapters.yahoo_finance_api import YahooFinanceApiCategory, YahooFinanceApiJobFactory
from mercury.adapters.yh_finance_api import YHFinanceApiCategory, YHFinanceApiJobFactory
from mercury.base.base_jobs import init_categorized_job

# Avoid experimental features
warnings.filterwarnings("ignore", category=ExperimentalWarning)

load_dotenv(override=False)

defs = Definitions(
    jobs=[
        *(init_categorized_job(YahooFinanceApiJobFactory(), YahooFinanceApiCategory)),
        *(init_categorized_job(YHFinanceApiJobFactory(), YHFinanceApiCategory)),
    ],
)
