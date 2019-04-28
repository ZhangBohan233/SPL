import namespace "queue"


class Test {
    abstract function get_name();
}

class TestObj extends Test {

    var value;
    const name = "TestObj";

    function TestObj(value) {
        this.value = value;
    }

    function print_value() {
        println(value);
    }

    @Override
    function get_name() {
        return name;
    }

    function get_value() {
        return value;
    }

    function fun() {
        value++;
        return this;
    }
}

if (main()) {
    const t1 = system.time();

    var link_lst = new LinkedList();
    for (var i = 0; i < 5000; i++) {
        var obj = new TestObj(i);
        obj.fun();
        link_lst.add_last(obj);
    }

    const t2 = system.time();
    print("object: ");
    println(t2 - t1);
    link_lst.last().fun().fun();
    println(link_lst.last().get_value());
}
