import "sgl"
import "io"


class IDLE {

    var window;
    var code_area;

    function IDLE() {
        window = new sgl.Stage();
        var pane = new sgl.VBox();

        var menubar = new sgl.HBox();
        var choose_file = new sgl.Button("Choose File");
        choose_file.callback("command", function () {
            var file_name = sgl.ask_file_dialog({
                "*.sp" = "Slowest program file"
            });
            if (file_name !== null) {
                var stream = new io.TextInputStream(file_name);
                var text = stream.read();
                stream.close();
                code_area.clear();
                code_area.append_text(text);
            }
        });

        menubar.add_child(choose_file);
        code_area = new sgl.TextArea();

        pane.add_child(menubar);
        pane.add_child(code_area);

        var cmd_bar = new sgl.HBox();
        var run_btn = new sgl.Button("Run");
        run_btn.callback("command", function() {
            var text = code_area.get_text();
            eval(text);
        });

        cmd_bar.add_child(run_btn);
        pane.add_child(cmd_bar);

        window.set_root(pane);
        window.show();
    }
}


if (main()) {
    var idle = new IDLE();
}