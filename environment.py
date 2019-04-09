import spl_lib as lib

GLOBAL_SCOPE = 0
CLASS_SCOPE = 1
FUNCTION_SCOPE = 2
LOOP_SCOPE = 3
SUB_SCOPE = 4


class NullPointer:
    def __init__(self):
        pass

    def __str__(self):
        return "NullPointer"


NULLPTR = NullPointer()


class Environment:
    variables: dict
    constants: dict
    scope_type: int

    """
    ===== Attributes =====
    :param scope_type: the type of scope, whether it is global, class, function or inner
    :param heap: the shared-heap space, all pointed to one
    """

    def __init__(self, scope_type, outer):
        self.scope_type = scope_type
        self.variables: dict = {}  # Stack variables
        self.constants: dict = {}  # Constants

        self.outer: Environment = outer

    def __str__(self):
        temp = ["Const: "]
        for c in self.constants:
            if c != "this":
                temp.append(str(c))
                temp.append(": ")
                temp.append(str(self.constants[c]))
                temp.append(", ")
        for v in self.variables:
            temp.append(str(v))
            temp.append(": ")
            temp.append(str(self.variables[v]))
            temp.append(", ")
        return "".join(['null' if k is None else k for k in temp])

    def invalidate(self):
        """
        Re-initialize this scope.

        This method will only be called in a scope under level 'LOOP_SCOPE', although this access will not
        be checked.

        :return: None
        """
        self.variables.clear()
        self.constants.clear()

    def is_global(self):
        raise NotImplementedError

    def is_sub(self):
        """
        Returns True iff this scope is a NOT a main scope.

        A 'main scope' is a scope that has its independent variable layer. GLOBAL_SCOPE, CLASS_SCOPE and
        FUNCTION_SCOPE are main scopes.

        :return:
        """
        raise NotImplementedError

    def inner_get_heap(self, key):
        raise NotImplementedError

    def add_heap(self, k, v):
        raise NotImplementedError

    def has_class(self, class_name):
        return not self.inner_get_heap(class_name) is NULLPTR

    def get_heap(self, class_name: str):
        """
        Returns the heap-variable corresponding to the key 'class_name'.

        This method will return the instance if the value stored in heap is a pointer.

        :param class_name:
        :return: the heap-variable corresponding to the key 'class_name'. Instance will be returned if the
        value stored in heap is a pointer.
        """
        obj = self.inner_get_heap(class_name)
        if obj is NULLPTR:
            raise lib.SplException("Global name '{}' is not defined".format(class_name))
        return obj

    def terminate(self, exit_value):
        raise lib.SplException("Return outside function.")

    def is_terminated(self):
        """
        Returns True iff this scope or one of its parent scopes had been terminated.

        :return: True iff this scope or one of its parent scopes had been terminated
        """
        return False

    def terminate_value(self):
        """
        Returns the last recorded terminate value of a function scope that the function had returned early.

        :return: the terminate value
        """
        raise lib.SplException("Terminate value outside function.")

    def break_loop(self):
        raise lib.SplException("Break not inside loop.")

    def pause_loop(self):
        """
        Pauses the loop for one iteration.

        This method is called when the keyword 'continue' is executed.

        :return: None
        """
        raise lib.SplException("Continue not inside loop.")

    def resume_loop(self):
        """
        Resumes a paused loop environment.

        If this scope is not paused, this method can still be called but makes no effect.

        :return: None
        """
        raise lib.SplException("Not inside loop.")

    def define_function(self, key, value, lf, options: dict):
        if not options["override"] and not options["suppress"] and key[0].islower() and self.contains_key(key):
            lib.print_waring("Warning: re-declaring method '{}' in '{}', at line {}".format(key, lf[1], lf[0]))
        self.variables[key] = value

    def define_var(self, key, value, lf):
        if self.local_contains(key):
            raise lib.SplException("Name '{}' is already defined in this scope, in '{}', at line {}"
                                   .format(key, lf[1], lf[0]))
        else:
            self.variables[key] = value

    def define_const(self, key, value, lf):
        if self.contains_key(key):
            raise lib.SplException("Name '{}' is already defined in this scope, in {}, at line {}"
                                   .format(key, lf[1], lf[0]))
        else:
            self.constants[key] = value

    def assign(self, key, value, lf):
        if key in self.variables:
            self.variables[key] = value
        else:
            out = self.outer
            while out:
                if key in out.variables:
                    out.variables[key] = value
                    return
                out = out.outer
            raise lib.SplException("Name '{}' is not defined, in '{}', at line {}"
                                   .format(key, lf[1], lf[0]))

    def local_inner_get(self, key: str):
        if key in self.constants:
            return self.constants[key]
        if key in self.variables:
            return self.variables[key]

        out = self
        while out.outer and out.is_sub():
            out = out.outer

            if key in out.constants:
                return out.constants[key]
            if key in out.variables:
                return out.variables[key]

        return self.inner_get_heap(key)

    def local_contains(self, key: str) -> bool:
        """
        Returns True iff this main scope has this key, or the heap has this key.

        :param key:
        :return:
        """
        v = self.local_inner_get(key)
        return v is not NULLPTR

    def inner_get(self, key: str):
        """
        Internally gets a value stored in this scope, 'NULLPTR' if not found.

        :param key:
        :return:
        """
        if key in self.constants:
            return self.constants[key]
        if key in self.variables:
            return self.variables[key]

        out = self.outer
        while out:
            if key in out.constants:
                return out.constants[key]
            if key in out.variables:
                return out.variables[key]

            out = out.outer

        return self.inner_get_heap(key)

    def get(self, key: str, line_file: tuple):
        """
        Returns the value of that key.

        If the value is a pointer, then returns the instance pointed by the pointer instead.

        :param key:
        :param line_file:
        :return: the value corresponding to the key. Instance will be returned if the value is a pointer.
        """
        v = self.inner_get(key)
        # print(key + str(v))
        if v is NULLPTR:
            raise lib.SplException("Name '{}' is not defined, in file {}, at line {}"
                                   .format(key, line_file[1], line_file[0]))
        return v

    def contains_key(self, key: str):
        v = self.inner_get(key)
        return v is not NULLPTR

    def attributes(self):
        """
        Returns a union of all local variables in this scope.

        :return: a union of all local variables in this scope
        """
        return {**self.constants, **self.variables}


