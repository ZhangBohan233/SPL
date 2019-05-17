class A {
    private var t = 0;

    function A(t) {
        this.t = t;
    }
}

var x = new A;
var y = new A(2);
println(x);
println(y);
