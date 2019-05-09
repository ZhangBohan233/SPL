if __name__ == "__main__":
    from bin import spl_lexer, spl_ast, spl_interpreter

    file_name = "sample.sp"
    file_name = "samples/sample5.sp"
    f = open(file_name, "r")
    lexer = spl_lexer.Lexer(f)
    lexer.read()

    print(lexer.tokens)

    psr = lexer.parse()
    print(psr)

    block = spl_ast.BlockStmt()
    block.lines = psr.elements

    itr = spl_interpreter.Interpreter(block)
    print(itr.interpret())
    # print(itr.env.variables)
    print(itr.env.heap)
