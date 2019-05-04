import "sgl"

class MemoryViewer {

    var base_env;
    var window;
    var tree;

    function MemoryViewer(env) {
        base_env = env;
        window = new sgl.Window();
        tree = new sgl.TreeView(window);
        tree.set_height(30);
        tree.columns(4);
        tree.column_width(2, 300);
        tree.column_heading(0, "Name");
        tree.column_heading(1, "Type");
        tree.column_heading(2, "Content");
        tree.column_heading(3, "Note");
        window.set_root(tree);
    }

    function browse(name, obj, parent) {
        var child = append(name, obj, parent);
        if (obj instanceof EnvWrapper) {
            for (var attr; obj.attributes()) {
                browse(attr, obj.get(attr), child);
            }
        } else if (obj instanceof Object || obj instanceof Module) {
            var sub_env = get_env(obj);
            for (var attr; sub_env.attributes()) {
                if (attr != "this") {
                    browse(attr, sub_env.get(attr), child);
                }
            }
        }
    }

    function append(name, obj, parent) {
        return tree.add_item(name, ~[type(obj), string(obj)], parent)
    }

    function show() {
        browse("root", base_env, "");
        window.show();
    }
}

function memory_view(env) {
    var mv = new MemoryViewer(env);
    mv.show();
}
