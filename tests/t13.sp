var lst = [1, 2, 3, [4, 5, {"a"=5}]];

var b = lst[3][2]["a"];
println(b);
var k = "a";
lst[3][2][k] = 99;
println(lst);
