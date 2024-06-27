import redbaron
import re


def only_two_if(ifnode: redbaron.IfelseblockNode) -> bool:
    if len(ifnode.value) < 2:
        return False
    if (
        (type(ifnode.value[-2]) != redbaron.IfNode
         and type(ifnode.value[-2]) != redbaron.ElifNode)
        or type(ifnode.value[-1]) != redbaron.ElseNode
    ):
        return False

    return True


def not_conditional(cond: str) -> str:
    not_pattern = r"not\s*"
    match = re.match(not_pattern, cond)
    if match is not None:
        return re.subn(not_pattern, "", cond, count=0)[0]
    else:
        if cond[0] == " ":
            return " not" + cond
        else:
            return " not " + cond  # be safe


def swap_if(ifnode: redbaron.IfelseblockNode) -> bool:
    if not only_two_if(ifnode):
        return False

    ifnode.value[-1].value, ifnode.value[-2].value = (
        ifnode.value[-2].value,
        ifnode.value[-1].value,
    )
    ifnode.value[-2].test = not_conditional(str(ifnode.value[0].test))

    return True


if __name__ == "__main__":
    with open("test/iftest.py", "r") as f:
        red = redbaron.RedBaron(f.read())

    n = red.find("IfelseblockNode")
    print(swap_if(n))

    print(red.dumps())
