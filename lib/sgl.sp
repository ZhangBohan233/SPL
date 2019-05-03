
/*
 *
 */
abstract class Node {

    var node;  // Graphic

    function Node(node) {
        this.node = node;
    }

    function update() {
        node.call("update");
    }
}

class Window extends Node {

    function Window() {
        node = new Graphic("Tk")
    }

    function set_root(root) {
        root.node.call("grid");
    }

    function set_menu(menu) {
        node.configure("menu", menu.node.tk);
    }

    function show() {
        node.call("mainloop");
    }
}

abstract class Container extends Node {

    var children = [];

    function Container(node) {
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

class VBox extends Container {

    function VBox(parent) {
        Container(new Graphic("Frame", parent.node));
    }

    function add(n) {
        n.node.call("grid", row=children.size(), column=0);
        children.append(n);
    }
}


class HBox extends Container {

    function HBox(parent) {
        Container(new Graphic("Frame", parent.node));
    }

    function add(n) {
        n.node.call("grid", row=0, column=children.size());
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
        node.call("insert", "end", text);
        node.call("see", "end");
        update();
    }

    function clear() {
        node.call("delete", "1.0", "end");
    }

    function get_text() {
        return node.call("get", "1.0", "end");
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


class MenuBar extends Node {

    function MenuBar(parent) {
        Node(new Graphic("Menu", parent.node));
    }

    function add_menu(menu, name) {
        node.call("add_cascade", label=name, menu=menu.node.tk);
    }
}


class Menu extends Node {

    function Menu(parent) {
        Node(new Graphic("Menu", parent.node));
        node.configure("tearoff", 0);
    }

    function add_item(name, ftn) {
        node.call("add_command", label=name, command=ftn);
    }

    function add_separator() {
        node.call("add_separator");
    }
}


function ask_file_dialog(types={}) {
    return (new Graphic("Button", null)).file_dialog(types);
}
