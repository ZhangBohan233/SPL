function testall() {
    var functions = get_all_tests();
    var failed = pair();
    for (var name; functions) {
        var test = functions[name];
        try {
            test();
        } catch (e: AssertionException) {
            failed[name] = e;
        }
    }
    var fail_num = failed.size();
    var result = fail_num > 0 ? "Failed" : "Passed";

    var total = functions.size();
    var passed = total - fail_num;
    println("Test %s. Passed: %d out of %d".format(result, passed, total));
    for (var failure; failed) {
        println("%s: %r".format(failure, failed[failure]), system.stderr);
    }
}

function get_all_tests() {
    var functions = pair();
    var vars = natives.variables();
    for (var key; vars) {
        var value = vars.get(key);
        if (value instanceof Function && value.annotations.contains("Test")) {
            functions[key] = value;
        }
    }
    return functions;
}
