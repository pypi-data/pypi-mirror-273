import time
from enum import Enum
from hashlib import md5
from typing import List, Optional

import redis

from .logger import logger

# from ..logger import logger

SESSION_METADATA_KEY_PREFIX = "crawler_session_meta_"  # hash
SESSION_URLS_KEY_PREFIX = "crawler_session_urls_"  # set
SESSION_CONTENT_KEY_PREFIX = "crawler_session_content_"  # set


class SessionStatus(Enum):
    NORMAL = 0
    STOPPED = 1


class Session:
    id: str
    r: redis.Redis
    meta_key: str
    urls_key: str
    content_key: str
    stats_channel: str

    def __init__(self, session_id, redis_inst: redis.Redis):
        self.id = session_id
        self.r = redis_inst
        self.meta_key = SessionManager.get_meta_key(self.id)
        self.urls_key = SessionManager.get_urls_key(self.id)
        self.content_key = SessionManager.get_content_key(self.id)
        self.stats_channel = Session.get_stats_channel(self.id)

    @staticmethod
    def get_stats_channel(session_id_or_mask):
        return f"stats_channel_{session_id_or_mask}"

    @staticmethod
    def get_stats_channel_mask():
        return Session.get_stats_channel("*")

    @staticmethod
    def get_session_id_by_channel(channel_name):
        return channel_name[14:]

    def get_meta(self):
        raw = self.r.hgetall(self.meta_key)
        res = {
            "hint_id": raw[b"hint_id"].decode(),
            "url": raw[b"url"].decode(),
            "total_tasks": int(raw[b"total_tasks"]),
            "complete_tasks": int(raw[b"complete_tasks"]),
            "failed_tasks": int(raw[b"failed_tasks"]),
            "rejected_tasks": int(raw[b"rejected_tasks"]),
            "crawled_content": int(raw[b"crawled_content"]),
            "evaluated_content": int(raw[b"evaluated_content"]),
            "status": int(raw[b"status"] if b"status" in raw else SessionStatus.NORMAL.value),
        }
        return res

    def set_status(self, status: SessionStatus):
        self.r.hset(self.meta_key, "status", status.value)

    def is_stopped(self):
        status = self.r.hget(self.meta_key, "status")
        return status is not None and int(status) == SessionStatus.STOPPED.value

    def add_url(self, url):
        # urls are stored in sets
        res = self.r.sadd(self.urls_key, url)
        if res:
            self.r.hincrby(self.meta_key, "total_tasks", 1)
        return res == 1

    def has_url(self, url):
        res = self.r.sismember(self.urls_key, url)
        # logger.info( f'has_url {res=} {type(res)=}')
        return res

    def add_content(self, url):
        return self.r.sadd(self.content_key, url)

    def has_content(self, url):
        return self.r.sismember(self.content_key, url)

    def inc_complete_urls(self):
        self.r.hincrby(self.meta_key, "complete_tasks", 1)
        self.r.publish(self.stats_channel, 1)

    def inc_failed_urls(self):
        self.r.hincrby(self.meta_key, "failed_tasks", 1)
        self.r.publish(self.stats_channel, 1)

    def inc_rejected_urls(self):
        self.r.hincrby(self.meta_key, "rejected_tasks", 1)
        self.r.publish(self.stats_channel, 1)

    def inc_crawled_content(self):
        self.r.hincrby(self.meta_key, "crawled_content", 1)
        self.r.publish(self.stats_channel, 1)

    def inc_evaluated_content(self):
        self.r.hincrby(self.meta_key, "evaluated_content", 1)
        self.r.publish(self.stats_channel, 1)

    def exists(self):
        res = self.r.exists(self.meta_key)
        return res


class SessionManager:
    def __init__(self, host, port=6379, db=0, protocol=3):
        self.r = redis.Redis(host=host, port=port, db=db, protocol=protocol)

    def is_ready(self) -> bool:
        try:
            self.r.ping()
            return True
        except redis.exceptions.ConnectionError:
            return False

    def create(self, hint_id=0, url="") -> Session:
        session_id = self.gen_session_id()
        self.r.hset(
            SessionManager.get_meta_key(session_id),
            mapping={
                "hint_id": hint_id,
                "url": url,
                "total_tasks": 0,
                "complete_tasks": 0,
                "failed_tasks": 0,
                "rejected_tasks": 0,
                "crawled_content": 0,
                "evaluated_content": 0,
                "status": SessionStatus.NORMAL.value,
            },
        )
        # logger.info( f'hset result {r=} {type(r)=}')
        return Session(session_id, self.r)

    def has(self, session_id) -> bool:
        res = self.r.exists(SessionManager.get_meta_key(session_id))
        # logger.info( f'sessionmanager.has {res=} {type(res)=}')
        return res

    def get(self, session_id) -> Optional[Session]:
        return Session(session_id, self.r) if self.has(session_id) else None

    def remove(self, session_id):
        self.r.delete(SessionManager.get_meta_key(session_id))
        self.r.delete(SessionManager.get_urls_key(session_id))
        self.r.delete(SessionManager.get_content_key(session_id))

    def gen_session_id(self) -> str:
        # TODO: add existance check
        return md5(str(time.time()).encode()).hexdigest()

    @staticmethod
    def get_meta_key(session_id):
        return f"{SESSION_METADATA_KEY_PREFIX}{session_id}"

    @staticmethod
    def get_urls_key(session_id):
        return f"{SESSION_URLS_KEY_PREFIX}{session_id}"

    @staticmethod
    def get_content_key(session_id):
        return f"{SESSION_CONTENT_KEY_PREFIX}{session_id}"

    def get_ids(self, limit) -> List[str]:
        keys = self.r.keys(f"{SESSION_METADATA_KEY_PREFIX}*")
        if len(keys) > limit:
            keys = keys[0:limit]
        n = len(SESSION_METADATA_KEY_PREFIX)
        return [k[n:] for k in keys]
