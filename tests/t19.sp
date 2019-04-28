import "exception"


var lst = [1];

try {
    lst[1];
} catch (e: IndexError) {
    lst[0] = e;
}

println(lst);

class RTE extends exception.Exception {

}

try {
    throw new RTE;
} catch (e: exception.Exception) {
    println(e);
}
