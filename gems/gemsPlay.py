import random as r
import time as t
import datetime as dt
from DB import TinyDB as DB, SQLite as sql
from gems import gemsFonctions as GF
from core import level as lvl
from operator import itemgetter


def crime(ID):
	"""Commets un crime et gagne des :gem:`gems` Attention au DiscordCop!"""
	if sql.spam(ID,GF.couldown_6s, "crime", "gems"):
		# si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
		if r.randint(0,9) == 0:
			sql.add(ID, "DiscordCop Arrestation", 1, "statgems")
			if int(sql.addGems(ID, -10)) >= 0:
				msg = "Vous avez été attrapés par un DiscordCop vous avez donc payé une amende de 10 :gem:`gems`"
			else:
				msg = "Vous avez été attrapés par un DiscordCop mais vous avez trop peu de :gem:`gems` pour payer une amende"
		else :
			gain = r.randint(2,8)
			jour = dt.date.today()
			if (jour.month == 10 and jour.day >= 23) or (jour.month == 11 and jour.day <= 10): #Special Halloween
				msg = "**Halloween** | Des bonbons ou un sort ?\n"
				msg += GF.message_crime[r.randint(0,3)]+" "+str(gain)
				if r.randint(0,1) == 0:
					msg += " :candy:`candy`"
					sql.add(ID, "candy", gain, "inventory")
				else:
					msg += " :lollipop:`lollipop`"
					sql.add(ID, "lollipop", gain, "inventory")
			else:
				msg = "{1} {0} :gem:`gems`".format(gain, GF.message_crime[r.randint(0,3)])
				sql.addGems(ID, gain)
				sql.addGems(sql.get_PlayerID(GF.idBaBot, "gems", "discord"), -gain)
				if (jour.month == 12 and jour.day >= 22) and (jour.month == 12 and jour.day <= 25):
					if r.randint(0,10) == 0:
						nbgift = r.randint(1,3)
						sql.add(ID, "lootbox_gift", nbgift, "inventory")
						msg += "\n\nTu as trouvé {} :gift:`cadeau de Noël (gift)`".format(nbgift)
				elif (jour.month == 12 and jour.day >= 30) or (jour.month == 1 and jour.day <= 2):
					if r.randint(0,10) == 0:
						nbgift = r.randint(1,3)
						sql.add(ID, "lootbox_gift", nbgift, "inventory")
						msg += "\n\nTu as trouvé {} :gift:`cadeau de la nouvelle année (gift)`:confetti_ball:".format(nbgift)
		sql.updateComTime(ID, "crime", "gems")
		lvl.addxp(ID, 1, "gems")
	else:
		msg = "Il faut attendre "+str(GF.couldown_6s)+" secondes entre chaque commande !"
	return msg
