import namespace "math"
import namespace "functions"
import namespace "queue"

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

var decorated_foo = decorator(foo, function(){println("Decorated")});
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

    function over() {
        println("Clazz over")
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

    @Override
    function over() {
        println("Clazz2 Over!");
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
    help(List);
    println(math.gcd(398, -298));
    println(math.log(5));
    println(math.log(8, 2));
    println(math.E);
    help(natives);
    var v = 1 + 2 * 3 - 2;
    println(v);
}

var file0 = f_open("t.txt", "r");
var text = file0.read();
file0.close();
println(text);
println(type(file0));
println(type(text));
println(file0 instanceof File);
println(1 instanceof int);
println("ss" instanceof String);
println(1 instanceof Object);

try {
    var file2 = f_open("E:\GgGg.txt");
    var text2 = file2.read();
    file2.close();
    println(text2);
} catch (err: IOException) {
    println(err);
}

println(type(system));
var c2 = new Clazz2;
c2.over();
println(c2 instanceof Object);

function whole(dic) {
    println(dic);
}

whole({'1'='g', true={"f"=1, r="r", 99={3, 5, false}}});

var kk = "k";
var lst = [{1, 2, 3, 1}, "dd", [3, 2, 1], {"a"=5, "b"={kk=6}}];
println(lst[2][1]);
println(lst[3]["b"][kk]++);
println(lst);

println(dir(Clazz2));
println(dir(List));
