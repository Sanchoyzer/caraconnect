import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.httpx import HttpxIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration


def setup_sentry(dsn: str, rate: float = 1.0) -> None:
    integrations = [StarletteIntegration(), FastApiIntegration(), HttpxIntegration()]
    sentry_sdk.init(dsn=dsn, integrations=integrations, traces_sample_rate=rate)
