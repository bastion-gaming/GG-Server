from gems import *
import gems
from DB import SQLite as sql
from languages import lang as lang_P


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
            if c["name_pl"] != "Admin":
                ID = sql.get_SuperID(c["name_p"], c["name_pl"])
            else:
                ID = sql.get_SuperID(c["name_p"], "discord")
            if ID != "Error 404":
                c["param_c"]["lang"] = sql.valueAtNumber(ID, "LANG", "IDs")
                c["param_c"]["PlayerID"] = sql.get_PlayerID(ID, "gems")
            else:
                c["param_c"]["lang"] = "EN"
            commande_forgee = commande_forgee + '(' + str(c["param_c"]) + ')'
        except KeyError:
            pass
        # Appelle la fonction

        print(commande_forgee)
        if ID != "Error 404" or commande == "connect" or commande == "begin":
            # try:
                ret = eval(commande_forgee)
                res["reponse"] = ret
            # except:
            #     res["reponse"] = ["WarningMsg", c["param_c"]["lang"], lang_P.forge_msg(c["param_c"]["lang"], "WarningMsg", None, False, 1)]
        else:
            res["reponse"] = ["WarningMsg", c["param_c"]["lang"], lang_P.forge_msg(c["param_c"]["lang"], "WarningMsg", None, False, 0)]

        res["name_c"] = commande
        res["name_p"] = c["name_p"]
        res["name_pl"] = c["name_pl"]
    else:
        res = None

    print(res)
    return res
