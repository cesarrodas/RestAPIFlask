from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\rodas\\Documents\\Projects\\Python\\FlaskAPI\\database.db'
#sqlite:////C:\Users\Student\path\to\foo.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False