#%%
from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData
from sqlalchemy import inspect
from sqlalchemy import distinct
from sqlalchemy.orm import sessionmaker, declarative_base
from functools import lru_cache
import pandas as pb

#%%
Base = declarative_base()
class Lecture(Base):
    __tablename__ = "user_account"

    vimeoId = Column(Integer, primary_key=True)
    title = Column(String)
    chapter_name = Column(String)
    paper = Column(Integer)

    def __repr__(self):
        return f"Lecture(id={self.vimeoId!r}, name={self.name!r})"

#%%
class DB:
    def __init__(self, db_path) -> None:
        self.engine = create_engine(f'sqlite:///{db_path}')
        session = sessionmaker(bind = self.engine)
        self.session = session()
        self.metadata = MetaData(self.engine)
        
        self.table: Table = None
        # self._table_subject:str = None
    
        # cache 
        # self.cache_paper = {}

    def select_subject(self, table_name):
        '''considering name tobe present in table list '''
        # self._selected_sub = table_name
        # Lecture.__tablename__ = table_name
        self.table = Table(table_name, self.metadata, autoload_with = self.engine)


    @lru_cache
    def list_subject(self):
        insp = inspect(self.engine)
        return insp.get_table_names()

    # @lru_cache()
    def list_paper(self):
        # self.session.query(Lecture.chapter_name).distinct().count()
        stmt = select(distinct(self.table.c.paper))
        df = pb.read_sql_query(stmt, self.engine)
        # return df.values[0] and len(df) or 0
        return df
    
    def list_chapter(self):
        # return self.session.query(Lecture.chapter_name).distinct()
        # from sqlalchemy import distinct, select
        stmt = select(distinct(self.table.c.chapter_name))
        df = pb.read_sql_query(stmt, self.engine)
        return df
    
    def list_section(self, chapter_name):
        stmt = select(distinct(self.table.c.section_name))
        df = pb.read_sql_query(stmt, self.engine)
        return df

    def list_listion(self, section_name):
        stmt = select(
            self.table.c.vimeoId, self.table.c.title
        ).where(
            self.table.c.section_name==section_name
        )
        df = pb.read_sql_query(stmt, self.engine)
        # df=self.session.execute(stmt)
        return df

#%%
d=DB("data/eduheive/hsc/hsc.db")
d.select_subject('English Grammar')
print(d.list_listion("Discussion on Article"))

# %%
