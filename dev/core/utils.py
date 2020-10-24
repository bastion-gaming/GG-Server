import random as r


def gen_code(max):
    # Générateur de code aléatoire à x chiffres.
    code = ""
    for i in range(0, max):
        code += "{}".format(r.randint(0, 9))
    return code
