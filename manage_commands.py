from gems import *
import gems
from DB import SQLite as sql


def exec_commands(c):
    """
    Va se charger d'exécuter toutes les commandes

    params :
    dict c => message

    return :
    dict => name_c, name_p, name_pl, reponse
    """
    # On récupère tous les modules dans gems
    list_here = gems.list_GG_module

    packets_list = list()
    function_dict = dict()
    res = dict()

    for i in list_here:
        # On exclut les magic func
        if "gems" in i:
            packets_list.append(i)

    for j in packets_list:
        tmp_list = list()
        tmp = dir(eval("gems."+j))

        for k in tmp:
            tmp_list.append(k)
        function_dict[str(j)] = tmp_list

    commande = c["name_c"]
    file_c = ""

    for mod_name in packets_list:
        if commande in function_dict[mod_name]:
            # Où a été trouvé la commande
            file_c = mod_name
            break
        else:
            file_c = None

    # S'il a trouvé une commande
    if file_c is not None:
        commande_forgee = "getattr(eval(file_c), commande)"
        try:
            c["param_c"]["name_pl"] = c["name_pl"]
            ID = sql.get_SuperID(c["name_p"], c["name_pl"])
            if ID != "Error 404":
                c["param_c"]["lang"] = sql.valueAtNumber(ID, "LANG", "IDs")
            else:
                c["param_c"]["lang"] = "EN"
            commande_forgee = commande_forgee + '(' + str(c["param_c"]) + ')'
        except KeyError:
            pass
        # Appelle la fonction

        print(commande_forgee)

        ret = eval(commande_forgee)

        res["name_c"] = commande
        res["name_p"] = c["name_p"]
        res["name_pl"] = c["name_pl"]
        res["reponse"] = ret

    else:
        res = None

    print(res)
    return res
