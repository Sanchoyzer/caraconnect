from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CI: bool = False

    SENTRY_DSN: str | None = None

    NEW_RELIC_CONFIG_FILE: str = 'newrelic.ini'
    NEW_RELIC_LICENSE_KEY: str | None = None

    @staticmethod
    def fastapi_docs_url() -> str:
        return '/docs'

    @staticmethod
    def fastapi_openapi_url() -> str:
        return '/openapi.json'


conf = Settings()
