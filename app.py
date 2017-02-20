from flask import  Flask
from peewee import *
from flask import request, redirect, url_for, render_template


app = Flask(__name__)

class ConnectDatabase:
    db = None

    @classmethod
    def get_db(cls):
        if cls.db is None:
            cls.connect_database()
        return cls.db

    @classmethod
    def connect_database(cls):

        cls.db = PostgresqlDatabase('dumbohill', 'dumbohill')

class BaseModel(Model):

    class Meta:
        database = ConnectDatabase.get_db()

class Stories(BaseModel):
    id = PrimaryKeyField(default = None)
    story_title = CharField()
    user_story = CharField()
    acceptance_criteria = CharField()
    business_value = IntegerField()
    estimation = IntegerField()
    status = CharField()


    def __init__(self, story_t, user_s, acceptance_c, business_v, est, stat):
        self.story_title = story_t
        self.user_story = user_s
        self.acceptance_criteria = acceptance_c
        self.business_value = business_v
        self.estimation = est
        self.status = stat



ConnectDatabase.get_db().connect()
ConnectDatabase.get_db().drop_tables([Stories], safe=True, cascade=True)
ConnectDatabase.get_db().create_tables([Stories], safe=True)


@app.route('/')
def index():
    db_select = Stories.select()
    return render_template('list.html', db_select=db_select)

@app.route('/story_page', methods=['POST'])
def story_page():
    return render_template('form.html')

@app.route('/post_story', methods=['POST'])
def post_story():
    stories = Stories(request.form['story_title'], request.form['user_story'], request.form['acceptance_criteria'], request.form['business_value'], request.form['estimation'], request.form['status'])
    ConnectDatabase.db.session.add(stories)
    ConnectDatabase.db.session.commit()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()