from pymongo import MongoClient

#connecting to mongodb atlas cluster and returning the database
def get_db():
    client = MongoClient("mongodb+srv://erikas3:Erik%401234@cluster0.zjfo3er.mongodb.net/?retryWrites=true&w=majority")
    return client["TicketSewa"]
