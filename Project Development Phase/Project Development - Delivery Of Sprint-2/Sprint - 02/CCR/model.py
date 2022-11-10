from flask_login import UserMixin

class Customer(UserMixin):
    def set(self, uuid, first_name, last_name, email, password, date):
        '''
            Method to initialise the Customer
        '''
        self.uuid = uuid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.date = date

    def get_id(self):
        '''
            Method to return the uuid of the Customer
        '''
        return (self.uuid)
  
class Agent(UserMixin):
    def set(self, uuid, first_name, last_name, email, password, date, confirm):
        '''
            Method to initialise the Agent
        '''
        self.uuid = uuid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.date = date
        self.confirm = confirm

    def get_id(self):
        '''
            Method to return the uuid of the Agent
        '''
        return (self.uuid)

class Admin(UserMixin):
    def set(self, email, password):
        self.email = email
        self.password = password

    def get_id(self):
        '''
            Method to return the email of the Admin
        '''
        return (self.email)
    
