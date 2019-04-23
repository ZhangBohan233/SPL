//import "math"
import "functions"


function f(a, b, c=0, d=1, e=2) {
    println(sum([a, b, c, d, e]));
}

//f(e = 3, 1, 2, 3, 4);

function g(*args, **kwargs) {
    println(args);
    println(f(*args));
    println(kwargs);
}

g(1, 2, 3, 4, b=2);
