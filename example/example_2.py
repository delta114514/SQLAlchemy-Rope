import responder

from sqlalchemy import Integer, Column
from sqlalchemy.orm.session import sessionmaker
import sqlalchemy.ext.declarative

from sqlalchemy_rope import SessionJenny

api = responder.API()
Base = sqlalchemy.ext.declarative.declarative_base()

url = "sqlite:///data.db"


class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True)
    count = Column(Integer, default=0)


engine = sqlalchemy.create_engine(url, echo=False)
Base.metadata.create_all(engine)
SessionMaker = sessionmaker(bind=engine)

jenny = SessionJenny(SessionMaker)

if not jenny.session.query(Data).all():
    data = Data()
    jenny.session.add(data)
    jenny.session.commit()


@api.route("/")
def index(req, resp):
    data = jenny.session.query(Data).first()
    data.count += 1
    jenny.session.commit()
    resp.content = str(data.count)


def session_id():
    return id(jenny.session)


if __name__ == "__main__":
    api.run()
