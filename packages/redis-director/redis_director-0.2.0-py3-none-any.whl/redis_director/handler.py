from .subscriber import Subscriber


def generic_set_handler(key: str):
    def handler(route: Subscriber, payload):
        route.redis.sadd(key, payload)

    return handler


def generic_list_handler(key: str):
    def handler(route: Subscriber, payload):
        route.redis.lpush(key, payload)

    return handler
