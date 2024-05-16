from typing import Any, Callable, NamedTuple
from redis import Redis
from redis.commands.core import Script
from .constants import INCREMENT_LUA_SCRIPT


class Subscriber(NamedTuple):
    redis: Redis
    score_name: str
    """
    The Redis key for the score.
    """
    score_value: str
    """
    The Redis member value for the score.
    """
    default_score: float
    """
    The default score.
    """
    min_score: float
    """
    """
    handler: Callable[["Subscriber", Any], None]  # type: ignore
    increment_script: Script

    @staticmethod
    def new(
        redis: Redis,
        score_name: str = None,  # type: ignore
        score_value: str = None,  # type: ignore
        default_score: float = 0,
        min_score: float = 1,
        handler: Callable[["Subscriber", Any], None] = None,  # type: ignore
    ):
        return Subscriber(
            redis=redis,
            score_name=score_name,
            score_value=score_value,
            default_score=default_score,
            min_score=min_score,
            handler=handler,
            increment_script=redis.register_script(
                INCREMENT_LUA_SCRIPT,
            ),  # type: ignore
        )

    @property
    def score(self) -> float:
        score = self.redis.zscore(
            self.score_name,
            self.score_value,
        )

        if score == None:
            self.redis.zadd(
                self.score_name,
                {
                    self.score_value: self.default_score,
                },
                nx=True,
            )

            return self.default_score

        return score  # type: ignore

    def add_score(self, value: float):
        return self.increment_script(
            self.score_name,
            (
                self.score_value,
                value,
                self.min_score,
            ),
        )

    def set_score(self, value: float):
        self.redis.zadd(
            self.score_name,
            {
                self.score_value: value,
            },
            xx=True,
        )

        return value

    def reset_score(self):
        self.set_score(self.default_score)

        return self.default_score