class GlobalEnvironment(Environment):
    def __init__(self):
        Environment.__init__(self, GLOBAL_SCOPE, None)

        self.heap = {}

    def is_global(self):
        return True

    def is_sub(self):
        return False

    def add_heap(self, k, v):
        self.heap[k] = v

    def inner_get_heap(self, key):
        return self.heap[key] if key in self.heap else NULLPTR


class ClassEnvironment(Environment):
    def __init__(self, outer):
        Environment.__init__(self, CLASS_SCOPE, outer)

    def is_global(self):
        return False

    def is_sub(self):
        return False

    def add_heap(self, k, v):
        self.outer.add_heap(k, v)

    def inner_get_heap(self, key):
        return self.outer.inner_get_heap(key)


class FunctionEnvironment(Environment):
    def __init__(self, outer):
        Environment.__init__(self, FUNCTION_SCOPE, outer)

        self.terminated = False
        self.exit_value = None

    def is_global(self):
        return False

    def is_sub(self):
        return False

    def terminate(self, exit_value):
        self.terminated = True
        self.exit_value = exit_value

    def terminate_value(self):
        return self.exit_value

    def is_terminated(self):
        return self.terminated

    def add_heap(self, k, v):
        self.outer.add_heap(k, v)

    def inner_get_heap(self, key):
        return self.outer.inner_get_heap(key)


class LoopEnvironment(Environment):
    def __init__(self, outer):
        Environment.__init__(self, LOOP_SCOPE, outer)

        self.broken = False
        self.paused = False

    def resume_loop(self):
        self.paused = False

    def is_global(self):
        return False

    def is_sub(self):
        return True

    def terminate(self, exit_value):
        self.broken = True
        self.outer.terminate(exit_value)

    def terminate_value(self):
        return self.outer.terminate_value()

    def is_terminated(self):
        return self.outer.is_terminated()

    def break_loop(self):
        self.broken = True

    def pause_loop(self):
        self.paused = True

    def add_heap(self, k, v):
        self.outer.add_heap(k, v)

    def inner_get_heap(self, key):
        return self.outer.inner_get_heap(key)


class SubEnvironment(Environment):
    def __init__(self, outer):
        Environment.__init__(self, SUB_SCOPE, outer)

    def resume_loop(self):
        self.outer.resume_loop()

    def is_global(self):
        return False

    def is_sub(self):
        return True

    def terminate(self, exit_value):
        self.outer.terminate(exit_value)

    def terminate_value(self):
        return self.outer.terminate_value()

    def is_terminated(self):
        return self.outer.is_terminated()

    def break_loop(self):
        self.outer.break_loop()

    def pause_loop(self):
        self.outer.pause_loop()

    def add_heap(self, k, v):
        self.outer.add_heap(k, v)

    def inner_get_heap(self, key):
        return self.outer.inner_get_heap(key)
