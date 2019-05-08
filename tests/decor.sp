//import "math"
import "functions"


function f(a, b, c=1, d=2) {
    println([a, b, c, d]);
}

//f(e = 3, 1, 2, 3, 4);

class A {
    function __kw_unpack__() {
        return {"d" = 4, "c" = 9};
    }
}

function g(*args, **kwargs) {
    println(args);
    f(*args, **kwargs);
    println(kwargs);
    //println(kwargs["c"]);
}

g(1, 2, **(new A));
