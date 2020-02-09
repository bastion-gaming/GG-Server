import json


def load_dates():
    """
    Charge les dates des saisons et leur nombre total

    Return :
    dict => 5 clefs avec pour les 4 premières les int 1, 2, 3 et 4 qui donnes
        les 4 dates puis une clef string total qui donne le total de saison écoulé.
    """
    path = "core/saisons.json"
    res = dict
    with open(path, encoding='utf-8') as json_file:
        data = json.load(json_file)
        for i in data:
            if i != "total":
                res[int(i)] = data[i]
            else:
                res[i] = data[i]
    return res
