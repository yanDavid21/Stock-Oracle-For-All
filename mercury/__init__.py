import warnings

from dagster import Definitions, ExperimentalWarning
from dotenv import load_dotenv

from mercury.adapters.yahoo_finance_api import YahooFinanceApiCategory, YahooFinanceApiFetchLatestPriceScheduleFactory
from mercury.adapters.yh_finance_api import YHFinanceApiCategory, YHFinanceApiFetchLatestPriceScheduleFactory

# Avoid experimental features
warnings.filterwarnings("ignore", category=ExperimentalWarning)

load_dotenv(override=False)

EVERY_TWO_HOURS = "0 */2 * * *"

yhLatestPriceSchedule = YHFinanceApiFetchLatestPriceScheduleFactory()
yahooLatestPriceSchedule = YahooFinanceApiFetchLatestPriceScheduleFactory()

defs = Definitions(
    schedules=[
        yhLatestPriceSchedule.create_schedule(YHFinanceApiCategory.LATEST_PRICE, EVERY_TWO_HOURS),
        yahooLatestPriceSchedule.create_schedule(YahooFinanceApiCategory.LATEST_PRICE, EVERY_TWO_HOURS),
    ]
)
