import pytest

from openapi_tester.exceptions import DocumentationError
from openapi_tester.schema_tester import SchemaTester
from tests.types import (
    bool_data,
    bool_type,
    integer_data,
    integer_type,
    list_data,
    list_type,
    number_data,
    number_type,
    string_data,
    string_type,
)

tester = SchemaTester({'type': 'array', 'items': {'type': 'object', 'properties': {}}}, [], None)


def test_valid_list() -> None:
    """
    Asserts that valid data passes successfully.
    """
    tester.test_schema_section(schema=list_type, data=list_data, reference='placeholder')


def test_bad_data_type() -> None:
    """
    Asserts that the appropriate exception is raised for a bad response data type.
    """
    with pytest.raises(DocumentationError, match='Mismatched types, expected list but received dict.'):
        tester.test_schema_section(schema=list_type, data={'test': list_data}, reference='placeholder')


def test_empty_schema_list() -> None:
    with pytest.raises(
        DocumentationError, match='Mismatched content. Response array contains data, when schema is empty.'
    ):
        list_schema = {'title': 'list_type_title', 'type': 'array', 'items': {}}  # empty list
        tester.test_schema_section(schema=list_schema, data=list_data, reference='placeholder')


def test_empty_response_data_list() -> None:
    """
    Asserts that the no exception is raised when the response data is missing - this has valid cases.
    """
    tester.test_schema_section(schema=list_type, data=[], reference='placeholder')


def test_call_list_from_list():
    """
    Verify that we're able to call _list from _list successfully.
    """
    custom_list = {
        'title': 'list_type_title',
        'type': 'array',
        'items': {
            'title': 'list_type_title',
            'type': 'array',
            'items': {
                'title': 'object_type_title',
                'type': 'object',
                'properties': {
                    'string': string_type,
                    'integer': integer_type,
                    'number': number_type,
                    'bool': bool_type,
                },
            },
        },
    }
    custom_data = [[{'string': string_data, 'integer': integer_data, 'number': number_data, 'bool': bool_data}]]
    assert tester.test_schema_section(schema=custom_list, data=custom_data, reference='placeholder') is None


def test_call_item_from_list():
    """
    Verify that we're able to call _list from _list successfully.
    """
    for type_schema in [
        (string_type, string_data),
        (bool_type, bool_data),
        (number_type, number_data),
        (integer_type, integer_data),
    ]:
        custom_list = {'title': 'list_type_title', 'type': 'array', 'items': type_schema[0]}
        custom_data = [type_schema[1]]
        assert tester.test_schema_section(schema=custom_list, data=custom_data, reference='placeholder') is None