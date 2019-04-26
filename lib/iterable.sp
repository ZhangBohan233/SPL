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


/*
 * The sign of iteration ends.
 */
class StopIteration {
    function StopIteration() {
    }
}
