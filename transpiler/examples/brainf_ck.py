import transpiler
import sys

parser = transpiler.Parser()

def tokenize_basics(tkn):
    tkn.props.lines = []

def tokenize(tkn):
    def interpreter(tkn):
        tkn.props.lines.append("tape[index] = (tape[index] + " + len(tkn.literal.value) + ") % 256")
    tokenize_basics(tkn)
    tkn.interpret = interpreter
parser.add(Snippet(transpiler.REGEXIFY("(?P<literal>\++)"), tokenize))


def main():
    script.parse_left_to_write(sys.argv[1])

    code = """
    import sys
    def stdout(char):
        print(char, end='', flush=True)
    def stdin():
        return 0
    def main():
        tape = [0]
        index = 0
        input = sys.argv[1] if len(sys.argv) > 1 else ""
        ascii = \"\"\"
         !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~\"\"\"


    """

    indent = 1
    for tkn in script.tokens:
        for line in tkn.props.lines:
            if type(line) is tuple and len(line[1]):
                indent += line[0]
                code += ("    " * indent) + line[1] + "\n"
            elif len(line):
                code += ("    " * indent) + line + "\n"

    code += """

    if __name__ == '__main__':
        main()
    """

if __name__ == '__main__':
    main()
