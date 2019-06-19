fn run(arg1, *args) {
    println(arg1);
    for (var a; args) {
        println(a);
    }
}

if (main()) {
    run(1, 2, 3);
}
