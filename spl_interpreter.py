import spl_memory as mem
import spl_ast as ast
import spl_lexer as lex
import spl_parser as psr
import spl_token_lib as stl
import spl_lib as lib
import multiprocessing
from environment import Environment, GlobalEnvironment, LoopEnvironment, SubEnvironment, \
    FunctionEnvironment, ClassEnvironment

LST = [72, 97, 112, 112, 121, 32, 66, 105, 114, 116, 104, 100, 97, 121, 32,
       73, 115, 97, 98, 101, 108, 108, 97, 33, 33, 33]

LINE_FILE = 0, "interpreter"
INVALID = lib.InvalidArgument()
UNPACK_ARGUMENT = lib.UnpackArgument()
KW_UNPACK_ARGUMENT = lib.KwUnpackArgument()

PRIMITIVE_TYPE_TABLE = {
    "boolean": "bool",
    "void": "NoneType"
}


class Interpreter:
    """
    A spl interpreter entry object.

    This class is used to create an spl evaluator, which is mostly used to interpret the root 'BlockStmt' of
    a program.
    """

    def __init__(self, argv: list, encoding: str):
        # mem.start()
        self.ast = None
        self.argv = argv
        self.encoding = encoding
        self.env = GlobalEnvironment()
        self.env.scope_name = "Global"
        self.set_up_env()

    def set_up_env(self):
        """
        Sets up the global environment.

        :return:
        """
        add_natives(self.env)
        # obj = lib.SplObject()
        system = lib.System(lib.List(*parse_args(self.argv)), self.encoding)
        natives = NativeInvokes()
        os_ = lib.Os()
        self.env.add_heap("Object", Class("Object", None, True))
        self.env.add_heap("system", system)
        self.env.add_heap("natives", natives)
        self.env.add_heap("os", os_)

    def set_ast(self, ast_: ast.BlockStmt):
        """
        Sets up the abstract syntax tree to be interpreted.

        :param ast_: the root of the abstract syntax tree to be interpreted
        :return: None
        """
        self.ast = ast_

    def interpret(self):
        """
        Starts the interpretation.

        :return: the exit value
        """
        return evaluate(self.ast, self.env)


def parse_args(argv):
    """

    :param argv: the system argv
    :return: the argv in spl String object
    """
    return [lib.String(x) for x in argv]


def add_natives(self):
    """
    Adds a bundle of global variables to the global scope.

    Includes all built-in functions and some global vars.

    :param self: the Environment
    :return: None
    """
    self.add_heap("print", NativeFunction(lib.print_, "print"))
    self.add_heap("println", NativeFunction(lib.print_ln, "println"))
    self.add_heap("type", NativeFunction(typeof, "type"))
    self.add_heap("pair", NativeFunction(lib.make_pair, "pair"))
    self.add_heap("list", NativeFunction(lib.make_list, "list"))
    self.add_heap("set", NativeFunction(lib.make_set, "set"))
    self.add_heap("int", NativeFunction(lib.to_int, "int"))
    self.add_heap("float", NativeFunction(lib.to_float, "float"))
    self.add_heap("string", NativeFunction(to_str, "string"))
    self.add_heap("repr", NativeFunction(to_repr, "repr"))
    self.add_heap("input", NativeFunction(lib.input_, "input"))
    self.add_heap("f_open", NativeFunction(lib.f_open, "f_open"))
    self.add_heap("eval", NativeFunction(eval_, "eval"))
    self.add_heap("dir", NativeFunction(dir_, "dir", self))
    self.add_heap("getcwf", NativeFunction(getcwf, "getcwf", self))
    self.add_heap("main", NativeFunction(is_main, "main", self))
    self.add_heap("exit", NativeFunction(lib.exit_, "exit"))
    self.add_heap("help", NativeFunction(help_, "help", self))

    # type of built-in
    self.add_heap("boolean", NativeFunction(lib.to_boolean, "boolean"))
    self.add_heap("void", NativeFunction(None, "void"))

    # global variables
    self.add_heap("cwf", None)


class NativeFunction:
    def __init__(self, func: callable, name: str, env: Environment = None):
        self.name = name
        self.function = func
        self.parent_env: Environment = env

    def __str__(self):
        try:
            return "NativeFunction {}".format(self.function.__name__)
        except AttributeError:
            return ""

    def __repr__(self):
        return self.__str__()

    def call(self, args, kwargs):
        if self.parent_env:
            if len(kwargs) > 0:
                return self.function(self.parent_env, *args, kwargs)
            else:
                return self.function(self.parent_env, *args)
        else:
            if len(kwargs) > 0:
                return self.function(*args, kwargs)
            else:
                return self.function(*args)


class ParameterPair:
    def __init__(self, name: str, preset):
        self.name: str = name
        self.preset = preset

    def __str__(self):
        return "{}={}".format(self.name, self.preset)

    def __repr__(self):
        return self.__str__()


class Function:
    """
    :type body: BlockStmt
    :type outer_scope: Environment
    """

    def __init__(self, params, body, outer, abstract: bool, options: dict):
        # self.name = f_name
        self.params: [ParameterPair] = params
        self.options = options
        # self.presets: list = presets
        self.body = body
        self.outer_scope = outer
        self.abstract = abstract
        self.file = None
        self.line_num = None

    def __str__(self):
        return "Function<{}>".format(id(self))

    def __repr__(self):
        return self.__str__()


