import importlib
import logging


def instrument_dependencies(app):
    instrument_functions = [
        _instrument_django,
        _instrument_fastapi,
        _instrument_flask,
        _instrument_mysql,
        _instrument_elasticsearch,
        _instrument_requests
    ]
    for instrument_function in instrument_functions:
        try:
            instrument_function(app)
        except Exception as e:
            logging.warning(f"Error instrumenting {instrument_function.__name__}: {str(e)}")


def _is_library_installed(library_name):
    try:
        importlib.import_module(library_name)
        return True
    except ImportError:
        return False


def _instrument_django(app):
    if _is_library_installed('django'):
        from opentelemetry.instrumentation.django import DjangoInstrumentor
        DjangoInstrumentor().instrument()


def _instrument_fastapi(app):
    if _is_library_installed('fastapi'):
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        FastAPIInstrumentor.instrument_app(app)


def _instrument_flask(app):
    if _is_library_installed('flask'):
        from opentelemetry.instrumentation.flask import FlaskInstrumentor
        FlaskInstrumentor().instrument_app(app)


def _instrument_mysql(app):
    if _is_library_installed('pymysql'):
        from opentelemetry.instrumentation.mysql import MySQLInstrumentor
        MySQLInstrumentor().instrument()


def _instrument_elasticsearch(app):
    if _is_library_installed('elasticsearch'):
        from opentelemetry.instrumentation.elasticsearch import ElasticsearchInstrumentor
        ElasticsearchInstrumentor().instrument()


def _instrument_requests(app):
    if _is_library_installed('requests'):
        from opentelemetry.instrumentation.requests import RequestsInstrumentor
        RequestsInstrumentor().instrument()
