import "json"

var t = json.from_string('{"3"="5", "2"="4", "4"=["1", "2", "3"]}');
println(t);
println(t instanceof List);

var s = json.to_json(t);
println(s);

json.write_file(t, "../json_test.json");
