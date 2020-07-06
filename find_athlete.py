import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime as DT

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float) 

class Athlete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

def find_athlete(session):
    user_id = input("Введите идентификатор пользователя (целое число): ")
    query = session.query(User)
    all_user_id_list = [user.id for user in query.all()]

    if int(user_id) in all_user_id_list:
        find_athlete_by_birthdate(session, user_id)
        find_athlete_by_height(session, user_id)

    else:
        print("Пользователя с таким иденти не существует")

def find_athlete_by_height(session, user_id):
    query = session.query(User).filter(User.id == user_id).first()
    our_user = query
    our_user_height = our_user.height

    query = session.query(Athlete)
    all_athletes = query.all()

    athletes_list = []        
    for athlete in all_athletes:
        athlete_dict = {"id": "", "difference_height": ""}
        if athlete.height != None:
            athlete_dict["id"] = athlete.id
            athlete_dict["difference_height"] = abs(athlete.height - our_user_height)

        else:
            athlete_dict["id"] = athlete.id
            athlete_dict["difference_height"] = our_user_height

        athletes_list.append(athlete_dict)

    id_athlete = min(athletes_list, key=lambda d: d.get("difference_height", float('inf')))["id"]

    query = session.query(Athlete).filter(Athlete.id == id_athlete).first()
    athlete_by_id = query.name
    print("Ближайший по росту атлет " + athlete_by_id)

def find_athlete_by_birthdate(session, user_id):
    query = session.query(User).filter(User.id == user_id).first()
    our_user = query
    our_user_birthdate = DT.datetime.strptime(our_user.birthdate, '%Y-%m-%d').date()

    query = session.query(Athlete)
    all_athletes = query.all()

    athletes_list = []        
    for athlete in all_athletes:
        athlete_dict = {"id": "", "difference_birthdate": ""}
        if athlete.birthdate != None:
            athlete_dict["id"] = athlete.id
            athlete_dict["difference_birthdate"] = abs(DT.datetime.strptime(athlete.birthdate, '%Y-%m-%d').date() - our_user_birthdate)
                
        else:
            athlete_dict["id"] = athlete.id
            athlete_dict["difference_birthdate"] = abs(DT.datetime.strptime("0001-01-01", '%Y-%m-%d').date() - our_user_birthdate)

        athletes_list.append(athlete_dict)

    id_athlete = min(athletes_list, key=lambda d: d.get("difference_birthdate", float('inf')))["id"]

    query = session.query(Athlete).filter(Athlete.id == id_athlete).first()
    athlete_by_id = query.name
    print("Ближайший по дате рождения атлет " + athlete_by_id)

def main():
    session = connect_db()
    find_athlete(session)

if __name__ == "__main__":
    main()
