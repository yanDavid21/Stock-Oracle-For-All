import redis
from mercury.base.config.providers import Provider




class RedisStockAPI:
    def __init__(self):
        self.redis = redis.Redis(host = 'localhost', port = '6379', charset="utf-8")

    def publish_stock(self, api_name: str, msg: str):
        self.redis.publish(api_name, msg)

    def receive_stock_price_aggregate(self):
        sub = self.redis.pubsub()
        sub.subscribe(Provider.YAHOO_FINANCE_API)
        sub.subscribe(Provider.YH_FINANCE_API)
        return sub.listen()
    



