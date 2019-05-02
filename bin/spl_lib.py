import sys
import time as time_lib
import os
import spl_memory as mem


def replace_bool_none(string: str):
    """
    Returns a str with 'None', 'True', and 'False' replaced with 'null', 'true', and 'false'.

    This function also removes quotes generated by spl String object.

    :param string: the str object to be replaced
    :return: a str with 'None', 'True', and 'False' replaced with 'null', 'true', and 'false'
    """
    in_single = False
    in_double = False
    lst = []
    i = 0
    while i < len(string):
        ch = string[i]
        if in_single:
            if ch == "'":
                in_single = False
                i += 1
                continue
        elif in_double:
            if ch == '"':
                in_double = False
                i += 1
                continue
        else:
            if ch == "'":
                in_single = True
                i += 1
                continue
            elif ch == '"':
                in_double = True
                i += 1
                continue
        if not in_single and not in_double:
            if i <= len(string) - 4:
                if string[i:i + 4] == "True":
                    lst.append("true")
                    i += 4
                    continue
                elif string[i:i + 4] == "None":
                    lst.append("null")
                    i += 4
                    continue
            if i <= len(string) - 5:
                if string[i:i + 5] == "False":
                    lst.append("false")
                    i += 5
                    continue
        lst.append(ch)
        i += 1
    return "".join(lst)


def print_waring(msg: str):
    sys.stderr.write(msg + "\n")
    sys.stderr.flush()


def concatenate_path(path: str, directory: str) -> str:
    if os.path.isabs(path):
        return path
    else:
        return directory + os.sep + path


def get_string_literal(lit) -> str:
    if lit is None:
        return "null"
    elif isinstance(lit, bool):
        return "true" if lit else "false"
    elif isinstance(lit, String):
        return lit.literal
    else:
        return str(lit)


def get_string_repr(o) -> str:
    if o is None:
        return "null"
    elif isinstance(o, bool):
        return "true" if o else "false"
    elif isinstance(o, int) or isinstance(o, float):
        return str(o)
    elif isinstance(o, String):
        return "'" + o.__repr__() + "'"
    else:
        return repr(o)


# Native functions with no dependency


class SplObject:
    """
    An superset of spl objects.

    There are two types of SplObjects: NativeType and Class

    ----- Attributes -----
        id: the identifier of this object, is guaranteed to be unique
    """

    id: int

    def __init__(self):
        self.id = mem.MEMORY.allocate()


class NativeType(SplObject):
    def __init__(self):
        SplObject.__init__(self)

    @classmethod
    def type_name__(cls) -> str:
        raise NotImplementedError

    @classmethod
    def doc__(cls) -> str:
        """
        :return: the doc string of this type
        """
        doc = ["NativeObject ", cls.type_name__(), " ", cls.__doc__, "\n"]
        for x in dir(cls):
            if len(x) < 2 or x[-2:] != "__":
                attr = getattr(cls, x)
                if callable(attr):
                    doc.append("    method ")
                    doc.append(x)
                    doc.append("(")
                    params = attr.__code__.co_varnames
                    for p in params:
                        if p != "self":
                            doc.append(p)
                            doc.append(", ")
                    if doc[-1] == ", ":
                        doc.pop()
                    doc.append("):")
                    doc.append("\n")
                    attr_doc = attr.__doc__
                    if attr_doc:
                        doc.append(attr_doc)
                        doc.append("\n")
        return "".join([str(x) for x in doc])


class Iterable:
    def __init__(self):
        pass

    def __iter__(self):
        raise NotImplementedError


