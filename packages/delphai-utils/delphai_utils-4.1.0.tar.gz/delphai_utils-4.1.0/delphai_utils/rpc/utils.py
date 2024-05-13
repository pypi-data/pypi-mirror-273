import datetime
import functools
import importlib.metadata
import re


def fix_message_timestamp(func):
    @functools.wraps(func)
    def inner(message):
        # Fix `pamqp` naive timestamp
        if message.timestamp:
            message.timestamp = message.timestamp.replace(tzinfo=datetime.timezone.utc)

        return func(message)

    return inner


def clean_service_name(service_name):
    return re.sub("[^a-z0-9-]+", "-", service_name.strip().lower())


def make_connection_name(service_name):
    package_name = __package__.split(".")[0]
    package_name_version = importlib.metadata.version(package_name)

    return f"{service_name} ({package_name} v{package_name_version})"
