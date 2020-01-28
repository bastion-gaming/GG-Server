import random as r
import datetime as dt
from DB import SQLite as sql
from gems import gemsFonctions as GF
import json

lvlmax = 19

class XP:

	def __init__(self,level,somMsg):
		self.level = level
		self.somMsg = somMsg

objetXP = [XP(0,100)
,XP(1,256)
,XP(2,625)
,XP(3,1210)
,XP(4,2401)
,XP(5,4096)
,XP(6,6561)
,XP(7,10930)
,XP(8,16342)
,XP(9,20000)
,XP(10,27473)
,XP(11,34965)
,XP(12,42042)
,XP(13,55739)
,XP(14,66778)
,XP(15,78912)
,XP(16,86493)
,XP(17,95105)
,XP(18,10187)
,XP(19,111111)]


def addxp(ID, nb, nameDB):
	balXP = sql.valueAtNumber(ID, "xp", nameDB)
	try:
		ns = balXP + int(nb)
	except TypeError:
		ns = int(nb)

	if ns <= 0:
		ns = 0
	sql.updateField(ID, "xp", ns, nameDB)


# async def checklevel(message, nameDB):
# 	ID = message.author.id
# 	Nom = message.author.name
# 	member = message.guild.get_member(ID)
# 	objet = objetXP
# 	try:
# 		lvl = sql.valueAtNumber(ID, "lvl", nameDB)
# 		xp = sql.valueAtNumber(ID, "xp", nameDB)
# 		check = True
# 		for x in objet:
# 			if lvl == x.level and check:
# 				if xp >= x.somMsg:
# 					sql.updateField(ID, "lvl", lvl+1, nameDB)
# 					desc = ":tada: {1} a atteint le niveau **{0}**".format(lvl+1, Nom)
# 					title = "Level UP"
# 					if nameDB == "gems":
# 						lvl3 = sql.valueAtNumber(ID, "lvl", nameDB)
# 						title += " | Get Gems"
# 						nbS = lvl3 // 5
# 						nbG = lvl3 % 5
# 						if nbS != 0:
# 							sql.addSpinelles(ID, nbS)
# 							desc += "\nTu gagne {} <:spinelle:{}>`spinelles`".format(nbS, GF.get_idmoji("spinelle"))
# 						if nbG != 0:
# 							nbG = nbG * 50000
# 							sql.addGems(ID, nbG)
# 							desc += "\nTu gagne {} :gem:`gems`".format(nbG)
# 					msg = discord.Embed(title = title,color= 6466585, description = desc)
# 					msg.set_thumbnail(url=message.author.avatar_url)
# 					await message.channel.send(embed = msg)
# 					check = False
# 	except:
# 		return print("Le joueur n'existe pas.")
