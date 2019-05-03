import "sgl"
import "io"


class TextAreaOutputStream extends OutputStream {

    var field;

    function TextAreaOutputStream(text_area) {
        field = text_area;
    }

    @Override
    function write(obj) {
        field.append_text(string(obj));
    }

    @Override
    function flush() {

    }

    @Override
    function close() {

    }
}


class IDLE {

    var window;
    var code_area;
    var output_area;

    function IDLE() {
        window = new sgl.Window();
        var pane = new sgl.VBox(window);

        var menubar = new sgl.MenuBar(window);
        var file_menu = new sgl.Menu(menubar);

        file_menu.add_item("Open File", function () {
            var file_name = sgl.ask_file_dialog({
                "*.sp" = "Slowest program file"
            });
            try {
                var stream = new io.TextInputStream(file_name);
                var text = stream.read();
                stream.close();
                code_area.clear();
                code_area.append_text(text);
            } catch (e: io.IOException) {
                println(e);
            }
        });

        menubar.add_menu(file_menu, "File");
        code_area = new sgl.TextArea(pane);

        var cmd_bar = new sgl.HBox(pane);
        cmd_bar.align(sgl.ALIGN_LEFT);
        var run_btn = new sgl.Button(cmd_bar, "Run");
        run_btn.callback("command", function() {
            var text = code_area.get_text();
            eval(text);
        });

        pane.add(code_area);

        cmd_bar.add(run_btn);
        pane.add(cmd_bar);

        output_area = new sgl.TextArea(pane);
        pane.add(output_area);

        system.set_out(new TextAreaOutputStream(output_area));

        window.set_menu(menubar);
        window.set_root(pane);
        window.show();
    }
}


if (main()) {
    var idle = new IDLE();
}