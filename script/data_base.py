#%%
from numpy import ndarray as array
from sqlalchemy import create_engine, select, Table, MetaData
from sqlalchemy import inspect
from sqlalchemy import distinct
from sqlalchemy.orm import sessionmaker
from functools import lru_cache
import pandas as pb


#%%
class DB:
    def __init__(self, db_path) -> None:
        self.engine = create_engine(f'sqlite:///{db_path}')
        session = sessionmaker(bind = self.engine)
        self.session = session()
        self.metadata = MetaData(self.engine)
        
        self.table: Table = None


    def select_subject(self, table_name):
        '''considering name tobe present in table list '''

        self.table = Table(table_name, self.metadata, autoload_with = self.engine)

    @lru_cache
    def list_subject(self):
        insp = inspect(self.engine)
        return insp.get_table_names()

    # @lru_cache()# need tk cache according to the subject
    def list_paper(self):
        # self.session.query(Lecture.chapter_name).distinct().count()
        stmt = select(distinct(self.table.c.paper))
        df = pb.read_sql_query(stmt, self.engine)
        # return df.values[0] and len(df) or 0
        return df
    
    def list_all_chapter(self):
        '''
        chapter -- paper
        '''
        stmt = select(distinct(self.table.c.chapter_name), self.table.c.paper)
        df = pb.read_sql_query(stmt, self.engine)
        df.set_index('chapter_name', inplace=True)
        return df
    
    def list_chapter(self, paper):
        stmt = select(
            distinct(self.table.c.chapter_name), self.table.c.paper
            ).where(
                self.table.c.paper==paper
            )
        df = pb.read_sql_query(stmt, self.engine)
        return df
    
    def list_section(self, chapter_name:str) -> array:
        stmt = select(
            distinct(self.table.c.section_name)
        ).where(
            self.table.c.chapter_name==chapter_name
        )
        df = pb.read_sql_query(stmt, self.engine)
        return df.values

    def list_listion(self, section_name:str):
        '''
        {
            'title' : 'vimeoid'
        }
        '''
        stmt = select(
            self.table.c.vimeoId, self.table.c.title
        ).where(
            self.table.c.section_name==section_name
        )
        df = pb.read_sql_query(stmt, self.engine)
        df.set_index('title', inplace=True)
        return df

#%%
if __name__=='__main__':
    f="data/eduheive/hsc/hsc.db"
    f="/home/kali/Desktop/coding/pyt/eduhive/data/eduheive/hsc/hsc.db"
    d=DB(f)
    d.select_subject('উচ্চতর গণিত')
    p=d.list_listion('অনুশীলনী ১.১ঃ ম্যাট্রিক্স')
    # print(hsc.list_listion("Discussion on Article"))
    print(p)

