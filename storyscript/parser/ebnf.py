# -*- coding: utf-8 -*-


class Ebnf:
    """
    Advanced EBNF grammar generator that provides for a readable, nicer and
    testable way of creating a grammar.

    A grammar is made by rules and rules are made by combinations of tokens.
    Tokens can be literals or regular expressions.

    Tokens can also be imported from an available grammar, or ignored
    completely, meaning they will not appear in the parsed tree.
    """

    def __init__(self):
        self._tokens = {}
        self._rules = {}
        self.imports = {}
        self.ignores = []

    def macro(self, name, template):
        """
        Creates a macro with the given name, by creating a method on the
        instance
        """
        def compile_macro(rule):
            return template.format(rule)
        setattr(self, name, compile_macro)

    def set_token(self, name, value):
        """
        Registers a token under a simplified name, and keep the original name,
        the value and the real token
        """
        token = name.split('.')[0]
        token_name = token.lower()
        if token_name.startswith('_'):
            token_name = token_name[1:]

        token_value = '"{}"'.format(value)
        if len(value) > 2:
            if value.startswith('/'):
                if value.endswith('/'):
                    token_value = value
        dictionary = {'name': name, 'value': token_value, 'token': token}
        self._tokens[token_name] = dictionary

    def resolve(self, name):
        """
        Resolves a name to its real value if it's a token, or leave it as it
        is.
        """
        clean_name = name.strip('*[]()?')
        if clean_name in self._tokens:
            real_name = self._tokens[clean_name]['token']
        else:
            real_name = clean_name
        return name.replace(clean_name, real_name)

    def set_rule(self, name, value):
        """
        Registers a rule, transforming tokens to their identifiers.
        """
        rule = ''
        for shard in value.split():
            rule = '{} {}'.format(rule, self.resolve(shard))
        self._rules[name] = rule.strip()

    def ignore(self, terminal):
        self.ignores.append('%ignore {}'.format(terminal))

    def load(self, token):
        self.imports[token] = '%import common.{}'.format(token.upper())

    def build_tokens(self):
        string = ''
        for name, token in self._tokens.items():
            string += '{}: {}\n'.format(token[0], token[1])
        return string

    def build_rules(self):
        string = ''
        for name, definitions in self._rules.items():
            string += '{}: {}\n'.format(name, '\n\t| '.join(definitions))
        return string

    def build(self):
        tokens = self.build_tokens()
        rules = self.build_rules()
        ignores = '\n'.join(self.ignores)
        imports = '\n'.join(self.imports.values())
        args = (self.start_line, rules, tokens, ignores, imports)
        return '{}\n{}\n{}\n{}\n\n{}'.format(*args)

    def __setattr__(self, name, value):
        if isinstance(value, str):
            if name.isupper():
                return self.set_token(name, value)
            return self.set_rule(name, value)
        object.__setattr__(self, name, value)
