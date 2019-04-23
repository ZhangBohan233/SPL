import spl_ast as ast
import spl_token_lib as stl

ABSTRACT_IDENTIFIER = {"function", "def", "class"}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        """
        Parses the list of tokens stored in this Lexer, and returns the root node of the parsed abstract syntax
        tree.

        :return: the parsed block
        """
        parser = ast.AbstractSyntaxTree()
        i = 0
        func_count = 0
        par_count = 0  # count of parenthesis
        square_count = 0  # count of square bracket
        # get_count = 0  # count of getitem
        cond_nest_list = []
        call_nest_list = []
        param_nest_list = []
        square_nest_list = []
        # get_nest_list = []
        is_abstract = False
        var_level = ast.ASSIGN
        brace_count = 0
        class_brace = -1
        extra_precedence = 0
        titles = []

        while True:
            try:
                token = self.tokens[i]
                line = (token.line_number(), token.file_name())
                if isinstance(token, stl.IdToken):
                    sym = token.symbol
                    if sym == "if":
                        cond_nest_list.append(par_count)
                        par_count += 1
                        parser.add_if(line)
                        i += 1
                    elif sym == "else":
                        parser.add_else()
                    elif sym == "while":
                        cond_nest_list.append(par_count)
                        par_count += 1
                        parser.add_while(line)
                        i += 1
                    elif sym == "for":
                        cond_nest_list.append(par_count)
                        par_count += 1
                        parser.add_for_loop(line)
                        i += 1
                    elif sym == "return":
                        parser.add_unary(line, "return", 0)
                        # parser.add_return(line)
                    elif sym == "break":
                        parser.add_break(line)
                    elif sym == "continue":
                        parser.add_continue(line)
                    elif sym == "true" or sym == "false":
                        parser.add_bool(line, sym)
                    elif sym == "null":
                        parser.add_null(line)
                    elif sym == "const":
                        var_level = ast.CONST
                    elif sym == "var":
                        var_level = ast.VAR
                    # elif sym == "let":
                    #     var_level = ast.LOCAL
                    elif sym == "@":
                        i += 1
                        next_token: stl.IdToken = self.tokens[i]
                        titles.append(next_token.symbol)
                    elif sym == "{":
                        brace_count += 1
                        last_token = self.tokens[i - 1]
                        if isinstance(last_token, stl.IdToken) and \
                                (last_token.symbol == ")" or  # is a function
                                 last_token.symbol.isidentifier()):  # is a class
                            parser.new_block()
                        else:
                            parser.add_dict()
                    elif sym == "}":
                        brace_count -= 1
                        # parser.build_line()
                        parser.build_block()
                        parser.try_build_func()
                        if brace_count == class_brace:
                            parser.build_class()
                            class_brace = -1
                        next_token = self.tokens[i + 1]
                        if not (isinstance(next_token, stl.IdToken) and next_token.symbol in stl.NO_BUILD_LINE):
                            parser.build_line()
                    elif sym == "(":
                        if i > 0 and is_call(self.tokens[i - 1]):
                            parser.add_call(line)
                            call_nest_list.append(par_count)
                            par_count += 1
                        else:
                            extra_precedence += 1
                    elif sym == ")":
                        if extra_precedence == 0:
                            par_count -= 1
                            if is_this_list(call_nest_list, par_count):
                                # parser.build_expr()
                                parser.build_line()
                                parser.build_call()
                                call_nest_list.pop()
                            elif is_this_list(param_nest_list, par_count) > 0:
                                parser.build_func_params()
                                param_nest_list.pop()
                            elif is_this_list(cond_nest_list, par_count) > 0:
                                parser.build_expr()
                                parser.build_condition()
                                cond_nest_list.pop()
                        else:
                            # if parser.in_expr:
                            extra_precedence -= 1
                    elif sym == "[":
                        if i > 0 and is_call(self.tokens[i - 1]):
                            parser.add_getitem(line)
                        else:
                            square_nest_list.append(square_count)
                            func_name = "list"
                            if i > 0:
                                last_token = self.tokens[i - 1]
                                if isinstance(last_token, stl.IdToken) and last_token.symbol == "~":
                                    func_name = "i_list"
                            parser.add_name(line, func_name)
                            parser.add_call(line)
                        square_count += 1
                    elif sym == "]":
                        square_count -= 1
                        if is_this_list(square_nest_list, square_count):  # end of list creation
                            square_nest_list.pop()
                            parser.build_call()
                        else:
                            parser.build_getitem()
                    elif sym == "=":
                        parser.build_expr()
                        parser.add_assignment(line, var_level, extra_precedence)
                        var_level = ast.ASSIGN
                    elif sym == ",":
                        # parser.build_expr()
                        if len(call_nest_list) > 0 or len(param_nest_list) > 0:
                            parser.build_line()
                        else:
                            parser.build_line()
                    elif sym == ".":
                        parser.add_dot(line, extra_precedence)
                    elif sym == "~":  # a special mark
                        pass
                    elif sym == "function" or sym == "def":
                        func_doc = self.get_doc(i)
                        i += 1
                        f_token: stl.IdToken = self.tokens[i]
                        f_name = f_token.symbol
                        push_back = 1
                        if f_name == "(":
                            func_count += 1
                            push_back = 0
                        elif f_name.isidentifier():
                            parser.add_name(line, f_name)
                            parser.add_assignment(line, ast.FUNC_DEFINE, 0)
                        else:
                            raise stl.ParseException("Illegal function name '{}'".format(f_name))
                        parser.add_function(line, is_abstract, titles.copy(), func_doc)
                        i += push_back
                        param_nest_list.append(par_count)
                        par_count += 1
                        is_abstract = False
                        titles.clear()
                    elif sym == "operator":
                        func_doc = self.get_doc(i)
                        i += 1
                        op_token: stl.IdToken = self.tokens[i]
                        op_name = "__" + stl.BINARY_OPERATORS[op_token.symbol] + "__"
                        parser.add_name(line, op_name)
                        parser.add_assignment(line, ast.FUNC_DEFINE, 0)
                        parser.add_function(line, False, titles.copy(), func_doc)
                        param_nest_list.append(par_count)
                        par_count += 1
                        titles.clear()
                        i += 1
                    elif sym == "class":
                        class_doc = self.get_doc(i)
                        i += 1
                        c_token: stl.IdToken = self.tokens[i]
                        class_name = c_token.symbol
                        if class_name in stl.NO_CLASS_NAME:
                            raise stl.ParseException("Name '{}' is forbidden for class name".format(class_name))
                        parser.add_class(
                            (c_token.line_number(), c_token.file_name()),
                            class_name,
                            is_abstract,
                            class_doc
                        )
                        class_brace = brace_count
                        is_abstract = False
                    elif sym == "extends":
                        i += 1
                        cla = parser.get_current_class()
                        while True:
                            c_token = self.tokens[i]
                            superclass_name = c_token.symbol
                            parser.add_extends(superclass_name, cla)
                            next_token = self.tokens[i + 1]
                            if isinstance(next_token, stl.IdToken) and next_token.symbol == ",":
                                i += 2
                            else:
                                break
                    elif sym == "abstract":
                        next_token = self.tokens[i + 1]
                        if isinstance(next_token, stl.IdToken) and next_token.symbol in ABSTRACT_IDENTIFIER:
                            is_abstract = True
                        else:
                            raise stl.ParseException("Unexpected token 'abstract', in file '{}', at line {}"
                                                     .format(line[1], line[0]))
                            # parser.add_abstract(line)
                    elif sym == "new":
                        i += 1
                        c_token = self.tokens[i]
                        class_name = c_token.symbol
                        parser.add_class_new((c_token.line_number(), c_token.file_name()), class_name)
                    elif sym == "throw":
                        parser.add_unary(line, "throw", 0)
                        # parser.add_throw(line)
                    elif sym == "try":
                        parser.add_try(line)
                    elif sym == "catch":
                        parser.add_catch(line)
                        i += 1
                        cond_nest_list.append(par_count)
                        par_count += 1
                    elif sym == "finally":
                        parser.add_finally(line)
                    elif sym == "assert":
                        parser.add_unary(line, "assert", 0)
                    elif sym == "++" or sym == "--":
                        parser.add_increment_decrement(line, sym, extra_precedence)
                    elif sym in stl.TERNARY_OPERATORS and \
                            (parser.is_in_ternary() or stl.TERNARY_OPERATORS[sym]):
                        # This check should go strictly before the check of binary ops
                        if parser.is_in_ternary():
                            parser.finish_ternary(line, sym)
                        else:
                            parser.add_ternary(line, sym, extra_precedence)
                    elif sym in stl.BINARY_OPERATORS:
                        if sym == "-" and (i == 0 or is_unary(self.tokens[i - 1])):
                            parser.add_unary(line, "neg", extra_precedence)
                        elif sym == "*" and (i == 0 or is_unary(self.tokens[i - 1])):
                            next_token = self.tokens[i + 1]
                            if isinstance(next_token, stl.IdToken) and next_token.symbol == "*":
                                parser.add_unary(line, "kw_unpack", 0)
                                i += 1
                            else:
                                parser.add_unary(line, "unpack", 0)
                        else:
                            parser.add_operator(line, sym, extra_precedence)
                    elif sym in stl.UNARY_OPERATORS:
                        if sym == "!" or sym == "not":
                            parser.add_unary(line, "!", extra_precedence)
                        else:
                            print("Should not be here")
                    elif sym[:-1] in stl.OP_EQ:
                        parser.add_operator(line, sym, extra_precedence, True)
                    elif sym == ":":
                        parser.build_expr()
                        parser.add_type(line)
                    elif token.is_eol():
                        if var_level != ast.ASSIGN:
                            active = parser.get_active()
                            und_vars = active.stack.copy()
                            # print(und_vars)
                            active.stack.clear()
                            for node in und_vars:
                                active.stack.append(node)
                                parser.add_assignment(line, var_level, extra_precedence)
                                parser.add_undefined(line)
                                parser.build_line()
                            var_level = ast.ASSIGN
                        parser.build_line()
                    else:
                        parser.add_name(line, sym)
                        # auth = stl.PUBLIC

                elif isinstance(token, stl.NumToken):
                    value = token.value
                    parser.add_number(line, value)
                elif isinstance(token, stl.LiteralToken):
                    value = token.text
                    parser.add_literal(line, value)
                elif isinstance(token, stl.DocToken):
                    pass
                elif token.is_eof():
                    parser.build_line()
                    break
                else:
                    stl.unexpected_token(token)
                i += 1
            except stl.ParseException as e:
                raise e
            except Exception:
                raise stl.ParseException("Parse error in '{}', at line {}".format(self.tokens[i].file_name(),
                                                                                  self.tokens[i].line_number()))

        if par_count != 0 or len(call_nest_list) != 0 or len(cond_nest_list) != 0 or len(param_nest_list) or \
                len(square_nest_list) != 0 or brace_count != 0 or extra_precedence != 0:
            raise stl.ParseEOFException(
                "Reach the end while parsing, {},{},{},{}".format(par_count, call_nest_list,
                                                                  cond_nest_list, param_nest_list))
        return parser.get_as_block()

    def get_doc(self, index):
        if index > 0:
            doc_token = self.tokens[index - 1]
            if isinstance(doc_token, stl.DocToken):
                return doc_token.text
        return ""


def is_call(last_token: stl.Token) -> bool:
    if last_token.is_identifier():
        last_token: stl.IdToken
        if last_token.symbol.isidentifier() or \
                last_token.symbol == "." or \
                last_token.symbol == ")" or \
                last_token.symbol == "]":
            return True
    return False


def is_this_list(lst: list, count: int) -> bool:
    """
    Returns true iff the list is not empty and the last item of the list equals the 'count'

    :param lst:
    :param count:
    :return:
    """
    return len(lst) > 0 and lst[-1] == count


def is_unary(last_token):
    """
    Returns True iff this should be an unary operator.
    False if it should be a minus operator.

    :param last_token:
    :type last_token: Token
    :return:
    :rtype: bool
    """
    if isinstance(last_token, stl.IdToken):
        if last_token.is_eol():
            return True
        else:
            sym = last_token.symbol
            if sym in stl.BINARY_OPERATORS:
                return True
            elif sym in stl.SYMBOLS:
                return True
            elif sym == "(":
                return True
            elif sym == "=":
                return True
            elif sym in stl.RESERVED:
                return True
            else:
                return False
    elif isinstance(last_token, stl.NumToken):
        return False
    else:
        return True