class Class:
    def __init__(self, class_name: str, body: ast.BlockStmt, abstract: bool):
        self.class_name = class_name
        self.body = body
        self.superclass_names = []
        self.outer_env = None
        self.abstract = abstract
        self.line_num = None
        self.file = None

    def __str__(self):
        if len(self.superclass_names):
            return "Class<{}> extends {}".format(self.class_name, self.superclass_names)
        else:
            return "Class<{}>".format(self.class_name)

    def __repr__(self):
        return self.__str__()


class Undefined:
    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, Undefined)

    def __str__(self):
        return "undefined"

    def __repr__(self):
        return self.__str__()


class Thread(lib.NativeType):
    def __init__(self, process):
        lib.NativeType.__init__(self)

        self.process: multiprocessing.Process = process
        self.daemon = False

    def type_name(self):
        return "thread"

    def set_daemon(self, d):
        self.daemon = d

    def start(self):
        self.process.daemon = self.daemon
        self.process.start()

    def alive(self):
        return self.process.is_alive()


class NativeInvokes(lib.NativeType):
    def __init__(self):
        lib.NativeType.__init__(self)

    def type_name(self):
        return "natives"

    def str_join(self, s: lib.String, itr):
        if isinstance(itr, lib.Iterable):
            return lib.String(s.literal.join([x.text() for x in itr]))
        else:
            raise lib.TypeException("Object is not a native-iterable object.")

    def thread(self, env: Environment, target: Function, name: str, args: lib.List):
        call = ast.FuncCall(LINE_FILE, name)
        call.args = ast.BlockStmt(LINE_FILE)
        for x in args.list:
            call.args.lines.append(x)

        process = multiprocessing.Process(target=call_function, args=(call, target, target.outer_scope, env))
        return Thread(process)


UNDEFINED = Undefined()


class ClassInstance(lib.SplObject):
    def __init__(self, env: Environment, class_name: str):
        """
        ===== Attributes =====
        :param class_name: name of this class
        :param env: instance attributes
        """
        lib.SplObject.__init__(self)
        self.class_name = class_name
        self.env = env
        self.env.constants["this"] = self

    def __getitem__(self, item):
        if self.env.contains_key("__getitem__"):
            call = ast.FuncCall(LINE_FILE, "__getitem__")
            call.args = ast.BlockStmt(LINE_FILE)
            call.args.add_line(item)
            return evaluate(call, self.env)
        else:
            raise lib.SplException("{} object does not support indexing".format(self.class_name))

    def __hash__(self):
        if self.env.contains_key("__hash__"):
            call = ast.FuncCall(LINE_FILE, "__hash__")
            call.args = ast.BlockStmt(LINE_FILE)
            return evaluate(call, self.env)
        else:
            raise lib.SplException("{} object is not hashable".format(self.class_name))

    def __neg__(self):
        if self.env.contains_key("__neg__"):
            call = ast.FuncCall(LINE_FILE, "__neg__")
            call.args = ast.BlockStmt(LINE_FILE)
            return evaluate(call, self.env)
        else:
            raise lib.SplException("{} object has no neg attribute".format(self.class_name))

    def __repr__(self):
        if self.env.contains_key("__repr__"):
            return to_repr(self).literal
        else:
            return "<{} at {}>".format(self.class_name, self.id)

    def __setitem__(self, item):
        if self.env.contains_key("__setitem__"):
            call = ast.FuncCall(LINE_FILE, "__setitem__")
            call.args = ast.BlockStmt(LINE_FILE)
            call.args.add_line(item)
            return evaluate(call, self.env)
        else:
            raise lib.SplException("{} object does not support indexing".format(self.class_name))

    def __str__(self):
        if self.env.contains_key("__str__"):
            return to_str(self).literal
        else:
            attr = self.env.attributes()
            attr.pop("this")
            attr.pop("=>")
            return "<{} at {}>: {}".format(self.class_name, self.id, attr)


class RuntimeException(Exception):
    def __init__(self, exception: ClassInstance):
        Exception.__init__(self, "RuntimeException")

        self.exception = exception

    def __str__(self):
        return self.exception.__str__()


# Native functions with dependencies

def to_str(v) -> lib.String:
    if isinstance(v, ClassInstance):
        fc: ast.FuncCall = ast.FuncCall(LINE_FILE, "__str__")
        block: ast.BlockStmt = ast.BlockStmt(LINE_FILE)
        fc.args = block
        func: Function = v.env.get("__str__", LINE_FILE)
        result: lib.String = call_function(fc, func, v.env, None)
        return result
    else:
        return lib.String(v)


def to_repr(v) -> lib.String:
    if isinstance(v, ClassInstance):
        fc: ast.FuncCall = ast.FuncCall(LINE_FILE, "__repr__")
        block: ast.BlockStmt = ast.BlockStmt(LINE_FILE)
        fc.args = block
        func: Function = v.env.get("__repr__", LINE_FILE)
        result: lib.String = call_function(fc, func, v.env, None)
        return result
    else:
        return lib.String(v)


def typeof(obj) -> lib.String:
    if obj is None:
        return lib.String("void")
    elif isinstance(obj, ClassInstance):
        return lib.String(obj.class_name)
    elif isinstance(obj, bool):
        return lib.String("boolean")
    elif isinstance(obj, lib.NativeType):
        return lib.String(obj.type_name())
    else:
        t = type(obj)
        return lib.String(t.__name__)


def eval_(expr: lib.String):
    lexer = lex.Tokenizer()
    lexer.file_name = "expression"
    lexer.script_dir = "expression"
    lexer.tokenize([expr.text()])
    parser = psr.Parser(lexer.get_tokens())
    block = parser.parse()
    return block


