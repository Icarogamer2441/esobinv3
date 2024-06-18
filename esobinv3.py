import sys
import compiler

def interpret(code):
    lines = code.split("\n")
    binpos = 0

    for line in lines:
        tokens = list(line)

        for token in tokens:
            if token == "1":
                binpos += 4
            elif token == "0":
                binpos -= 3
            elif token == "2":
                compiler.asciimsg(binpos)
            elif token == "3":
                compiler.msg(f"{binpos}")

if __name__ == "__main__":
    version = "1.0"
    if len(sys.argv) == 1:
        print(f"esobinv2 {1.0}")
        print(f"Usage: {sys.argv[0]} <file>")
    else:
        if sys.argv[1].endswith(".ebin3"):
            with open(sys.argv[1], "r") as f:
                outname = sys.argv[1].replace(".ebin3", "")
                compiler.start(outname)
                interpret(f.read())
                compiler.end()
        else:
            print("Use .ebin3 file extension")
