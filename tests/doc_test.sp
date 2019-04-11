/*
 * This is the new test.
 */
class Clazz {

    /*
     * This is an attribute.
     */
    var a = 0;
    var b;

    /*
     * This is the constructor.
     * Okay.
     */
    function Clazz() {

    }

    function other() {

    }
}

/*
 * This is the doc of a single function.
 *
 * @param a: the parameter
 * @return: something
 */
function foo(a, b=true) {
    return a;
}

foo(3);
help(foo);
help(Clazz);
help(list);
println("223", system.stdout);

var a = input("fuck you?");
println(a);
