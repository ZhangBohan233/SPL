import "sgl"
import "io"


class TextAreaOutputStream extends OutputStream {

    var field;
    var tag;

    function TextAreaOutputStream(text_area, tag) {
        field = text_area;
        this.tag = tag;
    }

    @Override
    function write(obj) {
        field.append_text(string(obj), tag);
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
            var exit_value = eval(text);
            println("Process finished with exit value " + string(exit_value));
        });

        pane.add(code_area);

        cmd_bar.add(run_btn);
        pane.add(cmd_bar);

        output_area = new sgl.TextArea(pane);
        pane.add(output_area);

        output_area.tag('stdout');
        output_area.tag('stderr', foreground="red");

        system.set_out(new TextAreaOutputStream(output_area, 'stdout'));
        system.set_err(new TextAreaOutputStream(output_area, 'stderr'));

        window.set_menu(menubar);
        window.set_root(pane);
        window.show();
    }
}


if (main()) {
    var idle = new IDLE();
}