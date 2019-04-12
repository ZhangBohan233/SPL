/*
 * Superclass of all iterable classes.
 *
 * Iterable are typically used when calling for (iterable; )
 */
abstract class Iterable {

    /*
     * Returns an object to be iterated.
     */
    abstract function __iter__();

    /*
     * Returns the next iteration.
     */
    abstract function __next__();
}


/*
 * The sign of iteration ends.
 */
class StopIteration {
    function StopIteration() {
    }
}
