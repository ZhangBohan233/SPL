import "functions"
import "math"

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
