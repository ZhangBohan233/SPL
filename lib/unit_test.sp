function testall() {
    var functions = get_all_tests();
    var failed = 0;
    for (var test; functions) {
        try {
            test();
        } catch (e: AssertionException) {
            println(e);
            failed++;
        }
    }
    var result = failed > 0 ? "Failed" : "Passed";

    var total = functions.length();
    var passed = total - failed;
    println("Test %s. Passed: %d out of %d".format(result, passed, total));
}

function get_all_tests() {
    var functions = list();
    var vars = natives.variables();
    for (var key; vars) {
        var value = vars.get(key);
        if (value instanceof Function && value.annotations.contains("Test")) {
            functions.append(value);
        }
    }
    return functions;
}
