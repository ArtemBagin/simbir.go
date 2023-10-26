from blacklist.redis_init import init_redis_pool


class BlackList:
    def __init__(self, redis=init_redis_pool) -> None:
        self._redis = redis

    def add_blacklist_token(self, value) -> int:
        for session in self._redis():
            res = session.lpush('tokens:black_list', f'token:{value}')
            return res

    def get_blacklisted_tokens(self):
        for session in self._redis():
            res = session.lrange('tokens:black_list', 0, -1)
            return res

    def is_token_blacklisted(self, value):
        return f'token:{value}' in self.get_blacklisted_tokens()


blacklist = BlackList()
