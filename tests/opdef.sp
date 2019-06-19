keyword fun {
    "name" = "fun",
    "number" = 2,
    "precedence" = 2
}

keyword run {
    "name" = "run",
    "number" = 1,
    "precedence" = 1
}

class A {
    function __fun__(b) {
        println(123);
    }

    operator 1 run() {
        println(334);
    }
}

var a = new A;
var b = new A;
a fun b;
run a;

//eval("println(1+3)");
run "../idle.sp";
