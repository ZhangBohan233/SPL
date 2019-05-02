
/*
 *
 */
abstract class Node {

    var node;  // Graphic

    function Node(node) {
        this.node = node;
    }

    function update() {
        node.call("update", [], {});
    }
}

class Window extends Node {

    function Window() {
        node = new Graphic("Tk")
    }

    function set_root(root) {
        root.node.call("grid", [], {});
    }

    function show() {
        node.call("mainloop", [], {});
    }
}

abstract class Pane extends Node {

    var children = [];

    function Pane(node) {
        Node(node);
    }

    function set_width(width) {
        node.configure("width", width);
    }

    function set_height(height) {
        node.configure("height", height);
    }

    function background(color) {
        node.set_bg(color);
    }
}

class VBox extends Pane {

    function VBox(parent) {
        Pane(new Graphic("Frame", parent.node));
    }

    function add(n) {
        n.node.call("grid", [], {"row"=children.size(), "column"=0});
        children.append(n);
    }
}


class HBox extends Pane {

    function HBox(parent) {
        Pane(new Graphic("Frame", parent.node));
    }

    function add(n) {
        n.node.call("grid", [], {"row"=0, "column"=children.size()});
        children.append(n);
    }
}


abstract class LabelAble extends Node {
    function set_text(text) {
        node.configure("text", text);
    }

    function get_text() {
        return node.get("text");
    }
}


class Label extends LabelAble {

    function Label(parent, text="") {
        Node(new Graphic("Label", parent.node));
        set_text(text);
    }
}


class TextField extends Node {

    function TextField(parent) {
        Node(new Graphic("Entry", parent.node));
    }

    function get() {

    }
}


class TextArea extends Node {

    function TextArea(parent) {
        Node(new Graphic("Text", parent.node));
    }

    function append_text(text) {
        node.call("insert", ["'end'", "'''" + text + "'''"], {});
        node.call("see", ["'end'"], {});
        update();
    }

    function clear() {
        node.call("delete", ["'1.0'", "'end'"], {});
    }

    function get_text() {
        return node.call("get", ["'1.0'", "'end'"], {});
    }
}


class Button extends LabelAble {

    function Button(parent, text="") {
        Node(new Graphic("Button", parent.node));
        set_text(text);
    }

    function callback(command, ftn) {
        node.callback(command, ftn);
    }
}


function ask_file_dialog(types={}) {
    return (new Graphic("Button", null)).file_dialog(types);
}
