class User():
    def __init__(self, username, info, error):
        self.username = username
        self.info = info
        self.error = error

    def getusername(self):
        return self.username
    def get_info_number(self):
        return self.info
    def get_error_number(self):
        return self.error

    def addInfoCount(self):
        self.info += 1

    def addErrorCount(self):
        self.error += 1

    def __eq__(self, other):
        return self.username == other
    def __str__(self):
        return "User " + self.username + " Info count " + str(self.info) + " Error Count " + str(self.error)

