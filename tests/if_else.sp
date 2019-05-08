if (true) println(1);
else println(0);

var age = 5;
var grade;

if (age > 25 || age < 18) {
    grade = 0;
} else if (age > 24)
    grade = 5;
else if (age > 23) grade = 4;
else if (age > 22) grade = 3;
else if (age > 21) {
    grade = 2;
} else {
    grade = 1;
}

println(grade);

if (true)
    if (false)
        println(100);
    else
        println(200);

for (var i = 0; i < 10; i++) print(i);
println();
for (var i = 0; i < 10; ++i) print(i);
