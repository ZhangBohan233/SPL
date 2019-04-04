import "exception"

if (main()) {
    var a = 5;
    var b = a + 2;
    println(b);
    var c = system.time();
    println(c);
    var d = !false;
    println(d);
    try {
        throw new Exception;
    } catch (e: Exception) {
        println(e);
    }
}