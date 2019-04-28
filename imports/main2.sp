import "dirs.lib.sp" as db
import namespace "user.sp"

namespace db;

println(functions.map(function (a) {-a}, []));

var a = c;
for (var i = 0; i < 1000; i++) {
    c++;
}

println(c);
user.c = 6;
println(a);

var x = fuck(1, 2);
println(x);
println(db.x);
