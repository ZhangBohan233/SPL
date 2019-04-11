class A {
    var a = 0;
    def A() {}
}

var a = 0;
var b = a++;  // b = 0
var c = ++a;  // c = 2

println(b);
println(c);
println(--a);

var d = new A();
d.a++;
println(d);

for (0; d.a < 5; d.a += 1) println(d.a);
