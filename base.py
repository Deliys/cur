import sqlite3
import datetime

def start():
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()

	# создаем таблицу, если она еще не существует
	cursor.execute('''CREATE TABLE IF NOT EXISTS users
					(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT, password TEXT, email TEXT, role TEXT, signup_date TEXT)''')


	cursor.execute('''CREATE TABLE IF NOT EXISTS basket
			 (id INTEGER PRIMARY KEY AUTOINCREMENT,
			 id_user INTEGER,
			 id_item INTEGER)''')
	cursor.execute('''CREATE TABLE IF NOT EXISTS comment
			 (id INTEGER PRIMARY KEY AUTOINCREMENT,
			 id_user INTEGER,
			 id_orders INTEGER,
			 text_s Text
			 )''')
	cursor.execute('''CREATE TABLE IF NOT EXISTS orders
			 (id INTEGER PRIMARY KEY AUTOINCREMENT,
			 id_user INTEGER,
			 id_master INTEGER,
			 id_sample INTEGER,
			 status Text
			 )''')
	cursor.execute('''CREATE TABLE IF NOT EXISTS sample
			 (id INTEGER PRIMARY KEY AUTOINCREMENT,
			 Name Text,
			 about Text,
			 include Text,
			 photo Text
			 )''')
	conn.commit()
	conn.close()
def get_sample():
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	cursor.execute('SELECT Name, about, include, photo ,cena ,id FROM sample ')
	result = cursor.fetchall()
	conn.close()
	return result

	
def register(username, password, email):
	# сохраняем пользователя в базу данных
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()

	# устанавливаем роль по умолчанию - "user" и текущую дату как дату регистрации
	role = "user"
	signup_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	cursor.execute('''INSERT INTO users (username, password, email, role, signup_date) 
				  VALUES (?, ?, ?, ?, ?)''', 
				  (username, password, email, role, signup_date))
	conn.commit()
def login(username,password):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()

	# выполняем запрос SELECT для поиска пользователя с заданным именем и паролем
	cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
	user = cursor.fetchone()

	# закрываем соединение
	conn.close()

	# если пользователь существует, вернуть True, иначе False
	if user:
		return True
	
	return False

def get_role(username):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()

	# выполняем запрос SELECT для поиска пользователя с заданным именем и паролем
	cursor.execute('SELECT role FROM users WHERE username = ? ', (username,))
	user = cursor.fetchone()

	# закрываем соединение
	conn.close()

	# если пользователь существует, вернуть True, иначе False
	if user:
		return user[0]


def get_users():
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()

	# выполняем запрос SELECT для поиска пользователя с заданным именем и паролем
	cursor.execute('SELECT username ,signup_date,role,id  FROM users ')
	users = cursor.fetchall()

	# закрываем соединение
	conn.close()	
	return users


def create_sample(name ,cena, about,include,photo):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()

	# устанавливаем роль по умолчанию - "user" и текущую дату как дату регистрации
	
	photo = str(photo).replace("b'",'').replace("'",'')

	cursor.execute('''INSERT INTO sample (Name, about, include, photo,cena) 
				  VALUES (?, ?, ?, ?,?)''', 
				  (name, about, include, photo,cena))

	conn.commit()


def delete_sample(idd):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	cursor.execute("DELETE FROM sample WHERE id = ?", (idd,))	
	conn.commit()
def add_basket(idd ,username):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	user_idd = cursor.execute('SELECT id FROM users WHERE username=?' ,(username,)).fetchone()[0]
	# устанавливаем роль по умолчанию - "user" и текущую дату как дату регистрации

	print(type(user_idd))
	print(type(idd))

	cursor.execute('''INSERT INTO basket (id_user, id_item) 
				  VALUES (?, ?)''', 
				  (user_idd, idd ))

	conn.commit()


def get_basket(username):

	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	user_idd = cursor.execute('SELECT id FROM users WHERE username=?' ,(username,)).fetchone()[0]
	# устанавливаем роль по умолчанию - "user" и текущую дату как дату регистрации

	item_b =cursor.execute('SELECT id_item,id FROM basket WHERE id_user=?' ,(user_idd,)).fetchall()
	rec = []
	for i in item_b:
		
		rec.append([cursor.execute('SELECT Name, about, include, photo ,cena ,id FROM sample WHERE id=?' ,(i[0],)).fetchone(),i[1]])

	# cursor.execute('''INSERT INTO basket (id_user, id_item) 
	# 			  VALUES (?, ?)''', 
	# 			  (user_idd, idd ))


	return rec

def basket_delete_item(idd):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	cursor.execute("DELETE FROM basket WHERE id = ?", (idd,))	
	conn.commit()

def gen_order(username):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	user_idd = cursor.execute('SELECT id FROM users WHERE username=?' ,(username,)).fetchone()[0]

	list_item = cursor.execute('SELECT id_item ,id FROM basket WHERE id_user=?' ,(user_idd,)).fetchall()

	for i in list_item:
		cursor.execute('''INSERT INTO orders (id_user, id_sample, status) VALUES (?, ?, ?)''', 
				  (user_idd, i[0], "active"))
		cursor.execute("DELETE FROM basket WHERE id = ?", (i[1],))	

	conn.commit()