def dir_(env, obj):
    """
    Returns a List containing all attributes of a type or an object.

    :param env:
    :param obj:
    :return:
    """
    lst = lib.List()
    if isinstance(obj, Class):
        # instance = inter.ClassInstance(env, obj.class_name)
        create = ast.ClassInit((0, "dir"), obj.class_name)
        instance: ClassInstance = evaluate(create, env)
        exc = {"=>", "this"}
        # for attr in instance.env.variables:
        for attr in instance.env.attributes():
            if attr not in exc:
                lst.append(attr)
        mem.MEMORY.free_last()
        # del instance
        # mem.MEMORY.free()
    elif isinstance(obj, NativeFunction):
        for nt in lib.NativeType.__subclasses__():
            if nt.type_name(nt) == obj.name:
                lst.extend(dir(nt))
    elif isinstance(obj, lib.NativeType):
        for nt in lib.NativeType.__subclasses__():
            if nt.type_name(nt) == obj.type_name():
                lst.extend(dir(nt))
    lst.sort()
    return lst


def getcwf(env: Environment):
    return lib.String(env.get_heap("cwf"))


def is_main(env: Environment):
    return env.get_heap("system").argv[0] == getcwf(env)


def help_(env, obj):
    if isinstance(obj, NativeFunction):
        pass
    elif isinstance(obj, Function):
        print(obj)
    elif isinstance(obj, Class):
        cla_self = _get_doc(obj)
        print("Help on class", obj.class_name, "\n")
        title = ["class ", obj.class_name]
        if len(obj.superclass_names) > 0:
            title.append(" extends ")
            for x in obj.superclass_names:
                title.append(x)
                title.append(", ")
            title.pop()
        print("".join(title))
        print(cla_self)
        print("---------- Attributes ----------")

        create = ast.ClassInit((0, "dir"), obj.class_name)
        instance: ClassInstance = evaluate(create, env)
        # do not add to pointer list
        exc = {"this"}
        # for attr in instance.env.variables:
        for attr in instance.env.attributes():
            if attr not in exc:
                print(attr)
                print(_get_doc(instance.env.get(attr, (0, "help"))))
        mem.MEMORY.free_last()
        # del instance
        # mem.MEMORY.decrement()


# Helper functions

def _get_doc(obj):
    if isinstance(obj, Class) or isinstance(obj, Function) or isinstance(obj, ast.Node):
        doc_file = stl.get_doc_name(obj.file)
        try:
            with open(doc_file, "r") as f:
                lines = f.readlines()

            pos = obj.line_num - 1
            result = []
            result.extend(_filter_doc(lines, pos))
            return "".join(result)
        except IOError:
            return "| "
    else:
        return "| " + typeof(obj).literal


def _filter_doc(lines: [str], pos: int):
    """

    :param lines:
    :return:
    """
    lst = []
    in_doc = False
    for i in range(pos - 1, -1, -1):
        line = lines[i]
        if not in_doc:
            if line[0] == "+":
                break
            elif line[0] == "*":
                lst.append("| ")
                lst.append(line[1:])
    return lst


# Interpreter


def eval_for_loop(node: ast.ForLoopStmt, env: Environment):
    con: ast.BlockStmt = node.condition
    start = con.lines[0]
    end = con.lines[1]
    step = con.lines[2]

    title_scope = LoopEnvironment(env)

    block_scope = LoopEnvironment(title_scope)

    result = evaluate(start, title_scope)

    while not title_scope.broken and evaluate(end, title_scope):
        block_scope.invalidate()
        result = evaluate(node.body, block_scope)
        title_scope.resume_loop()
        evaluate(step, title_scope)

    del title_scope
    del block_scope
    return result


def eval_for_each_loop(node: ast.ForLoopStmt, env: Environment):
    con: ast.BlockStmt = node.condition
    inv: ast.Node = con.lines[0]
    lf = node.line_num, node.file

    title_scope = LoopEnvironment(env)

    block_scope = LoopEnvironment(title_scope)

    if inv.node_type == ast.NAME_NODE:
        inv: ast.NameNode
        invariant = inv.name
    elif inv.node_type == ast.ASSIGNMENT_NODE:
        inv: ast.AssignmentNode
        evaluate(inv, title_scope)
        invariant = inv.left.name
    else:
        raise lib.SplException("Unknown type for for-each loop invariant")
    target = con.lines[1]
    # print(target)
    iterable = evaluate(target, title_scope)
    if isinstance(iterable, lib.Iterable):
        result = None
        for x in iterable:
            block_scope.invalidate()
            block_scope.assign(invariant, x, lf)
            result = evaluate(node.body, block_scope)
            title_scope.resume_loop()
            if title_scope.broken:
                break

        del title_scope
        del block_scope
        # env.broken = False
        return result
    elif isinstance(iterable, ClassInstance) and is_subclass_of(title_scope.get_heap(iterable.class_name), "Iterable",
                                                                title_scope):
        ite = ast.FuncCall(lf, "__iter__")
        ite.args = ast.BlockStmt(LINE_FILE)
        iterator: ClassInstance = evaluate(ite, iterable.env)
        result = None
        while not title_scope.broken:
            block_scope.invalidate()
            nex = ast.FuncCall(lf, "__next__")
            nex.args = ast.BlockStmt(LINE_FILE)
            res = evaluate(nex, iterator.env)
            if isinstance(res, ClassInstance) and is_subclass_of(title_scope.get_heap(res.class_name), "StopIteration",
                                                                 title_scope):
                break
            block_scope.assign(invariant, res, lf)
            result = evaluate(node.body, block_scope)
            title_scope.resume_loop()
        # env.broken = False
        del title_scope
        del block_scope
        return result
    else:
        raise lib.SplException(
            "For-each loop on non-iterable objects, in {}, at line {}".format(node.file, node.line_num))


