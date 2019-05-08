import "unittest"

class Clazz {
    function Clazz() {

    }

    @Suppress
    @Test
    function test() {

    }
}

var s = set(1, 4, 1, 3);
println(s);
var c = new Clazz();
println(c.test.annotations);

@Test
function test1() {
    assert 1 == 1;
}

@Test
function test2() {
    assert 3 > 4;
}

testall();
