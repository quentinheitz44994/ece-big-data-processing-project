"""Test doubles and builders shared by the streaming tests."""

from __future__ import annotations


def change(
    event_id, title, dt_text, wiki="enwiki", kind="edit", ns=0, bot=False, old=100, new=150, **extra
):
    event = {
        "meta": {
            "id": event_id,
            "dt": dt_text,
            "domain": "en.wikipedia.org",
            "stream": "mediawiki.recentchange",
        },
        "title": title,
        "wiki": wiki,
        "type": kind,
        "namespace": ns,
        "bot": bot,
        "minor": False,
        "user": "SomeEditor",
        "comment": "copyedit",
        "length": {"old": old, "new": new},
        "revision": {"old": 1, "new": 2},
        "server_name": "en.wikipedia.org",
    }
    event.update(extra)
    return event


class FakeKafkaProducer:
    def __init__(self):
        self.messages, self.flushed = [], False

    def produce(self, topic, key=None, value=None, on_delivery=None):
        self.messages.append((topic, key, value))

    def poll(self, timeout):
        return 0

    def flush(self, timeout):
        self.flushed = True