def eval_try_catch(node: ast.TryStmt, env: Environment):
    try:
        block_scope = SubEnvironment(env)
        result = evaluate(node.try_block, block_scope)
        return result
    except RuntimeException as re:  # catches the exceptions thrown by SPL program
        block_scope = SubEnvironment(env)
        exception: ClassInstance = re.exception
        exception_class = block_scope.get_heap(exception.class_name)
        catches = node.catch_blocks
        for cat in catches:  # catch blocks
            block_scope.invalidate()
            for line in cat.condition.lines:
                block_scope.define_var(line.left.name, exception, (line.line_num, line.file))
                catch_name = line.right.name
                if is_subclass_of(exception_class, catch_name, block_scope):
                    result = evaluate(cat.then, block_scope)
                    return result
        raise re
    except Exception as e:  # catches the exceptions raised by python
        block_scope = SubEnvironment(env)
        catches = node.catch_blocks
        for cat in catches:
            block_scope.invalidate()
            for line in cat.condition.lines:
                block_scope.define_var(line.left.name, e, (line.line_num, line.file))
                catch_name = line.right.name
                if catch_name == "Exception":
                    result = evaluate(cat.then, block_scope)
                    return result
        raise e
    finally:
        block_scope = SubEnvironment(env)
        if node.finally_block is not None:
            return evaluate(node.finally_block, block_scope)


def is_subclass_of(child_class: Class, class_name: str, env: Environment) -> bool:
    """
    Returns whether the child class is the ancestor class itself or inherited from that class.

    :param child_class: the child class to be check
    :param class_name: the ancestor class
    :param env: the environment, doesn't matter whether it is global or not
    :return: whether the child class is the ancestor class itself or inherited from that class
    """
    if isinstance(child_class, Class):
        if child_class.class_name == class_name:
            return True
        else:
            return any([is_subclass_of(env.get_heap(ccn), class_name, env) for ccn in child_class.superclass_names])
    else:
        return False


def eval_operator(node: ast.OperatorNode, env: Environment):
    left = evaluate(node.left, env)
    if node.assignment:
        right = evaluate(node.right, env)
        symbol = node.operation[:-1]
        res = arithmetic(left, right, symbol, env)
        asg = ast.AssignmentNode((node.line_num, node.file), False)
        asg.left = node.left
        asg.operation = "="
        asg.right = res
        return evaluate(asg, env)
    else:
        symbol = node.operation
        right_node = node.right
        return arithmetic(left, right_node, symbol, env)


def assignment(node: ast.AssignmentNode, env: Environment):
    key = node.left
    value = evaluate(node.right, env)
    t = key.node_type
    lf = node.line_num, node.file
    # print(key)
    if t == ast.NAME_NODE:
        key: ast.NameNode
        if node.level == ast.ASSIGN:
            env.assign(key.name, value, lf)
        elif node.level == ast.CONST:
            # var_type = generate_var_type(node.var_type, env)
            env.define_const(key.name, value, lf)
        elif node.level == ast.VAR:
            # var_type = generate_var_type(node.var_type, env)
            env.define_var(key.name, value, lf)
        elif node.level == ast.FUNC_DEFINE:
            value: Function
            env.define_function(key.name, value, lf, value.options)
        else:
            raise lib.SplException("Unknown variable level")
        return value
    elif t == ast.DOT:
        if node.level == ast.CONST:
            raise lib.SplException("Unsolved syntax: assigning a constant to an instance")
        node = key
        name_lst = []
        while isinstance(node, ast.Dot):
            name_lst.append(node.right.name)
            node = node.left
        name_lst.append(node.name)
        name_lst.reverse()
        # print(name_lst)
        scope = env
        for t in name_lst[:-1]:
            scope = scope.get(t, (node.line_num, node.file)).env
        scope.assign(name_lst[-1], value, lf)
        return value
    else:
        raise lib.InterpretException("Unknown assignment, in {}, at line {}".format(node.file, node.line_num))


def init_class(node: ast.ClassInit, env: Environment):
    cla: Class = env.get_heap(node.class_name)

    if cla.abstract:
        raise lib.SplException("Abstract class is not instantiable")

    # scope = Environment(CLASS_SCOPE, cla.outer_env)
    scope = ClassEnvironment(cla.outer_env)
    # scope.outer = env
    scope.scope_name = "Class scope<{}>".format(cla.class_name)
    class_inheritance(cla, env, scope)

    # print(scope.variables)
    instance = ClassInstance(scope, node.class_name)
    attrs = scope.attributes()
    for k in attrs:
        v = attrs[k]
        if isinstance(v, Function):
            v.outer_scope = scope

    # if node.args:
    #     print(111)
    #     # constructor: Function = scope.variables[node.class_name]
    #     fc = ast.FuncCall((node.line_num, node.file), node.class_name)
    #     fc.args = node.args
    #     func = scope.get(node.class_name, (node.line_num, node.file))
    #     call_function(fc, func, scope, env)
    # return mem.Pointer(instance.id)
    return instance


