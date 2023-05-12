from flask import request, jsonify, session, make_response
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_cors import CORS
from models import User, Ticket, TicketComment
from services import app, db, bcrypt

# import openai
import os
from dotenv import load_dotenv
# Load the env file
load_dotenv()
# Use os.environ.get() to get the data

app.config['SQLALCHEMY_DATABASE_URI'] = 'os.environ.get("DATABASE_URI")'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
CORS(app)

app.secret_key = os.environ.get("secretkey")


# ++++ GET&ADD to USERS(all) +++++
class AllUsers(Resource):
    def get(self):
        users = User.query.all()
        users_list = [user.to_dict() for user in users]
        response = make_response(jsonify(users_list), 200)

        return response

    def post(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        is_admin = data.get('is_admin')

        user_exists = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if user_exists:
            return jsonify({"error": "User already exists"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(username=username,
                        email=email,
                        password=hashed_password,
                        first_name=first_name,
                        last_name=last_name,
                        is_admin=is_admin)

        db.session.add(new_user)
        db.session.commit()

        response = make_response(jsonify(new_user.to_dict()), 201)
        return response

api.add_resource(AllUsers, '/api/users')



# ++++ UPDATE SPECIFIC USER ++++ 
class UsersById(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        response = make_response(jsonify(user.to_dict()), 200)

        return response

    def patch(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()

        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)

        db.session.commit()

        response = make_response(jsonify(user.to_dict()), 200)

        return response

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        response = make_response(jsonify({"message": "User deleted successfully"}), 200)

        return response

api.add_resource(UsersById, '/api/users/<int:id>')




# ++++ GET/ADD TICKETSlist(append.all) +++++
class AllTickets(Resource):
    def get(self):
        tickets = Ticket.query.all()
        tickets_list = [ticket.to_dict() for ticket in tickets]
        response = make_response(jsonify(tickets_list), 200)

        return response

    def post(self):
        data = request.get_json()
        print("Received data:", data)
        ticket = Ticket(user_id=data['user_id'], 
                        title=data['title'], 
                        description=data['description'], 
                        status=data['status'], 
                        category=data['category'],
                        priority=data['priority'])

        db.session.add(ticket)
        db.session.commit()

        response = make_response(jsonify(ticket.to_dict()), 201)
        return response

api.add_resource(AllTickets, '/api/tickets')



# ++++ UPDATE SPECIFIC TICKET(id)++++ 

class TicketsById(Resource):
    def get(self, ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)
        ticket_dict = ticket.to_dict()  # ticket_dict is defined here
        
        # Get the associated comments
        comments = TicketComment.query.filter(TicketComment.ticket_id == ticket_id).all()
        comments_list = [comment.to_dict() for comment in comments]

        # Add comments to the ticket dictionary
        ticket_dict['comments'] = comments_list
        
        response = make_response(jsonify(ticket.to_dict()), 200)
        return response

    def patch(self, ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)
        data = request.get_json()

        ticket.title = data.get('title', ticket.title)
        ticket.status = data.get('status', ticket.status)
        ticket.priority = data.get('priority', ticket.priority)
        ticket.category = data.get('category', ticket.category)
        ticket.description = data.get('description', ticket.description)
        ticket.user_id = data.get('user_id', ticket.user_id)

        db.session.commit()

        response = make_response(jsonify(ticket.to_dict()), 200)
        return response

    def delete(self, ticket_id):
        ticket = Ticket.query.get_or_404(ticket_id)
        db.session.delete(ticket)
        db.session.commit()
        response = make_response(jsonify({"message": "Ticket deleted successfully"}), 200)
        return response

api.add_resource(TicketsById, '/api/tickets/<int:ticket_id>')


        # +++++++++ COMMENTS ++++++++

class AllComments(Resource):
    def get (self):
        comments = TicketComment.query.all()
        comments_list = [comment.to_dict() for comment in comments]
        response = make_response(jsonify(comments_list), 200)

        return response

    def post(self):
        data = request.get_json()
        print("Received data:", data)
        comment = TicketComment(user_id=data['user_id'], 
                                ticket_id=data['ticket_id'], 
                                comment=data['comment'])

        db.session.add(comment)
        db.session.commit()

        response = make_response(jsonify(comment.to_dict()), 201)
        return response

api.add_resource(AllComments, '/api/ticket_comments')

class CommentsById(Resource):
    def get(self, id):
        comment = TicketComment.query.get_or_404(id)
        response = make_response(jsonify(comment.to_dict()), 200)
        return response
    
    def patch(self, id):
        comment = TicketComment.query.get_or_404(id)
        data = request.get_json()
        
        comment.comment = data.get('comment', comment.comment)
        
        db.session.commit()
        
        response = make_response(jsonify(comment.to_dict()), 200)
        return response
    
    def delete(self, id):
        comment = TicketComment.query.get_or_404(id)
        db.session.delete(comment)
        db.session.commit()
        response = make_response(jsonify({"message": "Comment deleted successfully"}), 200)
        return response

api.add_resource(CommentsById, '/api/ticket_comments/<int:id>')


        # +++++++++ LOGIN STUFF ++++++++
class Login(Resource):
    def post(self):
        try:
            jsoned_request = request.get_json()
            user = User.query.filter(
                User.username == jsoned_request["username"]).first()
            if user and bcrypt.check_password_hash(user.password, jsoned_request["password"]):
            # if user.authenticate(jsoned_request["password"]):
                session['user_id'] = user.id
                res = make_response(jsonify(user.to_dict()), 200)
                return res
        except Exception as e:
                res = make_response(jsonify({"error": [e.__str__()]}), 500)
                return res


api.add_resource(Login, '/login')

class get_logged_user(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == session["user_id"]).first()
            print(user.is_admin)
            res = make_response(jsonify(user.to_dict()), 200)
            return res


api.add_resource(get_logged_user, '/logged_user')

class check_logged_in(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            if user_id != None:
                return make_response({"logged_in": True}, 200)
        return make_response({"logged_in": False}, 200)


api.add_resource(check_logged_in, '/check')

class logout(Resource):
    def delete(self):
        session['user_id'] = None
        res = make_response(jsonify({ "login" : "Logged out"}),200)
        return res
api.add_resource(logout, '/logout')


if __name__ == '__main__':
    app.run(port=5555)