class String(NativeType, Iterable):
    """
    An object of a string literal.
    """

    def __init__(self, lit):
        NativeType.__init__(self)

        self.literal = get_string_literal(lit)

    def __contains__(self, item):
        return item in self.literal

    def __iter__(self):
        return (c for c in self.literal)

    def __str__(self):
        return self.literal

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, String) and self.literal == other.literal

    def __hash__(self):
        return hash(self.literal)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, String):
            return String(self.literal + other.literal)
        else:
            raise TypeException("Cannot add <String> with <{}>".format(type(other).__name__))

    def __getitem__(self, index):
        return self.literal[index]

    def length(self):
        """
        Returns the length of this string.

        :return: the length of this string
        """
        return len(self.literal)

    def contains(self, char):
        """
        Returns whether the <char> is a substring of this <String>.

        :param char: the character or string to look for
        :return: <true> iff the <char> is a substring of this <String>
        """
        return char.literal in self.literal

    def format(self, *args):
        """
        Formats this string with the specified format.

        :param args: the formats
        :return: the formatted string
        """
        lst = []
        i = 0
        count = 0
        while i < self.length():
            ch = self.literal[i]
            if ch == "%":
                j = i + 1
                params = []
                while not self.literal[j].isalpha():
                    params.append(self.literal[j])
                    j += 1
                if count >= len(args):
                    raise IndexOutOfRangeException("Not enough arguments for string format")
                flag = self.literal[j]
                if flag == "s":
                    lit = args[count]
                    try:
                        lst.append(lit.literal)
                    except AttributeError:
                        raise StringFormatException("Cannot resolve type '{}' with symbol '%s'"
                                                    .format(type(lit).__name__))
                elif flag == "d":
                    lst.append(str(int(args[count])))
                elif flag == "f":
                    if len(params) > 0:
                        precision = int(params[0])
                        lst.append(str(round(args[count], precision)))
                    else:
                        lst.append(str(args[count]))
                elif flag == "r":
                    lit = args[count]
                    lst.append(str(lit))
                else:
                    print_waring("Warning: Unknown flag: %" + flag)
                    lst.append("%")
                    i = j
                    continue
                i = j + 1
                count += 1
                continue
            lst.append(ch)
            i += 1

        if count < len(args):
            print_waring("Warning: too much arguments for string format")
        return String("".join(lst))

    @classmethod
    def type_name__(cls):
        return "String"

    def substring(self, from_, to=None):
        length = self.length()
        end = length if to is None else to
        if from_ < 0 or end > length:
            raise IndexOutOfRangeException("Substring index out of range")
        return String(self.literal[from_: end])


class PyInputStream(NativeType):
    def __init__(self, stream):
        NativeType.__init__(self)

        self.stream = stream

    @classmethod
    def type_name__(cls) -> str:
        return "PyInputStream"

    def read(self):
        return self.stream.read()

    def close(self):
        self.stream.close()


class PyOutputStream(NativeType):
    def __init__(self, stream):
        NativeType.__init__(self)

        self.stream = stream

    @classmethod
    def type_name__(cls) -> str:
        return "PyOutputStream"

    def write(self, obj):
        self.stream.write(str(obj))

    def flush(self):
        self.stream.flush()

    def close(self):
        self.stream.close()


class List(NativeType, Iterable):
    """
    A collector of sequential data with dynamic size and type.
    """
    def __init__(self, *initial, mutable=True):
        NativeType.__init__(self)

        self.mutable = mutable
        self.list = [*initial]

    def __iter__(self):
        return (x for x in self.list)

    def __str__(self):
        return str([String(get_string_repr(v)) for v in self.list])

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self.list[item]

    def __setitem__(self, key, value):
        self.list[key] = value

    def set(self, key, value):
        if self.mutable:
            self.__setitem__(key, value)
        else:
            raise IllegalOperationException("Mutating an immutable list")

    def get(self, key):
        return self.__getitem__(key)

    @classmethod
    def type_name__(cls):
        return "List"

    def append(self, value):
        """
        Adds a value at the end of this list.

        :param value: the item to be added
        """
        if self.mutable:
            self.list.append(value)
            return value
        else:
            raise IllegalOperationException("Mutating an immutable list")

    def contains(self, item):
        return item in self.list

    def insert(self, index, item):
        if self.mutable:
            self.list.insert(index, item)
        else:
            raise IllegalOperationException("Mutating an immutable list")

    def pop(self, index=-1):
        if self.mutable:
            return self.list.pop(index)
        else:
            raise IllegalOperationException("Mutating an immutable list")

    def clear(self):
        if self.mutable:
            return self.list.clear()
        else:
            raise IllegalOperationException("Mutating an immutable list")

    def extend(self, lst):
        if self.mutable:
            return self.list.extend(lst)
        else:
            raise IllegalOperationException("Mutating an immutable list")

    def size(self):
        return len(self.list)

    def sort(self):
        if self.mutable:
            return self.list.sort()
        else:
            raise IllegalOperationException("Mutating an immutable list")

    def sublist(self, from_, to=None):
        length = self.size()
        end = length if to is None else to
        if from_ < 0 or end > length:
            raise IndexOutOfRangeException("Sublist index out of range")
        return List(self.list[from_: end])

    def reverse(self):
        if self.mutable:
            return self.list.reverse()
        else:
            raise IllegalOperationException("Mutating an immutable list")


