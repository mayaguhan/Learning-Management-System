class User():


    def __init__(self, data):
        user_id = data["user_id"]
        username = data["username"]
        name = data["name"]
        email = data["email"]
        seniority_level = data["seniority_level"]
        contact = data["contact"]


        self.user_id = user_id
        self.username = username
        self.name = name
        self.email = email
        self.seniority_level = seniority_level
        self.contact = contact

    def getUserId(self):
        return self.user_id


class SeniorEngineer(User):

    def __init__(self, userData, salary=1000):
        User.__init__(self, userData)
        self.salary = salary

    
    def getSalary(self):
        return self.salary

    def getName(self):
        return self.name