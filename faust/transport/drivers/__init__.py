"""Transport registry."""
from yarl import URL

from .aiokafka import Transport as AIOKafkaTransport
from .confluent import Transport as ConfluentTransport

__all__ = ["by_name", "by_url"]


DRIVERS = {
    "aiokafka": AIOKafkaTransport,
    "kafka": AIOKafkaTransport,
    "confluent": ConfluentTransport

}


def by_name(driver_name: str):
    return DRIVERS[driver_name]


def by_url(url: URL):
    scheme = url.scheme
    return DRIVERS[scheme]
