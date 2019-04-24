import spl_interpreter
import spl_lexer as lex
import spl_token_lib as stl
import spl_parser as psr
import os
import sys


def print_waring(msg):
    sys.stderr.write(str(msg) + "\n")
    sys.stderr.flush()


if __name__ == "__main__":

    line_terminated = True

    lex2 = lex.Tokenizer()
    itr = spl_interpreter.Interpreter([], os.getcwd(), "utf8")
    lines = []

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
