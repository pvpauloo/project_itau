# coding=utf-8
import logging
import sys

import json_logging
import json_logging.framework
from json_logging import JSONLogWebFormatter
from json_logging.framework_base import AppRequestInstrumentationConfigurator, RequestAdapter, ResponseAdapter


def is_flask_present():
    # noinspection PyPep8,PyBroadException
    try:
        import flask
        return True
    except:
        return False


if is_flask_present():
    from flask import request as request_obj
    import flask as flask

    _current_request = request_obj
    _flask = flask


class FlaskAppRequestInstrumentationConfigurator(AppRequestInstrumentationConfigurator):
    def config(self, app):
        if not is_flask_present():
            raise RuntimeError("flask is not available in system runtime")
        from flask.app import Flask
        if not isinstance(app, Flask):
            raise RuntimeError("app is not a valid flask.app.Flask app instance")

        # Disable standard logging
        logging.getLogger('werkzeug').disabled = True

        json_logging.util.use_cf_logging_formatter([logging.getLogger('werkzeug')], JSONLogWebFormatter)

        # noinspection PyAttributeOutsideInit
        self.request_logger = logging.getLogger('flask-request-logger')
        self.request_logger.setLevel(logging.DEBUG)
        self.request_logger.addHandler(logging.FileHandler(filename='json.log'))

        from flask import g

        @app.before_request
        def before_request():
            g.request_info = json_logging.RequestInfo(_current_request)

        @app.after_request
        def after_request(response):
            request_info = g.request_info
            request_info.update_response_status(response)
            # TODO:handle to print out request instrumentation in non-JSON mode
            self.request_logger.info("", extra={'request_info': request_info})
            return response


class FlaskRequestAdapter(RequestAdapter):
    @staticmethod
    def get_request_class_type():
        raise NotImplementedError

    @staticmethod
    def support_global_request_object():
        return True

    @staticmethod
    def get_current_request():
        return _current_request

    def get_remote_user(self, request):
        if request.authorization is not None:
            return request.authorization.username
        else:
            return json_logging.EMPTY_VALUE

    def is_in_request_context(self, request_):
        return _flask.has_request_context()

    def get_http_header(self, request, header_name, default=None):
        if header_name in request.headers:
            return request.headers.get(header_name)
        return default

    def set_correlation_id(self, request_, value):
        _flask.g.correlation_id = value

    def get_correlation_id_in_request_context(self, request):
        return _flask.g.get('correlation_id', None)

    def get_protocol(self, request):
        return request.environ.get('SERVER_PROTOCOL')

    def get_path(self, request):
        return request.path

    def get_content_length(self, request):
        return request.content_length

    def get_method(self, request):
        return request.method

    def get_remote_ip(self, request):
        return request.remote_addr

    def get_remote_port(self, request):
        return request.environ.get('REMOTE_PORT')


class FlaskResponseAdapter(ResponseAdapter):
    def get_status_code(self, response):
        return response.status_code

    def get_response_size(self, response):
        return response.calculate_content_length()

    def get_content_type(self, response):
        return response.content_type