def eval_func_call(node: ast.FuncCall, env: Environment):
    lf = node.line_num, node.file
    # func = env.get(node.f_name, lf)
    func = evaluate(node.call_obj, env)

    if isinstance(func, Function):
        result = call_function(node, func, func.outer_scope, env)
        return result
    elif isinstance(func, ClassInstance):
        constructor: Function = func.env.get(func.class_name, lf)
        call_function(node, constructor, constructor.outer_scope, env)  # call constructor
        return func
    elif isinstance(func, NativeFunction):
        args = []
        kwargs = {}
        for i in range(len(node.args.lines)):
            arg = node.args.lines[i]
            if isinstance(arg, ast.AssignmentNode):
                kwargs[evaluate(arg.left, env)] = evaluate(arg.right, env)
            else:
                args.append(evaluate(arg, env))
        result = func.call(args, kwargs)
        if isinstance(result, ast.BlockStmt):
            # Special case for "eval"
            res = evaluate(result, env)
            return res
        else:
            return result
    else:
        raise lib.InterpretException("Not a function call, in {}, at line {}.".format(node.file, node.line_num))


def call_function(call: ast.FuncCall, func: Function, func_parent_env: Environment, call_env: Environment) \
        -> object:
    """
    Calls a function

    :param call: the call
    :param func: the function object itself
    :param func_parent_env: the parent environment of the function where it was defined
    :param call_env: the environment where the function call was made
    :return: the function result
    """
    lf = call.line_num, call.file

    if func.abstract:
        raise lib.AbstractMethodException("Abstract method is not callable, in '{}', at line {}."
                                          .format(call.file, call.line_num))

    # scope = Environment(FUNCTION_SCOPE, func.outer_scope)
    # scope.scope_name = "Function scope<{}>".format(call.f_name)
    scope = FunctionEnvironment(func.outer_scope)

    params = func.params

    if call.args is None:
        raise lib.SplException("Argument of  function '{}' not set, in file '{}', at line {}."
                               .format(call.f_name, call.file, call.line_num))
    args = call.args.lines

    pos_args = []  # Positional arguments
    kwargs = {}  # Keyword arguments

    for arg in args:
        if isinstance(arg, ast.Node):
            if arg.node_type == ast.ASSIGNMENT_NODE:
                arg: ast.AssignmentNode
                kwargs[arg.left.name] = arg.right
            elif arg.node_type == ast.UNARY_OPERATOR:
                arg: ast.UnaryOperator
                if arg.operation == "unpack":
                    args_list: lib.List = call_env.get(arg.value.name, LINE_FILE)
                    for an_arg in args_list:
                        pos_args.append(an_arg)
                elif arg.operation == "kw_unpack":
                    args_pair: lib.Pair = call_env.get(arg.value.name, LINE_FILE)
                    # print(args_pair)
                    for an_arg in args_pair:
                        kwargs[an_arg.literal] = args_pair[an_arg]
                elif arg.operation == "neg":
                    pos_args.append(arg)
                else:
                    raise lib.TypeException("Invalid operator in function parameter, in file '{}', at line {}."
                                            .format(arg.file, arg.line_num))
            else:
                pos_args.append(arg)
        else:
            pos_args.append(arg)
    # print(pos_args)
    # print(kwargs)
    # if len(pos_args) + len(kwargs) > len(params):
    #     raise lib.ArgumentException("Too many arguments for function '{}', in file '{}', at line {}"
    #                                 .format(call.f_name, call.file, call.line_num))
    arg_index = 0
    for i in range(len(params)):
        # Assign function arguments
        param: ParameterPair = params[i]
        if param.preset is UNPACK_ARGUMENT:
            arg_index = call_unpack(param.name, pos_args, arg_index, scope, call_env, lf)
            continue
        elif param.preset is KW_UNPACK_ARGUMENT:
            call_kw_unpack(param.name, kwargs, scope, call_env, lf)
            continue
        elif i < len(pos_args):
            arg = pos_args[arg_index]
            arg_index += 1
        elif param.name in kwargs:
            arg = kwargs[param.name]
        elif param.preset is not INVALID:
            arg = param.preset
        else:
            raise lib.ArgumentException("Function '{}' missing a positional argument '{}', in file '{}', at line {}"
                                        .format(call.f_name, param.name, call.file, call.line_num))

        e = evaluate(arg, call_env)
        scope.define_var(param.name, e, lf)

    result = evaluate(func.body, scope)
    func_parent_env.assign("=>", result, lf)
    return result


def call_unpack(name: str, pos_args: list, index, scope: Environment, call_env: Environment, lf) -> int:
    lst = lib.List()
    while index < len(pos_args):
        arg = pos_args[index]
        e = evaluate(arg, call_env)
        lst.append(e)
        index += 1

    scope.define_var(name, lst, lf)
    return index


def call_kw_unpack(name: str, kwargs: dict, scope: Environment, call_env: Environment, lf):
    pair = lib.Pair({})
    for k in kwargs:
        v = kwargs[k]
        e = evaluate(v, call_env)
        pair[lib.String(k)] = e

    scope.define_var(name, pair, lf)


