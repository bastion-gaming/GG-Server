from gems import *


def exec_commands(c):
    """
    Va se charger d'exécuter toutes les commandes

    params :
    dict c => message

    return :
    dict => name_c, name_p, name_pl, reponse
    """
    list_here = dir() # On récuppère tous les modules dans gems
    packets_list = list()
    function_dict = dict()
    res = dict()

    for i in list_here:
        if "gems" in i: # On exclut les magic func
            packets_list.append(i)

    for j in packets_list:
        tmp_list = list()
        tmp = dir(eval(j))

        for k in tmp:
            tmp_list.append(k)
        function_dict[str(j)] = tmp_list

    commande = c["name_c"]
    file_c = ""

    for mod_name in packets_list:
        if commande in function_dict[mod_name]:
            file_c = mod_name # Où a été trouvé la commande
            break
        else:
            file_c = None

    if file_c != None: # S'il a trouvé une commande
        commande_forgee = "getattr(eval(file_c), commande)"
        try:
            commande_forgee = commande_forgee + c["param_c"]
        except KeyError:
            pass
        ret = eval(commande_forgee)

        res["name_c"] = commande
        res["name_p"] = c["name_p"]
        res["name_pl"] = c["name_pl"]
        res["reponse"] = ret

        return res
