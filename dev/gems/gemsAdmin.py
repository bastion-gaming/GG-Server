from database import SQLite as sql


def admin(param):
    fct = param["fct"]
    arg2 = param["arg2"]
    arg3 = param["arg3"]
    arg4 = param["arg4"]
    msg = []
    if fct == "playerid":
        if arg2 == "None":
            platform = param["name_pl"]
        else:
            platform = arg2
    else:
        platform = param["name_pl"]
    if param["name_pl"] == "Admin" and fct != "playerid":
        PlayerID = int(param["ID"])
        lang = "EN"
    else:
        ID = sql.get_PlayerID(int(param["ID"]), platform)
        lang = param["lang"]
        if ID['error'] == 404:
            return {'error': 1, 'etat': 'warning', 'lang': lang}
        PlayerID = ID['ID']

    if fct == "init":
        sql.init()
    # elif fct == "update":
    #     # arg2 = nameDB | arg3 = fieldName | arg4 = fieldValue
    #     desc = sql.updateField(PlayerID, arg3, arg4, arg2)
    # elif fct == "add":
    #     # arg2 = nameDB | arg3 = nameElem | arg4 = nbElem
    #     desc = sql.add(PlayerID, arg3, arg4, arg2)
    # elif fct == "value":
    #     # arg2 = nameDB | arg3 = nameElem
    #     desc = sql.valueAt(PlayerID, arg3, arg2)
    elif fct == "addgems":
        # arg2 = nb gems
        desc = sql.addGems(PlayerID, arg2)
    elif fct == "addspinelles":
        # arg2 = nb spinelles
        desc = sql.addSpinelles(PlayerID, arg2)
    elif fct == "balance total" or fct == 'balancetotal':
        desc = "Balance total"
        desc += "\n{}:gem:".format(sql.countTotalGems())
        spinelleidmoji = "{idmoji[spinelle]}"
        desc += "\n{0}<:spinelle:{1}>".format(sql.countTotalSpinelles(), spinelleidmoji)
    elif fct == "playerid":
        desc = "PlayerID: {}".format(PlayerID)
    # elif fct == "inventory":
    #     desc = sql.valueAll(PlayerID, "inventory", ["Item", "Stock"])
    elif fct == "gems":
        desc = sql.value(PlayerID, "gems", "Gems")
    elif fct == "spinelles":
        desc = sql.value(PlayerID, "gems", "Spinelles")
    else:
        desc = ":regional_indicator_s::regional_indicator_q::regional_indicator_l:"

    msg.append("Admin {}".format(fct))
    msg.append(lang)
    msg.append(str(desc))
    return msg
