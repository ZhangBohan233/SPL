import namespace "math"
import namespace "functions"

const st = system.time();

function f(x) {
    return sum(map(function (n) {comb(x, n)}, new RangeIterator(0, x + 1, 1)));
}

var veg = f(19);
var meat = f(20);
var che = f(6);
var other = f(6);

var total = 4 * 6 * 12 * 4 * veg * meat * che * other;
println(total);

var days = total / 30;
var b_years = float(days) / 365 / pow(10, 9);
println(b_years);
println(13.799 / b_years);

var universe_days = 13.799 * (pow(10, 9));
println(universe_days);

const end = system.time();
println(end - st);

println(fact(0));
const e2 = system.time();
println(e2 - end);
