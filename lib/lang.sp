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

class NativeInputStream extends InputStream {

    var ns;

    function NativeInputStream(stream) {
        ns = stream;
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


system.set_in(new NativeInputStream(system.native_in));
system.set_out(new NativeOutputStream(system.native_out));
system.set_err(new NativeOutputStream(system.native_err));
