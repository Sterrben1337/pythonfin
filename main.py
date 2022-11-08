from flask import Flask, render_template, request
import requests
import psycopg2


hostname = 'localhost'
database = 'oaoao'
username = 'postgres'
pwd = '1337'
port_id = 5432

conn = psycopg2.connect(
    host=hostname,
    dbname=database,
    user=username,
    password=pwd,
    port=port_id
)
cur = conn.cursor()

create_script = ''' CREATE TABLE IF NOT EXISTS register (
Name varchar(40)  NOT NULL,
Surname varchar(50),
Email varchar(50),
Password varchar(50)
) '''

cur.execute(create_script)
conn.commit()

create_script1 = ''' SELECT Name, Surname, Email FROM register;'''
cur.execute(create_script1)
conn.commit()
people = cur.fetchall()
conn.commit()




def weather1(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()
print(weather1('95129', 'c83120d4614a77ca16f268781f559467'))



app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route('/main', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        Name = request.form["Name"]
        Surname = request.form["Surname"]
        Email = request.form["Email"]
        Password = request.form["Password"]
        insert_into = 'INSERT INTO register VALUES (%s, %s, %s, %s)'
        insert_values = (Name, Surname, Email, Password)
        cur.execute(insert_into, insert_values)
        conn.commit()
        return render_template("index3.html")
@app.route('/join', methods = ["GET", "POST"])
def join():
    if request.method == "POST":
        Email = request.form['Email']
        Password = request.form['Password']
        word = 'Вы ввели логин или пароль не правильно, повторите вход!!!'
        select_from = 'SELECT Email, Password, Name, Surname FROM register'
        cur.execute(select_from)
        select_all = cur.fetchall()
        print(select_all)
        for i in select_all:
            check_one = False
            if Email == i[0]:
                Name = i[2]
                Surname = i[3]
                check_one = True
                break
        for i in select_all:
            check_two = False
            if Password == i[1]:
                check_two = True
                break
        if check_one == check_two:
            return render_template("index2.html", Name = Name, Surname = Surname)
        else:
            return render_template("index3.html", word = word)

@app.route('/forum', methods = ['GET', 'POST'])
def forum():
    return render_template('index4.html')
@app.route('/forum/state', methods = ['POST', 'GET'])
def forum_weather():
    if request.method == "POST":
        zip = request.form['zipCode']
        api_key = 'c83120d4614a77ca16f268781f559467'
        data = weather1(zip, api_key)
        temp = "{0:.2f}".format(data["main"]["temp"])
        feels_like = "{0:.2f}".format(data["main"]["feels_like"])
        weather = data["weather"][0]['main']
        location = data['name']
        return render_template('result.html', temp=temp, feels_like=feels_like, weather=weather,location=location)
@app.route('/account')
def account():
    return render_template('index5.html', people=people)
if __name__ == '__main__':
    app.run(debug=True)

