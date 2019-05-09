import "dirs.lib.sp"
import "user.sp"


//namespace functions;

//println(user);

//var i = 5;

//user.func();


var user.d = new user.A(true);
//user.c = 6;
var e = new user.A;
println(user.d);
println(e);
//println(user.d.get_value());

class B extends user.A {
    const d;
    function B() {
        A(true);
    }
}

if (main()) {
    println("main is main");
    //println(user.functions.map(function (x) {-x}, [1, 2, 3, 4]));
    var b = new B();
    println(b);
}
