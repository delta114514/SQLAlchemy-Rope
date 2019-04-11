import flask
import threading

from sqlalchemy import Integer, Column
from sqlalchemy.orm.session import sessionmaker
import sqlalchemy.ext.declarative

from sqlalchemy_rope import SessionJenny

app = flask.Flask(__name__)
Base = sqlalchemy.ext.declarative.declarative_base()

url = "sqlite:///data.db"


class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True)
    count = Column(Integer, default=0)


engine = sqlalchemy.create_engine(url, echo=False)
Base.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)

session_not_safe = SessionMaker()
jenny = SessionJenny(SessionMaker)

if not jenny.session.query(Data).all():
    data = Data()
    jenny.session.add(data)
    jenny.session.commit()


@app.route("/")
def index():
    print("-" * 10, "enter", "-" * 10)
    print("thread:", threading.current_thread().ident)
    print("session id:", id(jenny.session))
    print("session id from another scope", session_id())
    data = jenny.session.query(Data).get(1)
    data.count += 1
    jenny.session.commit()
    print(locals())
    print("-" * 10, "exit", "-" * 10)
    return str(data.count)


def session_id():
    return id(jenny.session)


if __name__ == "__main__":
    app.run()