def eval_dot(node: ast.Dot, env: Environment):
    instance = evaluate(node.left, env)
    obj = node.right
    t = obj.node_type
    # print(node.left)
    if t == ast.NAME_NODE:
        obj: ast.NameNode
        if obj.name == "this":
            raise lib.UnauthorizedException("Access 'this' from outside")
        if isinstance(instance, lib.NativeType):
            return native_types_invoke(instance, obj)
        elif isinstance(instance, ClassInstance):
            attr = instance.env.get(obj.name, (node.line_num, node.file))
            return attr
        else:
            raise lib.InterpretException("Not a class instance, in {}, at line {}".format(node.file, node.line_num))
    elif t == ast.FUNCTION_CALL:
        obj: ast.FuncCall
        if isinstance(instance, lib.NativeType):
            try:
                return native_types_call(instance, obj, env)
            except IndexError as ie:
                raise lib.IndexOutOfRangeException(str(ie) + " in file: '{}', at line {}"
                                                   .format(node.file, node.line_num))
        elif isinstance(instance, ClassInstance):
            lf = node.line_num, node.file
            # func = instance.env.get(obj.f_name, lf)
            func = evaluate(obj.call_obj, instance.env)
            result = call_function(obj, func, instance.env, env)

            env.assign("=>", result, lf)
            return result
        else:
            raise lib.InterpretException("Not a class instance; {} instead, in {}, at line {}"
                                         .format(typeof(instance), node.file, node.line_num))
    else:
        raise lib.InterpretException("Unknown Syntax, in {}, at line {}".format(node.file, node.line_num))


def arithmetic(left, right_node: ast.Node, symbol, env: Environment):
    if symbol in stl.LAZY:
        if left is None or isinstance(left, bool):
            return primitive_and_or(left, right_node, symbol, env)
        elif isinstance(left, int) or isinstance(left, float):
            return num_and_or(left, right_node, symbol, env)
        else:
            raise lib.InterpretException("Operator '||' '&&' do not support type.")
    else:
        right = evaluate(right_node, env)
        if left is None or isinstance(left, bool):
            return primitive_arithmetic(left, right, symbol)
        elif isinstance(left, int) or isinstance(left, float):
            return num_arithmetic(left, right, symbol)
        elif isinstance(left, lib.String):
            return string_arithmetic(left, right, symbol)
        elif isinstance(left, lib.NativeType):  # NativeTypes other than String
            return native_arithmetic(left, right, symbol)
        elif isinstance(left, ClassInstance):
            return instance_arithmetic(left, right, symbol, env, right_node)
        else:
            return raw_type_comparison(left, right, symbol)


def instance_arithmetic(left: ClassInstance, right, symbol, env: Environment, right_node):
    if symbol == "===" or symbol == "is":
        return isinstance(right, ClassInstance) and left.id == right.id
    elif symbol == "!==":
        return not isinstance(right, ClassInstance) or left.id != right.id
    elif symbol == "instanceof":
        if isinstance(right, Class):
            return is_subclass_of(env.get_heap(left.class_name), right.class_name, env)
        elif isinstance(right_node, ast.NameNode) and isinstance(right, Function):
            right_extra = env.get_heap(right_node.name)
            return is_subclass_of(env.get_heap(left.class_name), right_extra.class_name, env)
        else:
            return False
    else:
        op_name = "__" + stl.BINARY_OPERATORS[symbol] + "__"
        fc = ast.FuncCall(LINE_FILE, op_name)
        fc.call_obj = ast.NameNode(LINE_FILE, op_name)
        if not left.env.contains_key(op_name):
            raise lib.AttributeException("Class '{}' does not support operation '{}'".format(left.class_name, symbol))
        block = ast.BlockStmt(LINE_FILE)
        block.add_line(right)
        fc.args = block
        # func: Function = left.env.get(fc.f_name, LINE_FILE)
        func: Function = evaluate(fc.call_obj, left.env)
        result = call_function(fc, func, left.env, env)
        return result


def native_arithmetic(left: lib.NativeType, right, symbol: str):
    if symbol == "===" or symbol == "is":
        return isinstance(right, lib.NativeType) and left.id == right.id
    elif symbol == "!==":
        return not isinstance(right, lib.NativeType) or left.id != right.id
    elif symbol == "instanceof":
        if isinstance(right, NativeFunction):
            return left.type_name() == right.name
        else:
            return False
    elif symbol == "==":
        return left == right
    elif symbol == "!=":
        return left != right
    else:
        raise lib.TypeException("Unsupported operation '{}' between {} and {}".format(symbol,
                                                                                      typeof(left),
                                                                                      typeof(right)))


STRING_ARITHMETIC_TABLE = {
    "==": lambda left, right: left == right,
    "!=": lambda left, right: left != right,
    "+": lambda left, right: left + right,
    "===": lambda left, right: left is right,
    "is": lambda left, right: left is right,
    "!==": lambda left, right: left is not right,
    "instanceof": lambda left, right: isinstance(right, NativeFunction) and right.name == "string"
}


def string_arithmetic(left, right, symbol):
    return STRING_ARITHMETIC_TABLE[symbol](left, right)


RAW_TYPE_COMPARISON_TABLE = {
    "==": lambda left, right: left == right,
    "!=": lambda left, right: left != right,
    "===": lambda left, right: left is right,
    "is": lambda left, right: left is right,
    "!==": lambda left, right: left is not right,
    "instanceof": lambda left, right: False
}


def raw_type_comparison(left, right, symbol):
    return RAW_TYPE_COMPARISON_TABLE[symbol](left, right)


def primitive_and_or(left, right_node: ast.Node, symbol, env: Environment):
    if left:
        if symbol == "&&" or symbol == "and":
            right = evaluate(right_node, env)
            return right
        elif symbol == "||" or symbol == "or":
            return True
        else:
            raise lib.TypeException("Unsupported operation for primitive type")
    else:
        if symbol == "&&" or symbol == "and":
            return False
        elif symbol == "||" or symbol == "or":
            right = evaluate(right_node, env)
            return right
        else:
            raise lib.TypeException("Unsupported operation for primitive type")


