import sqlite3
from flask import Flask, redirect, url_for, render_template, request, session
from PIL import Image
import base
import base64
from io import BytesIO


app = Flask(__name__)
app.secret_key = "r@nd0mSk_1"
base.start()

@app.route("/")
def index():
	

	if ('username' in session) == False:
		ss = """
	  <a href="/login" class="btn-primary">Вход</a>
	  <a href="/register" class="btn-primary">Регистрация</a>"""
	else:
		if session['role'] != 'user':
			ss = """
			<a href="/home" class="btn-primary">Профиль</a>
			<a href="/logout" class="btn-primary">Выход</a>"""
		else:
			ss = """
			<a href="/home" class="btn-primary">Профиль</a>
			<a href="/bascket" class="btn-primary">корзина</a>
			<a href="/logout" class="btn-primary">Выход</a>"""			
	d = ''
	for i in base.get_sample():
		if ('username' in session):
			if session['role'] != 'user':
				if i[3]!=None:

						a = '<img src="data:image/png;base64, {} " />'.format(str(i[3]))
				else:
					a = '<img src="https://via.placeholder.com/250x250.png" alt="Товар 1">'
				d+=""" 
				<div class="card-grid">
					<div class="card">
					{}
					<h3>{}</h3>
					<p>{} руб</p>
					
			  </div>""".format(i[0],a,i[4])
			else :
				if i[3]!=None:

					a = '<img src="data:image/png;base64, {} " />'.format(str(i[3]))
				else:
					a = '<img src="https://via.placeholder.com/250x250.png" alt="Товар 1">'
				d+=""" 
				<div class="card-grid">
					<div class="card">
					{}
					<h3>{}</h3>
					<p>{} руб</p>
					<a href="/add_basket/{}" class="btn-primary">в корзину</a>
			  </div>""".format(i[0],a,i[4],i[5])
		else:
			if i[3]!=None:

				a = '<img src="data:image/png;base64, {} " />'.format(str(i[3]))
			else:
				a = '<img src="https://via.placeholder.com/250x250.png" alt="Товар 1">'
			d+=""" 
			<div class="card-grid">
				<div class="card">
				{}
				<h3>{}</h3>
				<p>{} руб</p>
				<a href="/add_basket/{}" class="btn-primary">в корзину</a>
		  </div>""".format(i[0],a,i[4],i[5])			
	return render_template('main.html' ,card=d,ses=ss)


@app.route('/register', methods=["POST", "GET"])
def register():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		base.register(username, password,email)
		return redirect(url_for('index'))

	else:
		return render_template('register.html')

@app.route('/login', methods=["POST", "GET"])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if base.login(username, password):
			session['username'] = username
			session['role'] = base.get_role(username)

		return redirect(url_for('index'))
	else:
		return render_template('login.html')

@app.route('/home', methods=['POST', "GET"])
def home():
	if request.method == 'POST':
		password = request.form['newPassword']		
		base.ch_pass(session['username'],password)
		return redirect(url_for('login'))



	if 'username' in session:
		gg = ''
		if session['role'] == 'user':
			gg = '<a href="/bascket" class="btn-primary">корзина</a>'
			meny = """
				<li><a href="/archive">история заказов</a></li>
				<li><a href="/active">активные заказы</a></li>
			"""
		if session['role'] == 'jeweler':
			meny = """
				<li><a href="/task_new">Выбрать новый заказ</a></li>
				<li><a href="/archive_jev">история заказов</a></li>
				<li><a href="/active_jev">активные заказы</a></li>
			"""
		if session['role'] == 'manager':
			meny = """
			  <li><a href="/create_sample">добавление позиций на сайт</a></li>
			  <li><a href="/get_users">аккаунты пользователей</a></li>
			  <li><a href="/task_man_all">просмотр всех заказов</a></li>
			"""
		return render_template('home.html', 
			name=session['username'] , 
			role=session['role'],
			meny = meny,
			gg = gg
		 
			)
	else:
		return render_template('login.html')

