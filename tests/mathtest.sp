import "math"


if (main()) {
    const t1 = system.time();
    println(euler_phi_fp(360));
    const t2 = system.time();
    println(t2 - t1);
}
