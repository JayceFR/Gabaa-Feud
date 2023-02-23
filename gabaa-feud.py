import random
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db = SQLAlchemy(app)


class FeudQuestModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(800))
    answer1 = db.Column(db.String(500))
    answer2 = db.Column(db.String(500))
    answer3 = db.Column(db.String(500))
    answer4 = db.Column(db.String(500))
    answer5 = db.Column(db.String(500))
    answer6 = db.Column(db.String(500))
    answer7 = db.Column(db.String(500))
    answer8 = db.Column(db.String(500))

class RoomModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    quest1 = db.Column(db.Integer)
    quest2 = db.Column(db.Integer)
    quest3 = db.Column(db.Integer)
    quest4 = db.Column(db.Integer)
    quest5 = db.Column(db.Integer)
    quest6 = db.Column(db.Integer)
    quest7 = db.Column(db.Integer)
    quest8 = db.Column(db.Integer)
    

#with app.app_context():
#    db.create_all()

resource_fieds = {
        'id' : fields.Integer,
        'question' : fields.String,
        'answer1' : fields.String,
        'answer2' : fields.String,
        'answer3' : fields.String,
        'answer4' : fields.String,
        'answer5' : fields.String,
        'answer6' : fields.String,
        'answer7' : fields.String,
        'answer8' : fields.String,
        }

room_fields = {
        'id' : fields.Integer,
        'quest1' : fields.Integer,
        'quest2' : fields.Integer,
        'quest3' : fields.Integer,
        'quest4' : fields.Integer,
        'quest5' : fields.Integer,
        'quest6' : fields.Integer,
        'quest7' : fields.Integer,
        'quest8' : fields.Integer,
}

quest_post_args = reqparse.RequestParser()
quest_post_args.add_argument("question", type=str, help="Question not there", required=True)
quest_post_args.add_argument("answer1", type=str, help="Answer1 required", required=True)
quest_post_args.add_argument("answer2", type=str, help="Answer2 required", required=True)
quest_post_args.add_argument("answer3", type=str, help="Answer3 required", required=True)
quest_post_args.add_argument("answer4", type=str, help="Answer4 required", required=True)
quest_post_args.add_argument("answer5", type=str)
quest_post_args.add_argument("answer6", type=str)
quest_post_args.add_argument("answer7", type=str)
quest_post_args.add_argument("answer8", type=str)


task_put_args = reqparse.RequestParser()
task_put_args.add_argument("task", type=str)
task_put_args.add_argument("summary", type=str)


class Room(Resource):

    @marshal_with(room_fields)
    def get(self, room_id):
        room = RoomModel.query.filter_by(id=room_id).first()
        if not room:
            abort(406, message = "No Room With That Room ID...")
        return room
    
    @marshal_with(room_fields)
    def post(self, room_id):
        room = RoomModel.query.filter_by(id = room_id).first()
        if room:
            abort(406, message = "Room id has been already taken ")
        #Generating 8 random unique numbers
        list_of_random_numbers = []
        upper_boundary = 10
        for x in range(8):
            random_num = random.randint(1, upper_boundary)
            while random_num in list_of_random_numbers:
                random_num = random.randint(1, upper_boundary)
            list_of_random_numbers.append(random_num)
        new_room = RoomModel(id = room_id, quest1 = list_of_random_numbers[0], quest2 = list_of_random_numbers[1], quest3 = list_of_random_numbers[2], quest4 = list_of_random_numbers[3], quest5 = list_of_random_numbers[4], quest6 = list_of_random_numbers[5], quest7 = list_of_random_numbers[6], quest8 = list_of_random_numbers[7])
        db.session.add(new_room)
        db.session.commit()
        room_check = RoomModel.query.filter_by(id=room_id).first()
        return room_check
    
    def delete(self, room_id):
        room = RoomModel.query.filter_by(id=room_id).first()
        if not room:
            abort(406, message="No room found with that id ")
        db.session.delete(room)
        db.session.commit()
        room_check = RoomModel.query.filter_by(id=room_id).first()
        if not room_check:
            return {'successful' : 'True'}
        else:
            abort(406, message = "Delete Not Successful...")

class QuestList(Resource):
    def get(self):
        quests = FeudQuestModel.query.all()
        questions = {}
        for quest in quests:
            questions[quest.id] = {"queston" : quest.question, "answer1": quest.answer1, "answer2": quest.answer2, "answer3" : quest.answer3, "answer4" : quest.answer4}
            if quest.answer5:
                questions[quest.id].update({"answer5" : quest.answer5})
            if quest.answer6:
                questions[quest.id].update({"answer6" : quest.answer6})
            if quest.answer7:
                questions[quest.id].update({"answer7" : quest.answer7})
            if quest.answer8:
                questions[quest.id].update({"answer8" : quest.answer8})
        return questions
    
    def delete(self):
        quests = FeudQuestModel.query.all()
        for quest in quests:
            db.session.delete(quest)
        db.session.commit()

class Quest(Resource):
    @marshal_with(resource_fieds)
    def get(self, quest_id):
        task = FeudQuestModel.query.filter_by(id = quest_id).first()
        if not task:
            abort(404, message = "Could not find task with that id...")
        return task
    
    @marshal_with(resource_fieds)
    def put(self, quest_id):
        args = task_put_args.parse_args()
        return args
    
    def delete(self, quest_id):
        quest = FeudQuestModel.query.filter_by(id = quest_id).first()
        if not quest:
            abort(409, message= "No question found with that id...")
        db.session.delete(quest)
        db.session.commit()
        
    
    @marshal_with(resource_fieds)
    def post(self, quest_id):
        args = quest_post_args.parse_args()
        quest = FeudQuestModel.query.filter_by(id = quest_id).first()
        if quest:
            abort(409, message = "task id already tasken")
        new_quest = FeudQuestModel(id = quest_id, question = args['question'], answer1 = args['answer1'] , answer2 = args['answer2'], answer3 = args['answer3'], answer4 = args['answer4'], answer5 = args['answer5'], answer6 = args['answer6'], answer7 = args['answer7'], answer8 = args['answer8'])
        db.session.add(new_quest)
        db.session.commit()
        return new_quest, 200
        #if todo_id in todos:
        #    abort(409, "Task ID already taken")
        #todos[todo_id] = {"task" : args["task"], "summary" : args["summary"]}

api.add_resource(Quest, "/quest/<int:quest_id>")
api.add_resource(QuestList, "/quests")
api.add_resource(Room, "/room/<int:room_id>")
if __name__ == "__main__":
    app.run(debug=True)