class Pair(NativeType, Iterable):
    def __init__(self, initial: dict):
        NativeType.__init__(self)

        self.pair = initial.copy()

    def __iter__(self):
        return (k for k in self.pair)

    def __str__(self):
        return str({String(get_string_repr(k)): String(get_string_repr(self.pair[k])) for k in self.pair})

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        return self.pair[item]

    def __setitem__(self, key, value):
        self.pair[key] = value

    def contains(self, item):
        return item in self.pair

    def get(self, key):
        return self.__getitem__(key)

    def put(self, key, value):
        self.__setitem__(key, value)

    def size(self):
        return len(self.pair)

    @classmethod
    def type_name__(cls):
        return "Pair"


class Set(NativeType, Iterable):
    def __init__(self, *initial):
        NativeType.__init__(self)

        self.set = set(initial)

    def __iter__(self):
        return (v for v in self.set)

    def __str__(self):
        return str(set([String(get_string_repr(v)) for v in self.set]))

    def __repr__(self):
        return self.__str__()

    def size(self):
        return len(self.set)

    def add(self, item):
        self.set.add(item)

    def pop(self):
        self.set.pop()

    def clear(self):
        self.set.clear()

    def union(self, other):
        self.set.union(other)

    def update(self, s):
        self.set.update(s)

    def contains(self, item):
        return item in self.set

    @classmethod
    def type_name__(cls):
        return "Set"


class System(NativeType):
    """
    A class consists of system calls

    ----- Attributes -----
        argv: command line arguments
        cwd: the working directory
        encoding: the encoding mode
        stdout: system standard output stream, ClassInstance extends OutputStream
        stderr: system standard error output stream, ClassInstance extends OutputStream
        stdin: system standard input stream, ClassInstance extends InputStream
    """

    argv: List
    cwd: String
    encoding: str
    native_in = None
    native_out = None
    native_err = None
    stdout = None  # ClassInstance <NativeOutputStream>
    stderr = None  # ClassInstance <NativeOutputStream>
    stdin = None  # ClassInstance <NativeInputStream>

    def __init__(self, argv_: List, directory: String, enc: str, in_out_err):
        NativeType.__init__(self)

        self.native_in = PyInputStream(in_out_err[0])
        self.native_out = PyOutputStream(in_out_err[1])
        self.native_err = PyOutputStream(in_out_err[2])
        self.cwd = directory
        self.argv = argv_
        self.encoding = enc

    def set_in(self, in_):
        self.stdin = in_

    def set_out(self, out):
        self.stdout = out

    def set_err(self, err):
        self.stderr = err

    @staticmethod
    def time():
        """
        Returns the current system time, in millisecond.

        :return: the current system time, in millisecond
        """
        return int(time_lib.time() * 1000)

    @staticmethod
    def sleep(milli):
        """
        Pause the current thread for a period of time, in millisecond.

        :param milli: the time to pause, in millisecond
        """
        time_lib.sleep(milli / 1000)

    @classmethod
    def type_name__(cls):
        return "System"


class Os(NativeType):
    """
    A class consists of functions related to operating system

    ----- Attributes -----
        name: the name of the os
        separator: the default path separator of the os
    """
    name = String(os.name)
    separator = String(os.sep)

    def __init__(self):
        NativeType.__init__(self)

    @classmethod
    def type_name__(cls):
        return "Os"

    @staticmethod
    def list_files(path) -> List:
        """
        Returns a <List> consists of all files under the directory <path>.

        :param path: the directory path
        :return: a <List> consists of all files under the directory <path>
        """
        return List(os.listdir(path))


