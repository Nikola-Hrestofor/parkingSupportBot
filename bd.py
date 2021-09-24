import psycopg2

try:
	conn = psycopg2.connect(dbname='deecesr6evbgfm', user='srweumdkbseimw', host='ec2-54-73-147-133.eu-west-1.compute.amazonaws.com', password='bb399eb735c392e4432932a922f9293b95764e6355ff192d204b90c54d980050')
	conn.autocommit = True
except:
	print ("Cannot connect to db")

cur = conn.cursor()


def getIdBuNumber(carNumber):

	global cur

	cur.execute("select telegramId, phone from parkingList where carNumber =  %(carNumber)s;" , {"carNumber":carNumber})
	recordsAD = cur.fetchall()   
	print(recordsAD)

	return recordsAD

def reg(userName, userId, phone, name, carNumber, model):

	global cur

	cur.execute("insert into parkingList (telegramId, telegramName, phone, carNumber, name, auto) "
				"values (%(userId)s, %(userName)s, %(phone)s, %(carNumber)s, %(name)s, %(model)s);", 
				{"userId":userId,"userName":userName, "phone":phone, "carNumber":carNumber, "name":name, "model":model})

def searchPhone(carNumber):

	global cur
	cur.execute("select telegramName, phone, auto from parkingList where carNumber =  %(carNumber)s;" , {"carNumber":carNumber})
	recordsAD = cur.fetchall()   

	return recordsAD

def searchPhoneById(telegramId):

	global cur
	cur.execute("select phone from parkingList where telegramId =  %(telegramId)s;" , {"telegramId":telegramId})
	recordsAD = cur.fetchall()   
	print(recordsAD)

	return recordsAD

def isExistsById(id):

	global cur

	cur.execute("select 1 from parkingList where telegramId =  %(id)s;" , {"id":id})
	recordsAD = cur.fetchone()  
 
	return recordsAD



