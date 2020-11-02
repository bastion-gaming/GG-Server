from os import listdir

list_GG_module = list()
for file in listdir("gems"):
    if "gems" in file and ".py" in file:
        name_file = file.replace(".py", "")
        list_GG_module.append(name_file)

__all__ = list_GG_module
