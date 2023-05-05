from faker import Faker
from models import db, User, Ticket
from app import app, db


fake = Faker()

# Change these values according to how many records you want to seed
num_tickets = 15


with app.app_context():
    # ++++ USER FAKER IF WANTED. PASSWORDS MAY HAVE ISSUES WITH HASH BUT FILL "TEST" +++++
    # users = []
    # for i in range(num_users):
        
    #         username=fake.user_name()
    #         email=fake.email()
    #         user = User(username=username, email=email, password="test", first_name=fake.first_name(), last_name=fake.last_name(), role=fake.random_element(["Admin", "User"]))
    #         password="test",
    #         first_name=fake.first_name()
    #         last_name=fake.last_name()
    #         role=fake.random_element(["Admin", "User"])
    #         users.append(user)
            
    # db.session.add_all(users)
    # db.session.commit()

    # users = User.query.all()

    tickets = []
    for i in range(num_tickets):
        
            user_id= "1"
        #     tech_user_id=fake.random_element(users).id
            title=fake.sentence()
            description=fake.paragraph()
            status=fake.random_element(["Open", "In Progress", "Closed"])
            priority=fake.random_element(["Low", "Medium", "High", "Urgent"])
            category=fake.random_element(["Remote", "Onsite"])
            ticket = Ticket(title=title, description=description, status=status, priority=priority, category=category)
        #   user_id=user_id,
        #   tech_user_id=tech_user_id,
            tickets.append(ticket)
            
    for ticket in tickets:
        db.session.add(ticket)
        
    db.session.commit()



    # tickets = Ticket.query.all()
    # users = User.query.all()

    # ticket_comments = []
    # for i in range(num_comments):

    #         ticket_id=fake.random_element(tickets).id
    #         user_id=fake.random_element(users).id
    #         comment=fake.text()
    #         is_ai_generated=fake.boolean(chance_of_getting_true=20)
    #         ticket_comment=TicketComment(ticket_id=ticket_id, user_id=user_id, comment=comment, is_ai_generated=is_ai_generated)
    #         ticket_comments.append(ticket_comment)
        
    # for comment in ticket_comments:
    #     db.session.add(comment)

    db.session.commit()