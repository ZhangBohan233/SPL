/*
 * Superclass of all spl exceptions.
 */
class Exception {
    var message = "";

    /*
     * Create a new <Exception>, with message <msg>.
     */
    function Exception(msg="") {
        message = msg;
    }
}


/*
 * Exception of assertion failed.
 */
class AssertionException extends Exception {
    function AssertionException(msg="") {
        Exception(msg);
    }
}


/*
 * Exception of annotations.
 *
 * Exception from all annotations should be derived from this exception.
 */
class AnnotationException extends Exception {
    function AnnotationException(msg="") {
        Exception(msg);
    }
}


/*
 * A superclass of all iterator classes.
 */
abstract class Iterator {
    abstract function Iterator();

    abstract function __more__();

    abstract function __next__();
}


/*
 * An implementation of a Iterator, works only for integers.
 */
class RangeIterator extends Iterator {

    var iter;
    const step;
    const end;

    /*
     * Creates a new instance.
     *
     * @param begin: the initial value
     * @param end:   the stop value
     * @param step:  the value to be added in each iteration
     */
    function RangeIterator(begin, end, step) {
        this.iter = begin;
        this.end = end;
        this.step = function (x) {x + step};
    }

    @Override
    function __more__() {
        return iter != end;
    }

    @Override
    function __next__() {
        var temp = iter;
        iter = step(iter);
        return temp;
    }
}


/*
 * Superclass of all iterable classes.
 *
 * Iterable are typically used when calling for (iterable; )
 */
abstract class Iterable {

    /*
     * Returns an object to be iterated, probably an <Iterator>.
     */
    abstract function __iter__();
}


abstract class OutputStream {
    abstract function write(obj);

    abstract function flush();

    abstract function close();
}

abstract class InputStream {
    abstract function read();

    abstract function close();
}

/*
 * Abstract class of lined input stream.
 *
 * All classes extends this must implement <readline>
 */
abstract class LineInputStream extends InputStream {

    /*
     * Returns the next line.
     */
    abstract function readline();
}

class NativeInputStream extends LineInputStream {

    var ns;

    function NativeInputStream(stream) {
        ns = stream;
    }

    @Override
    function readline() {
        return ns.readline();
    }

    @Override
    function read() {
        return ns.read();
    }

    @Override
    function close() {
        ns.close();
    }
}

class NativeOutputStream extends OutputStream {

    var ns;

    function NativeOutputStream(stream) {
        ns = stream;
    }

    @Override
    function write(obj) {
        ns.write(obj);
    }

    @Override
    function flush() {
        ns.flush();
    }

    @Override
    function close() {
        ns.close();
    }
}


class List extends Iterable {

    var arr;
    var length = 0;

    function List(*args) {
        arr = array(length=8);
        for (var x; args) {
            append(x);
        }
    }

    function __getitem__(index) {
        return arr[index];
    }

    function __setitem__(index, value) {
        arr[index] = value;
    }

    function __iter__() {
        return to_array();
    }

    function __str__() {
        return string(to_array());
    }

    function __repr__() {
        return __str__();
    }

    function __unpack__() {
        return to_array();
    }

    function append(v) {
        if (length >= arr.size()) {
            double_size();
        }
        arr[length] = v;
        length++;
        return this;
    }

    function insert(index, value) {
        if (length >= arr.size()) {
            double_size();
        }
        for (var i = length + 1; i >= index; i--) {
            arr[i] = arr[i - 1];
        }
        arr[index] = value;
        length++;
    }

    function pop(index=null) {
        if (index === null) {
            index = length - 1;
        }
        var val = arr[index];
        for (var i = index; i < length; i++) {
            arr[i] = arr[i + 1];
        }
        length--;
        if (length < arr.size() / 4) {
            half_size();
        }
        return val;
    }

    function extend(iter) {
        for (var x; iter) {
            append(x);
        }
    }

    function clear() {
        arr = array(length = 8);
    }

    function copy() {
        return new List(*this);
    }

    function size() {
        return length;
    }

    function to_array() {
        var s_arr = array(length=length);
        for (var i = 0; i < length; i++) {
            s_arr[i] = arr[i];
        }
        return s_arr;
    }

    function double_size() {
        var big_arr = array(length = arr.size() * 2);
        for (var i = 0; i < arr.size(); i++) {
            big_arr[i] = arr[i];
        }
        arr = big_arr;
    }

    function half_size() {
        var sml_array = array(length = arr.size() / 2);
        for (var i = 0; i < sml_arr.size(); i++) {
            sml_arr[i] = arr[i];
        }
        arr = sml_arr;
    }
}


/*
 * Returns a new <List> instance, with initial elements *args
 */
function list(*args) {
    return new List(*args);
}

system.set_in(new NativeInputStream(system.native_in));
system.set_out(new NativeOutputStream(system.native_out));
system.set_err(new NativeOutputStream(system.native_err));

keyword run {
    "name" = "run",
    "number" = 1,
    "precedence" = 1
}
