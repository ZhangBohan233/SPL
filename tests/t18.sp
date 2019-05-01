import "queue"

if (main()) {
    var iter = new RangeIterator(0, 8, 1);
    var s;
    while (iter.__more__()) {
        s = iter.__next__();
        println(s);
    }

    var ll = new queue.LinkedList();
    ll.push(1);
    ll.push(2);
    ll.push(3);
    for (var x; ll) {
        print(x);
    }
}
