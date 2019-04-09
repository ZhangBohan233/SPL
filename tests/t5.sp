function b(x) {
    return function (y) {
        return function (z) {return x + y + z};
    }
}

var c = b(3)(2)(1);
println(c);

class A {
    var x;
    def A(x) {
        this.x = x;
    }

    def change(x) {
        this.x = x;
        return this;
    }

    function __getitem__(index) {
        return index;
    }

    function __setitem__(index, value) {
        return index + value;
    }

    operator +(o) {
        println(x + 1);
    }
}

var d = new A(3);
d.change(4).change(5).change(77);
println(d.x);
d + 1;

var e = list(1, 2, 3, 4);
println(e[1]);
println(e);
