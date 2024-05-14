import importlib
import logging


def instrument_dependencies(app):
    instrument_functions = [
        _instrument_django,
        _instrument_fastapi,
        _instrument_flask,
        _instrument_mysql,
        _instrument_elasticsearch
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
    from opentelemetry.instrumentation.django import DjangoInstrumentor
    DjangoInstrumentor().instrument()


def _instrument_fastapi(app):
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    FastAPIInstrumentor.instrument_app(app)


def _instrument_flask(app):
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    FlaskInstrumentor().instrument_app(app)


def _instrument_mysql(app):
    from opentelemetry.instrumentation.mysql import MySQLInstrumentor
    MySQLInstrumentor().instrument()


def _instrument_elasticsearch(app):
    from opentelemetry.instrumentation.elasticsearch import ElasticsearchInstrumentor
    ElasticsearchInstrumentor().instrument()