PRIMITIVE_ARITHMETIC_TABLE = {
    "==": lambda left, right: left == right,
    "!=": lambda left, right: left != right,
    "===": lambda left, right: left is right,
    "is": lambda left, right: left is right,
    "!==": lambda left, right: left is not right,
    "instanceof": lambda left, right: isinstance(right, NativeFunction) and PRIMITIVE_TYPE_TABLE[right.name] == type(
        left).__name__
}


def primitive_arithmetic(left, right, symbol):
    operation = PRIMITIVE_ARITHMETIC_TABLE[symbol]
    return operation(left, right)


def num_and_or(left, right_node: ast.Node, symbol, env: Environment):
    if left:
        if symbol == "||" or symbol == "or":
            return True
        elif symbol == "&&" or symbol == "and":
            right = evaluate(right_node, env)
            return right
        else:
            raise lib.TypeException("No such symbol")
    else:
        if symbol == "&&" or symbol == "and":
            return False
        elif symbol == "||" or symbol == "or":
            right = evaluate(right_node, env)
            return right
        else:
            raise lib.TypeException("No such symbol")


def divide(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a // b
    else:
        return a / b


NUMBER_ARITHMETIC_TABLE = {
    "+": lambda left, right: left + right,
    "-": lambda left, right: left - right,
    "*": lambda left, right: left * right,
    "/": divide,  # a special case in case to produce integer if int/int
    "%": lambda left, right: left % right,
    "==": lambda left, right: left == right,
    "!=": lambda left, right: left != right,
    ">": lambda left, right: left > right,
    "<": lambda left, right: left < right,
    ">=": lambda left, right: left >= right,
    "<=": lambda left, right: left <= right,
    "<<": lambda left, right: left << right,
    ">>": lambda left, right: left >> right,
    "&": lambda left, right: left & right,
    "^": lambda left, right: left ^ right,
    "|": lambda left, right: left | right,
    "===": lambda left, right: left is right,
    "is": lambda left, right: left is right,
    "!==": lambda left, right: left is not right,
    "instanceof": lambda left, right: isinstance(right, NativeFunction) and right.name == type(left).__name__
}


def num_arithmetic(left, right, symbol):
    return NUMBER_ARITHMETIC_TABLE[symbol](left, right)


def class_inheritance(cla: Class, env: Environment, scope: Environment):
    """

    :param cla:
    :param env: the global environment
    :param scope: the class scope
    :return: None
    """
    for sc in cla.superclass_names:
        # if sc != "Object":
        class_inheritance(env.get_heap(sc), env, scope)

    evaluate(cla.body, scope)  # this step just fills the scope


def native_types_call(instance: lib.NativeType, method: ast.FuncCall, env: Environment):
    """
    Calls a method of a native object.

    :param instance: the NativeType object instance
    :param method: the method being called
    :param env: the current working environment
    :return: the returning value of the method called
    """
    args = []
    for x in method.args.lines:
        args.append(evaluate(x, env))
    # name = method.f_name
    name = method.call_obj.name
    type_ = type(instance)
    method = getattr(type_, name)
    params: tuple = method.__code__.co_varnames
    if "env" in params and params.index("env") == 1:
        res = method(instance, env, *args)
    else:
        res = method(instance, *args)
    # check_gc(env, mem.Pointer(instance.id))
    return res


def native_types_invoke(instance: lib.NativeType, node: ast.NameNode):
    """
    Invokes an attribute of a native type.

    :param instance:
    :param node:
    :return:
    """
    name = node.name
    type_ = type(instance)
    res = getattr(type_, name)
    return res


def self_return(node):
    return node


def eval_boolean_stmt(node: ast.BooleanStmt, env):
    if node.value == "true":
        return True
    elif node.value == "false":
        return False
    else:
        raise lib.InterpretException("Unknown boolean value")


def eval_anonymous_call(node: ast.AnonymousCall, env: Environment):
    evaluate(node.left, env)
    right = node.right.args
    fc = ast.FuncCall((node.line_num, node.file), "=>")
    fc.args = right
    return evaluate(fc, env)


def eval_return(node: ast.Node, env: Environment):
    res = evaluate(node, env)
    # print(env.variables)
    env.terminate(res)
    return res


def eval_block(node: ast.BlockStmt, env: Environment):
    result = None
    for line in node.lines:
        result = evaluate(line, env)
    return result


def eval_if_stmt(node: ast.IfStmt, env: Environment):
    cond = evaluate(node.condition, env)
    block_scope = SubEnvironment(env)
    if cond:
        return evaluate(node.then_block, block_scope)
    else:
        return evaluate(node.else_block, block_scope)


def eval_while(node: ast.WhileStmt, env: Environment):
    title_scope = LoopEnvironment(env)

    block_scope = SubEnvironment(title_scope)

    result = 0
    while not title_scope.broken and evaluate(node.condition, title_scope):
        block_scope.invalidate()
        result = evaluate(node.body, block_scope)
        title_scope.resume_loop()

    del title_scope
    del block_scope
    return result


def eval_for_loop_stmt(node: ast.ForLoopStmt, env: Environment):
    arg_num = len(node.condition.lines)
    if arg_num == 3:
        return eval_for_loop(node, env)
    elif arg_num == 2:
        return eval_for_each_loop(node, env)
    else:
        raise lib.ArgumentException("Wrong argument number for 'for' loop, in {}, at line {}"
                                    .format(node.file, node.line_num))


def eval_def(node: ast.DefStmt, env: Environment):
    block: ast.BlockStmt = node.params
    params_lst = []
    # print(block)
    for p in block.lines:
        # p: ast.Node
        if p.node_type == ast.NAME_NODE:
            p: ast.NameNode
            name = p.name
            value = INVALID
        elif p.node_type == ast.ASSIGNMENT_NODE:
            p: ast.AssignmentNode
            name = p.left.name
            value = evaluate(p.right, env)
        elif p.node_type == ast.UNARY_OPERATOR:
            p: ast.UnaryOperator
            if p.operation == "unpack":
                name = p.value.name
                value = UNPACK_ARGUMENT
            elif p.operation == "kw_unpack":
                name = p.value.name
                value = KW_UNPACK_ARGUMENT
            else:
                raise lib.SplException("Unexpected syntax in function parameter, in file '{}', at line {}."
                                       .format(node.file, node.line_num))
        else:
            raise lib.SplException("Unexpected syntax in function parameter, in file '{}', at line {}."
                                   .format(node.file, node.line_num))
        pair = ParameterPair(name, value)
        params_lst.append(pair)

    options = {"override": "Override" in node.tags, "suppress": "Suppress" in node.tags}
    f = Function(params_lst, node.body, env, node.abstract, options)
    f.file = node.file
    f.line_num = node.line_num
    # options = {"override": "Override" in node.tags, "suppress": "Suppress" in node.tags}
    # env.define_function(node.name, f, (node.line_num, node.file), options)

    return f


def eval_class_stmt(node: ast.ClassStmt, env: Environment):
    cla = Class(node.class_name, node.block, node.abstract)
    cla.superclass_names = node.superclass_names
    cla.outer_env = env
    cla.line_num, cla.file = node.line_num, node.file
    env.add_heap(node.class_name, cla)
    return cla


def eval_jump(node, env: Environment):
    func: Function = env.get(node.to, (0, "f"))
    lf = node.line_num, node.file
    for i in range(len(node.args.lines)):
        env.assign(func.params[i].name, evaluate(node.args.lines[i], env), lf)
    return evaluate(func.body, env)


def eval_assert(node: ast.Node, env: Environment):
    result = evaluate(node, env)
    if result is not True:
        raise lib.AssertionException("Assertion failed, in file '{}', at line {}".format(node.file, node.line_num))


UNARY_TABLE = {
    "return": eval_return,
    "throw": lambda n, env: raise_exception(RuntimeException(evaluate(n, env))),
    "neg": lambda n, env: -evaluate(n, env),
    "!": lambda n, env: not bool(evaluate(n, env)),
    "assert": eval_assert,
}


def eval_unary_expression(node: ast.UnaryOperator, env: Environment):
    t = node.operation
    op = UNARY_TABLE[t]
    return op(node.value, env)


def eval_conditional_operator(left: ast.Node, mid: ast.Node, right: ast.Node, env: Environment):
    cond = evaluate(left, env)
    if cond:
        return evaluate(mid, env)
    else:
        return evaluate(right, env)


TERNARY_TABLE = {
    ("?", ":"): eval_conditional_operator
}


def eval_ternary_expression(node: ast.TernaryOperator, env: Environment):
    op1 = node.first_op
    op2 = node.second_op
    op = TERNARY_TABLE[(op1, op2)]
    return op(node.left, node.mid, node.right, env)


def raise_exception(e: Exception):
    raise e


# Set of types that will not change after being evaluated
SELF_RETURN_TABLE = {int, float, bool, lib.String, lib.List, lib.Set, lib.Pair, lib.System, lib.File, ClassInstance}

# Operation table of every non-abstract node types
NODE_TABLE = {
    # ast.INT_NODE: lambda n, env: n.value,
    # ast.FLOAT_NODE: lambda n, env: n.value,
    ast.LITERAL_NODE: lambda n, env: lib.String(n.literal),
    ast.NAME_NODE: lambda n, env: env.get(n.name, (n.line_num, n.file)),
    ast.BOOLEAN_STMT: eval_boolean_stmt,
    ast.NULL_STMT: lambda n, env: None,
    ast.BREAK_STMT: lambda n, env: env.break_loop(),
    ast.CONTINUE_STMT: lambda n, env: env.pause_loop(),
    ast.ASSIGNMENT_NODE: assignment,
    ast.DOT: eval_dot,
    ast.ANONYMOUS_CALL: eval_anonymous_call,
    ast.OPERATOR_NODE: eval_operator,
    ast.UNARY_OPERATOR: eval_unary_expression,
    ast.TERNARY_OPERATOR: eval_ternary_expression,
    ast.BLOCK_STMT: eval_block,
    ast.IF_STMT: eval_if_stmt,
    ast.WHILE_STMT: eval_while,
    ast.FOR_LOOP_STMT: eval_for_loop_stmt,
    ast.DEF_STMT: eval_def,
    ast.FUNCTION_CALL: eval_func_call,
    ast.CLASS_STMT: eval_class_stmt,
    ast.CLASS_INIT: init_class,
    ast.TRY_STMT: eval_try_catch,
    ast.JUMP_NODE: eval_jump,
    ast.UNDEFINED_NODE: lambda n, env: UNDEFINED,
    # ast.ARRAY_INIT: eval_array_init
}


def evaluate(node: ast.Node, env: Environment):
    """
    Evaluates a abstract syntax tree node, with the corresponding working environment.

    :param node: the node in abstract syntax tree to be evaluated
    :param env: the working environment
    :return: the evaluation result
    """
    if env.is_terminated():
        return env.terminate_value()
    if node is None:
        return None
    if type(node) in SELF_RETURN_TABLE:
        return node
    t = node.node_type
    node.execution += 1
    tn = NODE_TABLE[t]
    env.add_heap("cwf", node.file)
    return tn(node, env)

# Processes before run
