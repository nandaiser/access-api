from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(80), primary_key=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    services = relationship("Service", backref = "owner", cascade = "all, delete")

    def __repr__(self):
        return f'<User {self.id}>'
    
class Service(db.Model):
    __tablename__ = "service"
    
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    service = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable = False)
    owner_id = db.Column(db.String, db.ForeignKey("user.id"))
    
    def __repr__(self):
        return f"<Service id: {self.id}, service: {self.service}, owner id: {self.owner_id}>"