@app.route('/get_users', methods=['POST', "GET"])
def get_users():
	if 'username' in session:
		if session['role'] == 'manager':
			meny = """
				<li><a href="#">история заказов</a></li>
				<li><a href="#">активные заказы</a></li>
			"""
			temp = ""
			for i in base.get_users():
				if i[2] == 'manager':a = """
				<a href="/set_jevi/{}" class="btn-primary">Назначить ювелиром</a>
				<a href="/delete_user/{}" class="btn-primary">Удалить</a>""".format(i[3],i[3])
				if i[2] == 'user':a = """
				<a href="/set_jevi/{}" class="btn-primary">Назначить ювелиром</a>
				<a href="/set_manadjer/{}" class="btn-primary">Назначить меджером</a>
				<a href="/delete_user/{}" class="btn-primary">Удалить</a>""".format(i[3],i[3],i[3])
				if i[2] == 'jeweler':a = """
				<a href="/set_manadjer/{}" class="btn-primary">Назначить меджером</a>
				<a href="/delete_user/{}" class="btn-primary">Удалить</a>""".format(i[3],i[3])

				temp+="""<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(i[0],i[1],i[2],a)

		  

			return render_template('users.html', users=temp)
		else:
			return render_template('home.html', 
				name=session['username'] , 
				role=session['role'],
				meny = meny
			 
				)
	else:
		return render_template('login.html')


@app.route('/create_sample', methods=['GET', 'POST'])
def create_sample():
	temp = ''
	for i in base.get_sample():
		if i[3]!=None:photo='<img src="data:image/png;base64, {} " />'.format(str(i[3]))
		else:photo=''
		idd = i[5]
		temp+="""<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(i[0],i[1],i[2],photo,i[4] ,'<a href="/delete_sample/{}"><button>удалить</button></a></td>'.format(idd))	
	if request.method == 'POST':
		file = request.files['image']
		name = request.form['name']
		about = request.form['about']
		include = request.form['include']

	
		cena = request.form['cena']

		

		try:
			image = Image.open(file)
			buffer = BytesIO()
			image.save(buffer,format="JPEG")
			myimage = buffer.getvalue()                     
			image =base64.b64encode(myimage)
		except Exception as e:
			print(e)
			image = None
		
		base.create_sample(name , cena,about,include,image)
		return redirect(url_for('create_sample') )


	return render_template('upload.html',item=temp)


