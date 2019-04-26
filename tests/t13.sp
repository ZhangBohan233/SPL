class X {
    function __getitem__(index) {
        return index;
    }

    function __setitem__(index, value) {
        println( index + value);
    }
}


if (main()) {
    //var lst = [1, 2, 3, [4, 5, {"a"=5}]];

    //var b = lst[3][2]["a"];
    //println(b);
    //var k = "a";
    //lst[3][2][k] = 99;
    //println(lst);

    var cache = [];
    var lst2 = [11,12,13,14,15,16,17,18,19,20];
    for (var i = 0; i < 10; i++) {
        cache.append(i);
    }
    var x = lst2.size();
    for (var i = 0; i < 10; i++) {
        lst2[x - i - 1] = cache[i];
    }
    println(cache);
    println(lst2);

    var xx = new X;
    println(xx[2]);
    xx[2] = 3;
}