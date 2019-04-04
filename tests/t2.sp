class A {
    var a = 1;
    def A() {
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

var a = new A();
var b = new A();
println(b[3]);
