import json

with open("keywords.json", "r") as file:
    priority_keywords = json.load(file)

class Ticket:
    def __init__(self, ticket_id, title, description, status="Open", priority=None, created_by=None, assigned_to=None, dependencies=None):
        self.ticket_id = ticket_id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority or self.assign_priority()
        self.created_by = created_by
        self.assigned_to = assigned_to
        self.dependencies = dependencies if dependencies else []
        self.history = []
    
    def assign_priority(self):
        text = (self.title + " " + self.description).lower()
        for priority, keywords in priority_keywords.items():
            for word in keywords:
                if word in text:
                    return priority 
        return "Medium"