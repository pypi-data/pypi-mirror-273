from typing import Any, Callable, Dict
from fun_things.math import weighted_distribution
from redis import Redis

from .subscriber import Subscriber


class Publisher:
    def __init__(
        self,
        redis: Redis,
        score_name: str,
        queue_name: str,
    ):
        self.__subscribers: Dict[str, Subscriber] = {}

        self.__redis = redis
        self.__score_name: str = score_name
        self.__queue_name: str = queue_name

    @property
    def redis(self):
        return self.__redis

    @property
    def score_name(self):
        return self.__score_name

    @property
    def queue_name(self):
        return self.__queue_name

    def reset_scores(self):
        for subscriber in self.__subscribers.values():
            subscriber.reset_score()

    def add_subscriber(
        self,
        score_value: str,
        handler: Callable[[Subscriber, Any], None],
        default_score: float = 0,
        min_score: float = 1,
    ):
        self.__subscribers[score_value] = Subscriber.new(
            redis=self.__redis,
            score_name=self.__score_name,
            score_value=score_value,
            default_score=default_score,
            min_score=min_score,
            handler=handler,
        )

        return self

    def get_subscriber(self, name: str) -> Subscriber:
        if name not in self.__subscribers:
            return None  # type: ignore

        return self.__subscribers[name]

    def publish(
        self,
        batch_size=1,
    ):
        payloads = self.__redis.spop(
            self.__queue_name,
            batch_size,
        )

        if payloads == None:
            return self

        for payload in payloads:
            subscribers = weighted_distribution(
                self.__subscribers.values(),
                lambda subscriber: subscriber.score,
            )

            for subscribe in subscribers:
                subscribe.add_score(-1)

                if subscribe.handler != None:
                    subscribe.handler(subscribe, payload)

                break

        return self