class File(NativeType):
    """
    An opened file object.
    """

    def __init__(self, fp, mode):
        NativeType.__init__(self)

        self.mode: str = mode
        self.fp = fp

    def read_one(self):
        """
        Reads one unit from the file.

        :return: the next unit in tis file
        """
        r = self.fp.read(1)
        if r:
            if self.mode == "r":
                return String(r)
            elif self.mode == "rb":
                return int(self.fp.read(1)[0])
            else:
                raise IOException("Wrong mode")
        else:
            return None

    def read(self):
        """
        Reads all contents of this file.

        :return: all contents of this file
        """
        if self.mode == "r":
            return String(self.fp.read())
        elif self.mode == "rb":
            return List(*list(self.fp.read()))
        else:
            raise IOException("Wrong mode")

    def readline(self):
        """
        Reads the next line from this file.

        This method only works for text file.

        :return: the next line from this file
        """
        if self.mode == "r":
            s = self.fp.readline()
            if s:
                return String(s)
            else:
                return None
        else:
            raise IOException("Wrong mode")

    def write(self, s):
        """
        Writes the content to this file

        :param s: the content to be written
        """
        if "w" in self.mode:
            if "b" in self.mode:
                self.fp.write(bytes(s))
            else:
                self.fp.write(str(s))
        else:
            raise IOException("Wrong mode")

    def flush(self):
        """
        Flushes all buffered contents to the file.
        """
        if "w" in self.mode:
            self.fp.flush()
        else:
            raise IOException("Wrong mode")

    def close(self):
        """
        Closes this file.
        """
        self.fp.close()

    @classmethod
    def type_name__(cls):
        return "File"


# Exceptions

class InterpretException(Exception):
    def __init__(self, msg=""):
        Exception.__init__(self, msg)


class SplException(InterpretException):
    def __init__(self, msg=""):
        InterpretException.__init__(self, msg)


class NameException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


class TypeException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


class IndexOutOfRangeException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


class IOException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


class AbstractMethodException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


class UnauthorizedException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


class IllegalOperationException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


class ArgumentException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


class ArithmeticException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


class AttributeException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


class StringFormatException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


class AssertionException(SplException):
    def __init__(self, msg=""):
        SplException.__init__(self, msg)


def exit_(code=0):
    """
    Exits the current process.

    :param code: the exit code, 0 as default.
    """
    exit(code)


def input_(*prompt):
    """
    Asks input from user.

    This function will hold the program until the user inputs a new line character.

    :param prompt: the prompt text to be shown to the user
    :return the user input, as <String>
    """
    s = input(*prompt)
    st = String(s)
    return st


def make_list(*initial_elements):
    """
    Creates a dynamic mutable list.

    :param initial_elements: the elements that the list initially contains
    :return: a reference of the newly created <List> object
    """
    lst = List(*initial_elements)
    return lst


def make_immutable_list(*initial_elements):
    """
        Creates an immutable list.

        :param initial_elements: the elements that the list initially contains
        :return: a reference of the newly created <List> object
        """
    lst = List(*initial_elements, mutable=False)
    return lst


def make_pair(initial_elements: dict = None):
    """
    Creates a key-value pair.

    :param initial_elements: the elements that the pair initially contains
    :return: a reference of the newly created <Pair> object
    """
    if initial_elements is None:
        initial_elements = {}
    pair = Pair(initial_elements)
    return pair


def make_set(*initial_elements):
    """
    Creates a set.

    :param initial_elements: the elements that the set initially contains
    :return: a reference of the newly created <Set> object
    """
    s = Set(*initial_elements)
    return s


def to_int(v):
    return int(v)


def to_float(v):
    return float(v)


def to_boolean(v):
    return True if v else False


# etc


class InvalidArgument:
    def __init__(self):
        pass

    def __str__(self):
        return "INVALID"


class UnpackArgument:
    def __init__(self):
        pass

    def __str__(self):
        return "UNPACK"


class KwUnpackArgument:
    def __init__(self):
        pass

    def __str__(self):
        return "KW_UNPACK"
