# -*- coding: utf-8 -*-
from pytest import mark

from storyscript.ErrorCodes import ErrorCodes


@mark.parametrize('name, definition', [
    ('unidentified_error', ('E0001', '')),
    ('service_name', ('E0002', "A service name can't contain `.`")),
    ('arguments_noservice', (
        'E0003', 'Unefined argument; not a service'
    )),
    ('return_outside', ('E0004', '`return` is allowed only inside functions')),
    ('variables_backslash', ('E0005', "A variable name can't contain `/`")),
    ('variables_dash', ('E0006', "A variable name can't contain `-`")),
    ('assignment_incomplete', ('E0007', 'Missing value after `=`')),
    ('function_misspell', ('E0008', 'Misspelt `function`')),
    ('import_misspell', ('E0009', 'Misspelt `import`')),
    ('import_misspell_as', ('E0010',
                            'Misspelt `as` in an import statement'')),
    ('import_unquoted_file', ('E0011',
                              'The imported filename must be in quotes')),
    ('string_opening_quote', ('E0012', 'Missing opening quote for string')),
    ('string_closing_quote', ('E0013', 'Missing closing quote for string')),
    ('list_trailing_comma', ('E0014', 'Trailing comma in list')),
    ('list_opening_bracket', ('E0015', 'Missing opening bracket for list')),
    ('list_closing_bracket', ('E0016', 'Missing closing bracket for list')),
    ('object_opening_bracket',  (
        'E0017', 'Missing opening bracket for object'
    )),
    ('object_closing_bracket', ('E0018',
                                'Missing closing bracket for object')),
    ('service_argument_colon', ('E0019', 'Missing colon in service argument')),
    ('reserved_keyword', ('E0020', '`{keyword}` is a reserved keyword')),
    ('future_reserved_keyword',
        ('E0030', '`{keyword}` is reserved for future use')),
])
def test_errorcodes_errors(name, definition):
    assert getattr(ErrorCodes, name) == definition


def test_errorcodes_is_error():
    """
    Ensures that is_errror can find out whether an error name is valid.
    """
    assert ErrorCodes.is_error('service_name') is True


def test_errorcodes_is_error_none():
    assert ErrorCodes.is_error(None) is None


def test_errorcodes_is_error_string():
    assert ErrorCodes.is_error('foo') is None


def test_errorcodes_get_error():
    ErrorCodes.mock = 'value'
    assert ErrorCodes.get_error('mock') == 'value'
