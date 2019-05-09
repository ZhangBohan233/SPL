import "io"

var stream = new io.TextInputStream("t18.sp");
var t = stream.read();
stream.close();

println(t);

println(eval(t));

