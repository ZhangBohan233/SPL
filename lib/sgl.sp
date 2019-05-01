class Stage {

    var window;
    var root;

    function Stage() {
        window = new Window();
    }

    function set_root(root) {
        this.root = root;
        window.set_root(root.node);
    }

    function show() {
        window.show();
    }
}


/*
 *
 */
abstract class Node {

    var node;  // Graphic

    function Node(node) {
        this.node = node;
    }

    function set_parent(parent) {
        node.set_attr("master", parent.node.tk);
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

    function VBox() {
        Pane(new Graphic("Frame"));
    }

    function add_child(n) {
        n.set_parent(this);
        n.node.call("grid", [], {"row"=children.size(), "column"=0});
        children.append(n);
    }
}


class HBox extends Pane {

    function HBox() {
        Pane(new Graphic("Frame"));
    }

    function add_child(n) {
        n.set_parent(this);
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

    function Label(text="") {
        Node(new Graphic("Label"));
        set_text(text);
    }
}


class TextField extends Node {

    function TextField() {
        Node(new Graphic("Entry"));
    }

    function get() {

    }
}


class TextArea extends Node {

    function TextArea() {
        Node(new Graphic("Text"));
    }

    function append_text(text) {
        node.call("insert", ["'end'", "'''" + text + "'''"], {});
    }

    function clear() {
        node.call("delete", ["'1.0'", "'end'"], {});
    }

    function get_text() {
        return node.call("get", ["'1.0'", "'end'"], {});
    }
}


class Button extends LabelAble {

    function Button(text="") {
        Node(new Graphic("Button"));
        set_text(text);
    }

    function callback(command, ftn) {
        node.callback(command, ftn);
    }
}


function ask_file_dialog(types={}) {
    return (new Graphic("Button")).file_dialog(types);
}
