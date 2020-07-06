import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data(session):
    print("Привет! Я запишу твои данные!")
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = gender_input()
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    birthdate = input("А также мне понядобится дата твоего рождения в формате ГГГГ-ММ-ЧЧ: ")
    height = int(input("Еще, пожалуйста, укажи свой рост в сантиметрах: ")) / 100 # переводим сантиметры в метры
    # чтобы user_id получился уникальным, 
    # просто будем прибавлять единицу к максимальному user_id,который уже есть в таблице user
    query = session.query(User)
    user_ids = [user.id for user in query.all()]
    user_id = len(user_ids) + 1
    
    user = User(
        id=user_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )

    return user

def gender_input():
    # этот метод нужен, чтобы пользователь точно ввел корректный пол
    gender_input = input("Выбери свой пол:\n1 - Мужской\n2 - Женский\n")
    while gender_input not in ["1", "2"]:
        print("Некорректное значение пола\nВыбери, пожалуйста, 1 или 2")
        gender_input = input("Выбери свой пол:\n1 - Мужской\n2 - Женский\n")
    if gender_input == "1":
        gender = "Male"
    else:
        gender = "Female"
    return gender

def main():
    session = connect_db()
    user = request_data(session)
    session.add(user)
    session.commit()
    print("Спасибо, данные сохранены!")

if __name__ == "__main__":
    main()