from pyparsing import *

from ast.ast import AST


class Parser():

    def __init__(self, debug = 0):
        self.debug = debug
        self.ast = AST(debug)
        self.files = []

        LPAR, RPAR, LBRACK, RBRACK, LBRACE, RBRACE, SEMI, COMMA = map(Suppress, "()[]{};,")

        QUOTE = Suppress('"')

        PLUS = Keyword("+")
        MINUS = Keyword("-")

        NOT = Suppress("!")

        INT = Keyword("int")
        BOOL = Keyword("bool")
        WHILE = Keyword("while")
        IF = Keyword("if")
        ELSE = Keyword("else")
        VOID = Keyword("void")

        RETURN = Keyword("return")
        TRUE = Keyword("true")
        FALSE = Keyword("false")
        INCLUDE = Keyword("#include")

        name = Word(alphas + "_", alphanums + "_").setParseAction(self.ast.parse_word)
        filename = Word(alphanums + "." + alphanums)
        integer = (Regex(r"[+-]?\d+")).setParseAction(self.ast.parse_int)
        boolean = (TRUE | FALSE).setParseAction(self.ast.parse_bool)
        types = (INT | BOOL).setParseAction(self.ast.parse_type)

        statements = Forward()
        statement = Forward()
        expression = Forward()

        variable = (name("var") + Optional(LBRACK - expression - RBRACK)).setParseAction(self.ast.parse_variable)
        variable_statement = (types - variable - SEMI)

        if_statement = (IF - LPAR - expression - RPAR - statement - Optional(ELSE - statement))
        while_statement = (WHILE - LPAR - expression - RPAR - statement)
        return_statement = (RETURN - Optional(expression) - SEMI)

        relop = oneOf("== != > < <= >= =")
        addop = oneOf("+ - ||")
        mulop = oneOf("* / % &&")

        factor = Forward()
        factor << Group(
            integer
            | boolean
            | (NOT + factor).setParseAction(self.ast.parse_not)
            | (variable + Optional("(" + Optional(delimitedList(expression)) - ")")).setParseAction(self.ast.parse_call)
            | LPAR - expression - RPAR)
        term = (factor + ZeroOrMore(mulop + factor)).setParseAction(self.ast.parse_term)
        simple_expression = (Optional(PLUS | MINUS) + term + ZeroOrMore(addop - term)).setParseAction(self.ast.parse_simple_expression)
        expression << (simple_expression + ZeroOrMore(relop + simple_expression)).setParseAction(self.ast.parse_expression)

        statement << Group(
            if_statement.setParseAction(self.ast.parse_if_statement)
            | while_statement.setParseAction(self.ast.parse_while_statement)
            | return_statement.setParseAction(self.ast.parse_return_statement)
            | (LBRACE + statements + RBRACE).setParseAction(self.ast.parse_compound_statement)
            | variable_statement.setParseAction(self.ast.parse_variable_statement)
            | expression + SEMI)

        statements << (ZeroOrMore(statement)).setParseAction(self.ast.parse_statements)

        param = (types - variable).setParseAction(self.ast.parse_variable_statement)
        params = delimitedList(param)
        fundecl = ((types | VOID).setParseAction(self.ast.parse_type) - name - LPAR + Optional(params).setParseAction(
            self.ast.parse_params) - RPAR - LBRACE - statements - RBRACE).setParseAction(self.ast.parse_function)

        includes = (INCLUDE - QUOTE - filename - QUOTE).setParseAction(self.__parse_include)
        self.program = ZeroOrMore(includes) - ZeroOrMore(fundecl).setParseAction(self.ast.parse_program)

    def __parse_include(self, text, loc, args):

        if self.debug > 0:
            print "Include:", args

        filename = args[1]

        if filename in self.files:
            raise Exception(filename + " has already been included")

        self.files.append(filename)
        self.parse_file(filename)

    def parse_file(self, data_file):
        self.files = self.files.append(data_file)
        self.program.ignore(cStyleComment).parseFile(data_file, parseAll=True)

    def parse_text(self, text):
        self.program.ignore(cStyleComment).parseString(text, parseAll=True)

    def get_ast(self):
        return self.ast
