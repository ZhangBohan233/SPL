import "sgl"

var window = new sgl.Stage();

var root_node = new sgl.VBox();
root_node.background("red");
root_node.set_width(100);
root_node.set_height(100);

var label = new sgl.Label("Gan ni niang");
root_node.add_child(label);

var entry = new sgl.TextField();
root_node.add_child(entry);

var btn = new sgl.Button("Button");
btn.callback("command", function () {
    println(111);
});
root_node.add_child(btn);

println(root_node.node.tk);

window.set_root(root_node);
window.show();
