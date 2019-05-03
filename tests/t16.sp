class Node {
    var child;
    var value;

    function Node(v) {
        value = v;
    }

    function get_child() {
        return child;
    }

    function set_child(c) {
        child = c;
    }

    function __str__() {
        return "Node %r (%r)".format(value, child);
    }
}

if (main()) {
    var a = new Node(1);
    var b = new Node(2);
    a.set_child(b);
    println(a.get_child().get_child());
    a.get_child().child = new Node(3);
    var a.g = function() {println("ggg");}
    println(a.get_child().get_child());
    println(a);
    a.g();
}
