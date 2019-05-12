// Full unittests

import "unittest"

@Test
function test_cal() {
    assert 1 + 2 == 3;
    assert 3 / (2 + 1) == 1;
}

@Test
function test_fail() {
    unittest.assert_equals(1, 2);
}

@Test
function test_fail_native() {
    assert 2 == 3;
}

@Test
function test_triple_equal() {
    assert 2 == 2 == true;
}

@Test
function test_ternary() {
    var a = 1 == 2 ? "a" : "b";
    assert a == "b";
}

@Test
function test_increment() {
    var a = 5;
    var b = a++ + ++a;
    assert b == 12;
}

@Test
function instance_test() {
    assert true instanceof boolean;
}

unittest.testall();
