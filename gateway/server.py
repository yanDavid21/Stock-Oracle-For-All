import time
import json
from database.redis import RedisStockAPI
from database.mongo import MongoAPI
import datetime
from pytz import timezone
from numpy import mean

EXPECTED_QUERY_TIME_HRS = 2
NUM_OF_PROVIDERS = 2
EXPECTED_API_RESOLUTION_MS = 5


class GatewayServer():
    def __init__(self) -> None:
        self.redis_conn = RedisStockAPI()
        self.mongo_conn = MongoAPI()
        self.pub_sub_connection = self.redis_conn.subcribe_to_stocks()
        self.last_submitted_time = None
        self.providers = dict()

    def handle_message(self):
        message = self.pub_sub_connection.get_message()
        if message:
            decoded_message = json.loads(message)
            data = decoded_message.get("data", None)
            channel = decoded_message["channel"]
            self.insert_message_into_buffer(channel, data)
            if data != None:
                self.aggregate_values_from_message(data["ticker"])

    def insert_message_into_buffer(self, channel, data):
        ticker = data["ticker"]
        price = data["price"]
        timestamp = data["timestamp"]
        self.providers.setdefault(channel, {})[ticker] = {"price": price, "timestamp": timestamp}

    def detect_failure(self):
        est_timezone = timezone('EST')
        if self.last_submitted_time != None:
            current_time = datetime.datetime.utcnow(est_timezone)
            time_since_last_submittal = current_time - self.last_submitted_time
            if time_since_last_submittal >= datetime.timedelta(hours=EXPECTED_QUERY_TIME_HRS * 2):
                self.fail("Last submitted to database too long ago. Failure in pipeline detected.")

    def fail(self, msg):
        raise RuntimeError("Process failed: " + msg)

    def aggregate_values_from_message(self, ticker):
        latest_ticker_prices = []
        for channel_buffer in self.providers.values():
            if ticker in channel_buffer:
                latest_ticker_prices.append(channel_buffer[ticker])
        if len(latest_ticker_prices) == NUM_OF_PROVIDERS:
            if self.verify_same_epoch(latest_ticker_prices):
                aggregated_value = {"ticker": ticker, "timestamp": datetime.datetime.utcnow(),
                                    "price": mean(latest_ticker_prices)}
                self.mongo_conn.insert_to_collection(aggregated_value)
            else:
                self.fail("Failure in API data pipeline detected. Mismatching datetimes for prices across API's")

    def verify_same_epoch(self, prices_list):
        timestamps = [price.get("timestamp") for price in prices_list]
        max_time_diff = max(timestamps) - min(timestamps)
        return max_time_diff < datetime.timedelta(milliseconds=EXPECTED_API_RESOLUTION_MS)


if __name__ == '__main__':
    server = GatewayServer()
    while True:
        server.handle_message()
        server.detect_failure()
        time.sleep(0.01)
