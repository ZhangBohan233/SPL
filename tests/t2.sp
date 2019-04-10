class Obj {
    abstract function Obj();
}

class A extends Obj {
    var a = 1;
    def A(a) {
        this.a = a;
    }

    def copy() {
        return new A(a);
    }

    def __add__(o) {
        return a + o.a;
    }

    operator -(o) {
        return a - o.a;
    }

    def __getitem__(i) {
        return 44 + i;
    }
}

var a = new A(3);
var b = new A(4);
var c = a.copy();
a.a = 5;
println(c);
println(a);
