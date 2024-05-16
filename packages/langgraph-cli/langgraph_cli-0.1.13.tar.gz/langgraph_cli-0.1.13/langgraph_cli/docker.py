import pathlib
from typing import Optional


ROOT = pathlib.Path(__file__).parent.resolve()


DB = f"""
    langgraph-postgres:
        image: postgres:16
        restart: on-failure
        healthcheck:
            test: pg_isready -U postgres
            start_interval: 1s
            start_period: 5s
            interval: 5s
            retries: 5
        ports:
            - "5433:5432"
        environment:
            POSTGRES_DB: postgres
            POSTGRES_USER: postgres
            POSTGRES_PASSWORD: postgres
        volumes:
            - ./.langgraph-data:/var/lib/postgresql/data
            - {ROOT}/initdb:/docker-entrypoint-initdb.d
"""

DEBUGGER = """
    langgraph-debugger:
        image: langchain/langserve-debugger
        restart: on-failure
        ports:
            - "{debugger_port}:5173"
        depends_on:
            langgraph-api:
                condition: service_healthy
        environment:
            VITE_API_BASE_URL: http://localhost:{port}
"""


def compose(
    *,
    python_version: str,
    port: int,
    debugger_port: Optional[int] = None,
    # postgres://user:password@host:port/database?option=value
    postgres_uri: Optional[str] = None,
) -> str:
    if postgres_uri is None:
        include_db = True
        postgres_uri = "postgres://postgres:postgres@langgraph-postgres:5432/postgres?sslmode=disable&search_path=langgraph"
    else:
        include_db = False

    return f"""
services:
{DB if include_db else ""}
{DEBUGGER.format(port=port, debugger_port=debugger_port) if debugger_port else ""}
    langgraph-api:
        image: langchain/langgraph-api:{python_version}
        restart: on-failure
        ports:
            - "{port}:8000"
        depends_on:
            langgraph-postgres:
                condition: service_healthy
        environment:
            POSTGRES_URI: {postgres_uri}
"""
