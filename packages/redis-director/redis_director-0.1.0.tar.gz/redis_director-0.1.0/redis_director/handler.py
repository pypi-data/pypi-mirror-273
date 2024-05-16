from .subscriber import Subscriber


def generic_set_handler(name: str):
    def handler(route: Subscriber, payload):
        route.redis.sadd(name, payload)

    return handler


def generic_list_handler(name: str):
    def handler(route: Subscriber, payload):
        route.redis.lpush(name, payload)

    return handler
