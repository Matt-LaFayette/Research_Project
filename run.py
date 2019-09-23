from app import app, db
from app.models import User
from flask import Flask

app = Flask(__name__)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
#creates the sqllite db 
#engine = create_engine('sqlite:///C:\\sqlitedbs\\research_project.db', echo=True)


if __name__ == "__main__":
    app.run()

#this is required. Similar to a "commit"
#Base.metadata.create_all(engine)


#template for creating a table
# class School(Base):
#     __tablename__ = "woot"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)  


# don't know what this does
#     def __init__(self, name):
#         self.name = name    





