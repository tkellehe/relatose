import sys
sys.path.insert(0, '..')
from transpiler import transpiler

parser = transpiler.Parser()

def tokenize_basics(tkn):
    tkn.props.lines = []

def tokenize(tkn):
    def interpreter(tkn):
        tkn.props.lines.append("tape[index] = (tape[index] + " + len(tkn.literal.value) + ") % 256")
    tokenize_basics(tkn)
    tkn.interpret = interpreter
parser.add(transpiler.Snippet(transpiler.REGEXIFY("(?P<literal>\++)"), tokenize))


def main():
    executable = parser.parse_left_to_right(sys.argv[1])

    code = """
    import sys
    input = sys.argv[1] if len(sys.argv) > 1 else ""
    next = 0
    ascii = \"\"\"
     !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~\"\"\"

    def stdout(char_value):
        print(ascii[char_value], end='', flush=True)
    def stdin():
        return (ord(input[next])%256) if next < len(input) else return 0
    def main():
        tape = [0]
        index = 0

    """

    indent = 1
    for tkn in executable.tokens:
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

    sys.argv[1] = sys.argv[2] if len(sys.argv) > 2 else ""

    #exec(code)
    print(code)

if __name__ == '__main__':
    main()
