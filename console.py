from bin import spl_lexer as lex, spl_token_lib as stl, spl_parser as psr, spl_interpreter
import script
import os
import sys


def print_waring(msg):
    sys.stderr.write(str(msg) + "\n")
    sys.stderr.flush()


if __name__ == "__main__":

    line_terminated = True

    lex2 = lex.Tokenizer()

    lex2.setup(script.get_spl_path(), "console", script.get_spl_path(), import_lang=True)
    itr = spl_interpreter.Interpreter([], os.getcwd(), "utf8", (sys.stdin, sys.stdout, sys.stderr))

    # Makes the interpreter import the "lang.sp"
    lex2.tokenize([])
    parser_ = psr.Parser(lex2.get_tokens())
    block = parser_.parse()
    itr.set_ast(block)
    itr.interpret()
    lines = []

    lex2.import_lang = False

    def error_handler(e2):
        raise e2

    itr.set_error_handler(error_handler)

    while True:
        if line_terminated:
            line = input(">>> ")
        else:
            line = input("... ")
        lines.append(line)

        try:
            lex2.tokenize(lines)

            parser_ = psr.Parser(lex2.get_tokens())
            block = parser_.parse()

            itr.set_ast(block)
            res = itr.interpret()
            if res is not None:
                print(res)

            lines.clear()
            line_terminated = True
        except stl.ParseException as e:
            if len(line) > 0:
                line_terminated = False
            else:
                print_waring(e)
                lines.clear()
                line_terminated = True
        except Exception as e:
            print_waring(e)
            lines.clear()
            line_terminated = True
