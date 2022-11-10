from flask_login import UserMixin

class Customer(UserMixin):
    def set(self, uuid, first_name, last_name, email, password, date):
        self.uuid = uuid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.date = date

    def get_id(self):
        return (self.uuid)
  
