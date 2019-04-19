import "math"
import "functions"

const t1 = system.time();
var a = fib(20);
const t2 = system.time();
println(a);
println(t2 - t1);

function f(a, b, c=0, d=1, e=2) {
    println(sum([a, b, c, d, e]));
}

f(e = 3, 1, 2, 3, 4);
