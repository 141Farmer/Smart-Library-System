from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from os import getenv
from dotenv import load_dotenv
from contextlib import contextmanager
from application.database.Base import Base
from typing import Type, Any

class _Session:
    _engine=None
    _session_factory=None
    meta=MetaData()


    def __init__(self):
        load_dotenv()
        database_url=getenv('DATABASE_URL')
        if not database_url:
            raise ValueError("DATABASE_URL is not set in the environment variable")

        self._engine=create_engine(database_url,echo=True)
        self._session_factory=sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
            )
        self.meta.bind=self._engine
        _Session._engine=self._engine
        
    @contextmanager
    def get_session(self):
        session=self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_tables(self):
        Base.metadata.create_all(bind=self._engine)


    def read_all(self, model_cls):
        with self.get_session() as session:
            return session.query(model_cls).all()


    def read_one(self, model_cls, id):
        with self.get_session() as session:
            return session.get(model_cls,id)

    def query_filter(self, model_cls: Type, **filters: Any):
        print("filters",filters)
        with self.get_session() as session:
            query=session.query(model_cls)
            for key, value in filters.items():
                query=query.filter(getattr(model_cls,key)==value)
            return query

    def read_filter_all(self, model_cls: Type, **filters: Any):
        return self.query_filter(model_cls,**filters).all()

    def read_filter_one(self, model_cls: Type, **filters: Any):
        return self.query_filter(model_cls,**filters).first()


    def write(self, tableElement):
        with self.get_session() as session:
            session.add(tableElement)
            session.commit()
            session.refresh(tableElement)
            return tableElement


    def delete(self, model_cls, id):
        with self.get_session() as session:
            instance=session.get(model_cls,id)
            if not instance:
                return False
            session.delete(instance)
            session.commit()
            return True


    def update(self, model_cls, id, updates):
        with self.get_session() as session:
            instance=session.get(model_cls, id)
            if not instance:
                return None

            for key, value in updates.dict(exclude_unset=True).items():
                if key != "id":  
                    setattr(instance, key, value)
            session.commit()
            session.refresh(instance)
            return instance

    def count_all(self, model_cls):
        with self.get_session() as session:
            return session.query(model_cls).count()

    def count_filter(self, model_cls, **filters: any):
        self.query_filter(model_cls,**filters).count()

session_instance=_Session()