@app.route('/bascket', methods=['GET', 'POST'])
def basket():
	if 'username' in session:
		temp = ''
		for i in base.get_basket(session['username']):
			iddd = i[1]
			i =i[0]

			if i[3]!=None:photo='<img src="data:image/png;base64, {} " />'.format(str(i[3]))
			else:photo=''
			idd = i[5]
			temp+="""<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(i[0],i[1],i[2],photo,i[4] ,'<a href="/delete_item_basket/{}"><button>удалить</button></a></td>'.format(iddd))	
		if request.method == 'POST':
			file = request.files['image']
			name = request.form['name']
			about = request.form['about']
			include = request.form['include']

		
			cena = request.form['cena']

			

			try:
				image = Image.open(file)
				buffer = BytesIO()
				image.save(buffer,format="JPEG")
				myimage = buffer.getvalue()                     
				image =base64.b64encode(myimage)
			except Exception as e:
				print(e)
				image = None
			
			base.create_sample(name , cena,about,include,image)
			return redirect(url_for('basket') )


		return render_template('basket.html',item=temp)
	return redirect(url_for('/login'))



@app.route('/delete_item_basket/<idd>')
def delete_item_basket(idd):
	base.basket_delete_item(idd)
	return redirect(url_for('index') )
@app.route('/add_basket/<idd>')
def add_basket(idd):
	if 'username' in session:
		base.add_basket(idd,session['username'])
		return redirect(url_for('index') )
	else:
		return redirect(url_for('login') )



@app.route('/gen_order')
def gen_order():
	base.gen_order(session['username'])
	return redirect(url_for('basket') )

@app.route('/delete_sample/<idd>')
def delete_sample(idd):
	base.delete_sample(idd)
	return redirect(url_for('create_sample') )

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

@app.route('/active', methods=['POST', "GET"])
def get_active_order_user():
	if 'username' in session:
			temp = ""
			for i in base.get_active_order_user(session['username']):
				a = '<a href="/looking_order/{}"><button>обзор заказа</button></a></td>'.format(i[0])
				temp+="""<tr><td>{}</td><td>{}</td><td>{}</td></tr>""".format(i[0],i[1],a)
			return render_template('orders.html', users=temp)
	else:
		return render_template('login.html')

@app.route('/archive', methods=['POST', "GET"])
def get_archive_order_user():
	if 'username' in session:
			temp = ""
			for i in base.get_archive_order_user(session['username']):
				a = '<a href="/looking_order/{}"><button>обзор заказа</button></a></td>'.format(i[0])
				temp+="""<tr><td>{}</td><td>{}</td><td>{}</td></tr>""".format(i[0],i[1],a)
			return render_template('orders.html', users=temp)
	else:
		return render_template('login.html')

@app.route("/looking_order/<idd>", methods=['POST', "GET"])
def looking_order(idd):
	if request.method == 'POST':

			comment = request.form['comment']

			
			base.add_comment(session['username'], comment ,idd)
			# return redirect(url_for('/looking_order/{}'.format(idd)))


	temp = base.looking_order(idd)
	comm = """"""
	for i in temp[6]:
		comm+="""<li>user {} | {}</li>\n""".format(i[0],i[1])
	return render_template('looking_order.html',
		name = temp[0],
		master = temp[1],
		order = temp[4],
		cena = temp[3],
		comm = comm,
		iddd = idd,


		status = temp[5])

@app.route('/set_manadjer/<idd>')
def set_manadjer(idd):
	base.set_manadjer(idd)
	return redirect(url_for('get_users'))
@app.route('/set_jevi/<idd>')
def set_jevi(idd):
	base.set_jevi(idd)
	return redirect(url_for('get_users'))
@app.route('/delete_user/<idd>')
def delete_user(idd):
	base.delete_user(idd)
	return redirect(url_for('get_users'))

@app.route('/active_jev', methods=['POST', "GET"])
def active_jev():
	if 'username' in session:
			temp = ""
			for i in base.get_active_order_user_jew(session['username']):
				a = '<a href="/looking_order/{}"><button>обзор заказа</button></a> <a href="/end/{}"><button>завершить</button></a>'.format(i[0],i[0])
				temp+="""<tr><td>{}</td><td>{}</td><td>{}</td></tr>""".format(i[0],i[1],a)
			return render_template('orders.html', users=temp)
	else:
		return render_template('login.html')

@app.route('/archive_jev', methods=['POST', "GET"])
def archive_jev():
	if 'username' in session:
			temp = ""
			for i in base.get_archive_order_user_jew(session['username']):
				a = '<a href="/looking_order/{}"><button>обзор заказа</button></a></td>'.format(i[0])
				temp+="""<tr><td>{}</td><td>{}</td><td>{}</td></tr>""".format(i[0],i[1],a)
			return render_template('orders.html', users=temp)
	else:
		return render_template('login.html')
@app.route('/task_new', methods=['POST', "GET"])
def task_new():
	if 'username' in session:
			temp = ""
			for i in base.task_new():
				a = '<a href="/choise/{}"><button>принять</button></a> <a href="/looking_order/{}"><button>обзор заказа</button></a></td>'.format(i[0],i[0])
				

				temp+="""<tr><td>{}</td><td>{}</td><td>{}</td></tr>""".format(i[0],i[1],a)
			return render_template('orders.html', users=temp)
	else:
		return render_template('login.html')
@app.route('/task_man_all')
def task_man_all():
	if 'username' in session:
			temp = ""
			for i in base.task_man_all():
				if i[2] == 'archive':
					a = '<a href="/looking_order/{}"><button>обзор заказа</button></a>'.format(i[0],i[0])
				else:
					a = '<a href="/looking_order/{}"><button>обзор заказа</button></a> <a href="/end/{}"><button>завершить</button></a>'.format(i[0],i[0])
				temp+="""<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(i[0],i[1],i[2],a)
			return render_template('orderss.html', users=temp)
	else:
		return render_template('login.html')
def choise(idd):
	base.choise(idd ,session['username'])
	return redirect(url_for('home'))
@app.route('/end/<idd>')
def end(idd):
	base.end(idd )
	return redirect(url_for('home'))
if __name__ == '__main__':
	app.run(debug=True)