def get_active_order_user(username):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	user_idd = cursor.execute('SELECT id FROM users WHERE username=?' ,(username,)).fetchone()[0]

	list_item = cursor.execute('SELECT id,id_sample FROM orders WHERE id_user=? and status=?' ,(user_idd,'active',)).fetchall()

	res = []
	for i in list_item:
		print(1)
		a = cursor.execute('SELECT Name FROM sample WHERE id=?' ,(i[1],)).fetchone()[0]
		res.append([i[0] , a])

	return res
def get_archive_order_user(username):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	user_idd = cursor.execute('SELECT id FROM users WHERE username=?' ,(username,)).fetchone()[0]

	list_item = cursor.execute('SELECT id,id_sample FROM orders WHERE id_user=? and status=?' ,(user_idd,'archive',)).fetchall()

	res = []
	for i in list_item:
		print(1)
		a = cursor.execute('SELECT Name FROM sample WHERE id=?' ,(i[1],)).fetchone()[0]
		res.append([i[0] , a])

	return res


def looking_order(idd):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	sample = cursor.execute('SELECT id_sample,id_master,id ,status FROM orders WHERE id=?' ,(idd,)).fetchone()

	t = cursor.execute('SELECT * FROM sample WHERE id=?' ,(sample[0],)).fetchone()

	name = t[1]

	conn = cursor.execute('SELECT id_user,text_s FROM comment WHERE id_orders=?' ,(idd,)).fetchall()
	

	return [name,sample[1],t[2],t[5],sample[2],sample[3] ,conn]

def add_comment(username,text,idd):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	user_idd = cursor.execute('SELECT id FROM users WHERE username=?' ,(username,)).fetchone()[0]

	cursor.execute('''INSERT INTO comment (id_user, id_orders ,text_s) VALUES (?, ?,?)''', 
				  (user_idd, idd,text))
	conn.commit()
def set_manadjer(idd):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	cursor.execute("UPDATE users SET role = ? WHERE id = ?", ('manager', idd,))	
	conn.commit()

def set_jevi(idd):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	cursor.execute("UPDATE users SET role = ? WHERE id = ?", ('jeweler', idd,))
	conn.commit()
def delete_user(idd):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	cursor.execute("DELETE FROM users WHERE id = ?", (idd,))
	conn.commit()		



def get_active_order_user_jew(username):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	user_idd = cursor.execute('SELECT id FROM users WHERE username=?' ,(username,)).fetchone()[0]

	list_item = cursor.execute('SELECT id,id_sample FROM orders WHERE id_master=? and status=?' ,(user_idd,'active',)).fetchall()

	res = []
	for i in list_item:
		print(1)
		a = cursor.execute('SELECT Name FROM sample WHERE id=?' ,(i[1],)).fetchone()[0]
		res.append([i[0] , a])

	return res
def get_archive_order_user_jew(username):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	user_idd = cursor.execute('SELECT id FROM users WHERE username=?' ,(username,)).fetchone()[0]

	list_item = cursor.execute('SELECT id,id_sample FROM orders WHERE id_master=? and status=?' ,(user_idd,'archive',)).fetchall()

	res = []
	for i in list_item:
		print(1)
		a = cursor.execute('SELECT Name FROM sample WHERE id=?' ,(i[1],)).fetchone()[0]
		res.append([i[0] , a])

	return res
def task_new():
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	

	list_item = cursor.execute('SELECT id,id_sample FROM orders WHERE id_master=? OR id_master IS NULL AND status = ?' ,(None,'active',)).fetchall()

	res = []
	for i in list_item:
		print(1)
		a = cursor.execute('SELECT Name FROM sample WHERE id=?' ,(i[1],)).fetchone()[0]
		res.append([i[0] , a])

	return res

def choise(idd ,username):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	uu = cursor.execute('SELECT id FROM users WHERE username=?' ,(username,)).fetchone()[0]

	cursor.execute("UPDATE orders SET id_master = ? WHERE id = ?", (uu, idd,))	
	conn.commit()	
def end(idd):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	

	cursor.execute("UPDATE orders SET status = ? WHERE id = ?", ("archive", idd,))	
	conn.commit()	

def task_man_all():
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	

	list_item = cursor.execute('SELECT id,id_sample ,status FROM orders').fetchall()

	res = []
	for i in list_item:
		print(1)
		a = cursor.execute('SELECT Name FROM sample WHERE id=?' ,(i[1],)).fetchone()[0]
		res.append([i[0] , a ,i[2]])

	return res

def ch_pass(username,password):
	conn = sqlite3.connect('data.db')
	cursor = conn.cursor()
	
	idd = cursor.execute('SELECT id FROM users WHERE username=?' ,(username,)).fetchone()[0]
	cursor.execute("UPDATE users SET password = ? WHERE id = ?", (password, idd,))	
	conn.commit()		