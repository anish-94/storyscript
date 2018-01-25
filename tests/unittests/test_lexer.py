import os

from ply import lex

from storyscript.lexer import Lexer


def test_lexer_init(mocker):
    mocker.patch.object(Lexer, 'build')
    Lexer()
    Lexer.build.assert_called_with(optimize=True)


def test_lexer_build(mocker):
    mocker.patch.object(os, 'getcwd')
    mocker.patch.object(Lexer, '__init__', return_value=None)
    mocker.patch.object(lex, 'lex')
    lexer = Lexer()
    lexer.build()
    lex.lex.assert_called_with(object=lexer, outputdir=os.getcwd())
    assert lexer.lexer == lex.lex()
    assert lexer.lexer.filename is None
    assert lexer.token_stream is None