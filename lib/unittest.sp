function testall() {
    var all_functions = get_all_tests();
    var run_before = all_functions[0];
    var run_after = all_functions[1];
    var functions = all_functions[2];
    var failed = pair();

    // run before
    for (var ftn; run_before) ftn();

    // tests
    for (var name; functions) {
        var test = functions[name];
        try {
            test();
        } catch (e: AssertionException) {
            failed[name] = e;
        }
    }

    // run after
    for (var ftn; run_after) ftn();

    var fail_num = failed.size();
    var result = fail_num > 0 ? "Failed" : "Passed";

    var total = functions.size();
    var passed = total - fail_num;
    println("Test %s. Passed: %d out of %d".format(result, passed, total));
    for (var failure; failed) {
        println("%s: %r".format(failure, failed[failure].message), system.stderr);
    }
}

function get_all_tests() {
    var functions = {};
    var run_before = [];
    var run_after = [];
    var vars = natives.variables();
    for (var key; vars) {
        var value = vars.get(key);
        if (value instanceof Function) {
            if (value.annotations.contains("Test")) {
                functions[key] = value;
            }
            if (value.annotations.contains("RunBefore")) {
                run_before.append(value);
            }
            if (value.annotations.contains("RunAfter")) {
                run_after.append(value);
            }
        }
    }
    return ~[run_before, run_after, functions];
}

function assert_equals(actual, expected) {
    if (actual != expected) {
        throw new AssertionException("Assertion failed. Expected %r, got %r".format(expected, actual));
    }
}
