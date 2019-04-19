var d = {
    "a" = 1,
    3 = 4,
    "c" = {1, 2, {5}}
}

function f(d1, d2={}) {
    println(d1);
    println(d2);
}

f({'1'='g'}, d);

var lst = [1, "a", 3, [9, 9], {1 = f({}), 2 = 3}];
println(lst);
println(lst[4][2]);