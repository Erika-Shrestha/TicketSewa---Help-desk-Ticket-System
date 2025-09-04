import json
from connectDb import get_db

with open("keywords.json", "r") as file:
    priority_keywords = json.load(file)

db = get_db()
ticketSewa_collection = db["Tickets"]

class Ticket:
    def __init__(self, title, description, status="Open", priority=None, created_by=None, assigned_to=None, dependencies=None, ticket_id = None, ):
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority or self.assign_priority()
        self.created_by = created_by
        self.assigned_to = assigned_to
        self.dependencies = dependencies or []
        self.history = []
        if ticket_id: 
            self.ticket_id = ticket_id
        else:
            self.ticket_id = None
            self.save_to_db()

    
    def assign_priority(self):
        text = (self.title + " " + self.description).lower()
        for priority, keywords in priority_keywords.items():
            for word in keywords:
                if word.lower() in text:
                    return priority 
        return "Medium"
    
    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_by": self.created_by,
            "assigned_to": self.assigned_to,
            "dependencies": self.dependencies,
            "history": self.history
        }
    
    def save_to_db(self):
        result = ticketSewa_collection.insert_one(self.to_dict())
        self.ticket_id = str(result.inserted_id)
        print(f"Ticket '{self.title}' stored in MongoDB.")