from pydantic import BaseSettings


class Settings(BaseSettings):
    @staticmethod
    def fastapi_docs_url() -> str:
        return '/docs'

    @staticmethod
    def fastapi_openapi_url() -> str:
        return '/openapi.json'


conf = Settings()
