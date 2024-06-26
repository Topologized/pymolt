import ast
import re
import random
import io
import tokenize
import os

FUNC_NAMES = []

with open("function_names.txt") as f:
    while (s := f.readline()):
        FUNC_NAMES.append(s.strip())

VAR_NAMES = []

with open("var_names.txt") as f:
    while (s := f.readline()):
        VAR_NAMES.append(s.strip())


def remove_docs(source):
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        if token_type == tokenize.COMMENT:
            pass
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    out = '\n'.join(l for l in out.splitlines() if l.strip())
    return out

def do_rename(pairs, code):
    for key in pairs:
        code = re.sub(fr"\b({key})\b", pairs[key], code, re.MULTILINE)
    return code

def _rename(filename: str):
    with open(filename, "r") as file:
        code = file.read()
        code = remove_docs(code)
        parsed = ast.parse(code)

    funcs = {
        node for node in ast.walk(parsed) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    # classes = {
    #     node for node in ast.walk(parsed) if isinstance(node, ast.ClassDef)
    # }
    args = {
        node.id for node in ast.walk(parsed) if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load)
    }
    # attrs = {
    #     node.attr for node in ast.walk(parsed) if isinstance(node, ast.Attribute) and not isinstance(node.ctx, ast.Load)
    # }
    for func in funcs:
        if func.args.args:
            for arg in func.args.args:
                args.add(arg.arg)
        if func.args.kwonlyargs:
            for arg in func.args.kwonlyargs:
                args.add(arg.arg)
        if func.args.vararg:
            args.add(func.args.vararg.arg)
        if func.args.kwarg:
            args.add(func.args.kwarg.arg)

    pairs = {}
    used = set()
    for func in funcs:
        if func.name == "__init__":
            continue
        newname = random.choice(FUNC_NAMES)
        while newname in used:
            newname = random.choice(FUNC_NAMES)
        used.add(newname)
        print(F"New function name: {newname}")
        pairs[func.name] = newname

    for arg in args:
        newname = random.choice(VAR_NAMES)
        while newname in used:
            newname = random.choice(VAR_NAMES)
        used.add(newname)
        print(F"New variable name: {newname}")
        pairs[arg] = newname

    string_regex = r"('|\")[\x1f-\x7e]{1,}?('|\")"

    original_strings = re.finditer(string_regex, code, re.MULTILINE)
    originals = []

    for matchNum, match in enumerate(original_strings, start=1):
        originals.append(match.group().replace("\\", "\\\\"))

    placeholder = os.urandom(16).hex()
    code = re.sub(string_regex, f"'{placeholder}'", code, 0, re.MULTILINE)

    for i in range(len(originals)):
        for key in pairs:
            originals[i] = re.sub(r"({.*)(" + key + r")(.*})", "\\1" + pairs[key] + "\\3", originals[i], re.MULTILINE)

    while True:
        found = False
        code = do_rename(pairs, code)
        for key in pairs:
            if re.findall(fr"\b({key})\b", code):
                found = True
        if found == False:
            break


    replace_placeholder = r"('|\")" + placeholder + r"('|\")"
    for original in originals:
        code = re.sub(replace_placeholder, original, code, 1, re.MULTILINE)

    return code

def _rename2(filename: str):
    with open(filename, "r") as file:
        code = file.read()
        code = remove_docs(code)
        parsed = ast.parse(code)

    funcs = {
        node for node in ast.walk(parsed) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    classes = {
        node for node in ast.walk(parsed) if isinstance(node, ast.ClassDef)
    }
    args = {
        node.id for node in ast.walk(parsed) if isinstance(node, ast.Name) and not isinstance(node.ctx, ast.Load)
    }
    attrs = {
        node.attr for node in ast.walk(parsed) if isinstance(node, ast.Attribute) and not isinstance(node.ctx, ast.Load)
    }
    for func in funcs:
        if func.args.args:
            for arg in func.args.args:
                args.add(arg.arg)
        if func.args.kwonlyargs:
            for arg in func.args.kwonlyargs:
                args.add(arg.arg)
        if func.args.vararg:
            args.add(func.args.vararg.arg)
        if func.args.kwarg:
            args.add(func.args.kwarg.arg)

    pairs = {}
    used = set()
    for func in funcs:
        if func.name == "__init__":
            continue
        newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        while newname in used:
            newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        used.add(newname)
        pairs[func.name] = newname

    for _class in classes:
        newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        while newname in used:
            newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        used.add(newname)
        pairs[_class.name] = newname

    for arg in args:
        newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        while newname in used:
            newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        used.add(newname)
        pairs[arg] = newname

    for attr in attrs:
        newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        while newname in used:
            newname = "".join(random.choice(["I", "l"]) for i in range(random.randint(8, 20)))
        used.add(newname)
        pairs[attr] = newname

    string_regex = r"('|\")[\x1f-\x7e]{1,}?('|\")"

    original_strings = re.finditer(string_regex, code, re.MULTILINE)
    originals = []

    for matchNum, match in enumerate(original_strings, start=1):
        originals.append(match.group().replace("\\", "\\\\"))

    placeholder = os.urandom(16).hex()
    code = re.sub(string_regex, f"'{placeholder}'", code, 0, re.MULTILINE)

    for i in range(len(originals)):
        for key in pairs:
            originals[i] = re.sub(r"({.*)(" + key + r")(.*})", "\\1" + pairs[key] + "\\3", originals[i], re.MULTILINE)

    while True:
        found = False
        code = do_rename(pairs, code)
        for key in pairs:
            if re.findall(fr"\b({key})\b", code):
                found = True
        if found == False:
            break


    replace_placeholder = r"('|\")" + placeholder + r"('|\")"
    for original in originals:
        code = re.sub(replace_placeholder, original, code, 1, re.MULTILINE)

    return code

def w(filename: str, content):
    with open(filename, "w") as f:
        f.write(content)

def rename(src: str, dest: str):
    w(dest, _rename2(src))
    w(dest, _rename(dest))

if __name__ == "__main__":
    code = rename("test/3420.py", "test/3420-obf.py")