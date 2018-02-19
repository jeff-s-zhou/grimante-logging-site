from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logging.db'
db = SQLAlchemy(app)

class ProgressLog(db.Model):
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer)
    user_id = Column(Integer)
    version = Column(Text)
    level_id = Column(Integer)
    seconds = Column(Integer)
    final_turn = Column(Integer)
    outcome = Column(Integer)

class User(db.Model):
    id = Column(Integer, primary_key=True)

class AttemptSession(db.Model):
    id = Column(Integer, primary_key=True)

db.create_all()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/get_new_user')
def get_new_user():
    user = User()
    db.session.add(user)
    db.session.commit()
    return str(user.id)

@app.route('/get_new_attempt_session')
def get_new_attempt_session():
    attempt_session = AttemptSession()
    db.session.add(attempt_session)
    db.session.commit()
    return str(attempt_session.id)


@app.route('/get_steam_key', methods=['POST'])
def get_new_key():
    json = request.get_json()
    passcode = json['passcode']
    if passcode == 'jeff_zhou':
        return get_key_from_file()
    else:
        return 'incorrect passcode'


def get_key_from_file():
    with open('keys.txt', 'r') as f:
        keys_list = f.readlines()
        if len(keys_list) > 0:
            key = keys_list.pop()
        else:
            key = "Sorry, it seems as though Jeff has run out of keys. Please reach out directly to obtain a copy of Grimante."

    with open('keys.txt', 'w') as f:
        f.writelines(keys_list)
    return key


@app.route('/log', methods=['POST'])
def log():
    json = request.get_json()
    l = ProgressLog()
    l.session_id = int(json["attempt_session_id"])
    l.user_id = int(json["user_id"])

    l.version = json["version"]

    l.level_id = int(json["level_id"])
    l.seconds = int(json["seconds"])
    l.final_turn = int(json["final_turn"])
    l.outcome = int(json["outcome"])

    print("printing the session id")
    print(l.session_id)

    db.session.add(l)
    db.session.commit()



app.debug = True

if __name__ == '__main__':
    app.run()