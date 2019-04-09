import "exception"

if (main()) {
    var a = 5;
    var b = a + 2;
    println(b);
    var c = system.time();
    println(c);
    var d = !false;
    println(d);
    println(getcwf());
    try {
        throw new Exception("xxs");
    } catch (e: Exception) {
        println(e);
    }
}