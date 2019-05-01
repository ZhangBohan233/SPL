var lst = [1];

try {
    lst[1];
} catch (e: IndexError) {
    lst[0] = e;
}

println(lst);

class RTE extends Exception {

}

try {
    throw new RTE;
} catch (e: IndexError) {
    println(111);
} catch (e: Exception) {
    println(223);
}
