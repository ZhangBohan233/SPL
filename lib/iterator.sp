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
