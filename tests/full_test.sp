import "functions"
import "math"
import "queue"

/*
 * This is the doc of a single function.
 *
 * @param a: the parameter
 * @param b: the b
 * @param c: the c
 * @return: the sum of a, b, c
 */
function foo(a, b=0, c=1) {
    return a + b + c;
}

println(foo(3));

// decorator test
function decorator(func, dec) {
    return function(*args, **kwargs) {
        dec();
        return func(*args, **kwargs);
    }
}

var decorated_foo = decorator(foo, function(){println(555)});
println(decorated_foo(2, 3));

const k = 0;
var r;
if (k > 5) {
    r = 0;
} else if (k > 2) {
    r = 1;
} else if (k > 0) {
    r = 2;
} else {
    r = 3;
}
assert r == 3;
var y = r != 3 ? "a" : decorated_foo(3, 5);
println(y);

var q = new LinkedList();
for (var i = 0; i < 10; ++i) {
    q.add_last(i);
}
for (var x; q) {
    print("%d ".format(x));
}
println();

abstract class Interface {
    abstract function test();
}

class Super {
    var v1;

    function Super(v1) {
        this.v1 = v1;
    }
}

class Clazz extends Super, Interface {
    function Clazz() {
        Super(3);
    }
}

var clazz = new Clazz();
println(clazz);
try {
    clazz.test();
} catch (e: AbstractMethodException) {
    println(e);
} finally {
    println(233);
}

clazz.test = function () {
    return ++clazz.v1;
}

println(clazz.test());

/*
 * This is the new test.
 */
class Clazz2 extends Clazz {

    var a = 0;
    var b;

    /*
     * This is the constructor.
     * Okay.
     */
    function Clazz2() {
        Clazz();
    }

    function other() {

    }
}

abstract function g();

if (main) {
    println(foo(3), system.stderr);
    help(foo);
    help(Clazz2);
    help(list);
    println(gcd(398, -298));
    println(log(5));
    println(log(8, 2));
    println(E);
    help(natives);
    var v = 1 + 2 * 3 - 2;
    println(v);
}
