import ast

def parse_file(filename):
    with open(filename, "r") as f:
        src = f.read()
        
    print(ast.dump(ast.parse(src), indent=4))

if __name__ == "__main__":
    parse_file("test/3420.py")
    