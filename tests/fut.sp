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

@Test
function instance_test2() {
    assert 1 instanceof int;
}

@Test
function if_else_test() {
    const score = 78;
    var gpa;
    if (score >= 85) gpa = 4.0;
    else if (score >= 82) gpa = 3.7;
    else if (score >= 80) gpa = 3.3;
    else if (score >= 77) {
        gpa = 3.0;
    } else if (score >= 73) gpa = 2.7;
    else throw new Exception("You are trash");

    assert gpa == 3.0;
}

class TestException extends Exception {
    function TestException(msg) {
        Exception(msg);
    }
}

@Test("exception" = TestException)
function test_exception() {
    throw new TestException("What");
}

unittest.testall();
