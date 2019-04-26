var lst = [1];

try {
    lst[1];
} catch (e: IndexError) {
    lst[0] = e;
}