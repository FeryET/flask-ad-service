from typing import Any


def generate_smorest_api_docs_config() -> dict[str, str]:
    return {
        "API_TITLE": "My API",
        "API_VERSION": "v1",
        "OPENAPI_JSON_PATH": "api-spec.json",
        "OPENAPI_RAPIDOC_PATH": "/rapidoc",
        "OPENAPI_RAPIDOC_URL": "https://unpkg.com/rapidoc/dist/rapidoc-min.js",
        "OPENAPI_REDOC_PATH": "/redoc",
        "OPENAPI_REDOC_URL": "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
        "OPENAPI_SWAGGER_UI_PATH": "/swagger-ui",
        "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        "OPENAPI_URL_PREFIX": "/docs",
        "OPENAPI_VERSION": "3.1.2",
    }


def generate_flask_sqlalchemy_config() -> dict[str, Any]:
    return {
        "SQLALCHEMY_DATABASE_URI": "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres",
        "SQLALCHEMY_ENGINE_OPTIONS": {"pool_pre_ping": True},
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }


def generate_flask_security_config() -> dict[str, Any]:
    return {
        "REMEMBER_COOKIE_SAMESITE": "strict",
        "SECRET_KEY": "7fFksx3hW-RJBnp954PG3qAHTJ2gJzKbi9B6XpGQTfE",
        "SECURITY_EMAIL_VALIDATOR_ARGS": {"check_deliverability": False},
        "SECURITY_PASSWORD_SALT": "266926640719280391640225122043389353677",
        "SESSION_COOKIE_SAMESITE": "strict",
    }


def generate_app_config() -> dict[str, Any]:
    return {
        "DEBUG": True,
        **generate_flask_security_config(),
        **generate_flask_sqlalchemy_config(),
        **generate_smorest_api_docs_config(),
    }
