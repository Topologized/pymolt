from redbaron import RedBaron, DefNode, NameNode, BinaryOperatorNode, DictNode
from redbaron.base_nodes import CommaProxyList, Node
from typing import Optional, Union
import redbaron
import random

# Function Overloading not supported


def swizzle_comma_str(a, b: list[int]):
    return ", ".join([str(a[i]) for i in b])

def swizzle_function_arguments(defnode: DefNode, module: RedBaron):
    """
    swizzle the positional arguments.
    conditions are:
    1. Function must be "naked": in other words, not a method, and defined in the file.
    2. Function must have no *args / **kwargs
    3. If a call uses a keyword in *any* parameter, apply keyword to all parameters and
    shuffle randomly. Else, shuffle in same order as changed definition.
    """
    fname: str = defnode.name
    only_pos: bool = True
    for args in defnode.arguments:
        match type(args):
            case redbaron.DictArgumentNode:
                only_pos = False
                break
            case redbaron.ListArgumentNode:
                only_pos = False
                break

    if not only_pos:
        return

    n_args: int = len(defnode.arguments)
    if n_args == 0:
        return

    arg_names = [args.target.value for args in defnode.arguments]
    swizzle = list(range(n_args))
    random.shuffle(swizzle)

    defnode.arguments = swizzle_comma_str(defnode.arguments, swizzle)

    possible_call: redbaron.CallNode
    # we want to modify in-place, I want to be safe
    all_calls = [s for s in module.find_all("CallNode")]
    for possible_call in all_calls:
        # NameNode, NameNode, ..., NameNode, CallNode
        # parent name defaults to the first namenode name
        # so this tests if the function is naked also
        if str(possible_call.parent.name) != str(fname):
            continue

        has_keyword = any((arg.target is not None) for arg in possible_call)

        # if no keyword arguments, shuffle in order
        if not has_keyword:
            l = swizzle_comma_str(possible_call.value, swizzle)
            possible_call.value = l
        else:
            # we have keywords, force keyword and give any order
            # Note that pos args can't go after keyword args
            for i, arg in enumerate(possible_call):
                if arg.target is None:
                    arg.target = arg_names[i]
            random.shuffle(possible_call.value)

def swizzle_dict(dictnode: DictNode):
    random.shuffle(dictnode)

# At least ONE is required to be numeric type
# the abelian operators are
# + * & | == !=
# and the logic operators (and, or)
# the convertible operators are
# == != >= <= > <
# but watch out for 1 < 2 < 3
def operator_commute(bnode: BinaryOperatorNode):
    match bnode.value:
        case "+":
            pass
        case "*":
            pass

if __name__ == "__main__":
    with open("test\\3420.py", "r") as f:
        src = f.read()

    module = RedBaron(src)
    def_node = module.find("DefNode")
    swizzle_function_arguments(def_node, module)
    print(module.dumps())