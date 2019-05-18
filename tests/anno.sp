@Suppress("kind"="all", "s"=123)
@Override
function f() {

}

@Suppress
function g(x) {

}

class Clazz {
    abstract function up();
}

class B extends Clazz {
    @Override
    function up() {
        println(123);
    }
}

g(2);
var c = new B;
c.up();
println(f.annotations);
for (var x; f.annotations) {
    println(x.params);
}
