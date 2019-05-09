import namespace "functions"

function func() {
    for (var i = 0; i < 5; i++) {
        println(i);
    }
}

var c = 123;

class A {

    var value = c;
    var even;

    function A(even) {
        this.even = even;
    }

    function get_value() {
        return value;
    }
}

if (main()) {
    println("user is main");
}
