import "math"
import "unittest"


var n;

@RunBefore
function setup() {
    n = 360;
}

@RunAfter
function clean() {
    n = 0;
    println("Finished with " + string(n));
}


@Test
function test_euler_phi() {
    assert euler_phi_fp(n) == 96;
}


if (main()) {
    const t1 = system.time();
    println(euler_phi_fp(360));
    const t2 = system.time();
    println(t2 - t1);

    println(deg(PI));
    println(rad(180));
    println(sin(1));

    testall();
}
