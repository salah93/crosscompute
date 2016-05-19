import json
from bs4 import BeautifulSoup
from crosscompute.types import get_data_type_by_suffix
from crosscompute.scripts import (
    load_tool_definition, prepare_result_response_folder, run_script)
from crosscompute.scripts.serve import get_app
from urlparse import urlparse as parse_url
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse


DATA_FOLDER = '/tmp/crosscompute/tests'


def run(tool_name, result_arguments=None):
    target_folder = prepare_result_response_folder(DATA_FOLDER)[1]
    tool_definition = load_tool_definition(tool_name)
    return run_script(
        target_folder, tool_definition, result_arguments or {},
        get_data_type_by_suffix())


def serve(tool_name, result_arguments=None):
    response, client = _prepare_response(tool_name, result_arguments)
    assert response.status_code == 303
    result_url = parse_url(dict(response.headers)['Location']).path
    with client.get(result_url) as response:
        soup = BeautifulSoup(response.data, 'lxml')
    return soup, client


def serve_bad_request(tool_name, result_arguments=None):
    response, client = _prepare_response(tool_name, result_arguments)
    assert response.status_code == 400
    return json.loads(response.data)


def _prepare_response(tool_name, result_arguments):
    tool_definition = load_tool_definition(tool_name)
    app = get_app(tool_definition, DATA_FOLDER)
    client = Client(app, BaseResponse)
    with client.post('/t/1', data=result_arguments or {}) as response:
        return response, client