#%%
import re
from pathlib import Path
from typing import Generator
import requests
import json
import pandas as pb

from secrect import user_agent, cookies

#%%
headers = {
  'User-Agent': user_agent,
  'sec-ch-ua-platform': '"Linux"',
  'Accept': '*/*',
  'Origin': 'https://eduhive.com.bd',
  'Referer': 'https://eduhive.com.bd/',
  'Accept-Language': 'en-US,en;q=0.9',
}


def read_json(fp):
    with open(fp) as f:
        return json.load(f)

class EduHive:
    url = "https://api.eduhive.com.bd/get-original-course-details"

    def __init__(self, subject_fp) -> None:
        self.subjects = pb.read_json(subject_fp)
        self.root_dir = Path(subject_fp).parent # working directory
        self.dbe = create_engine(f'sqlite:///{self.root_dir.name}.db')

    def get_original_course(self, subject_id, chapter_id, save_to:Path):
        ''' considered save_to as non-existinb. ooened save to with "w" mode '''
        save_to = save_to.joinpath(chapter_id)
        if save_to.is_file():
            return
        
        params={
            'subject':subject_id,
            'chapterId':chapter_id
        }

        r = requests.request("GET", self.url, headers=headers, params=params, cookies=cookies)
        with open(save_to, 'w') as f:
            f.write(r.text)

    def pull_subject_by_name(self, name:str='উচ্চতর গণিত'):
        
        sub = self.subjects.loc[#TODO: pop row
            self.subjects['name']==name
        ]
        self._pull_subject(sub)
    
    def _pull_subject(self, sub:pb.Series):
        subject_id = sub['_id'].values[0]
        chapters = sub['chapters'].values[0]
        sub_dir = self.root_dir.joinpath(
            sub['name'].values[0]
        )

        for cp in chapters:
            chapter_id = cp["_id"]
            paper = str(cp.get('paper'))
            # chapter name subject name is no longer anh need
            name = cp['name']

            file_path = sub_dir
            if paper: 
                file_path = file_path.joinpath(paper)
            file_path.joinpath(name)
            file_path.mkdir(parents=True, exist_ok=True)

            self.get_original_course(subject_id, chapter_id, file_path)

    def pull_all_subject(self):
        for i in self.subjects:
            self._pull_subject(i)


    def save_db(self, s, paper=None):
        '''
        s :json: course content
        '''
        subject_name = s['subject']['name']
        for subcp in s['sections']:
            p = pb.DataFrame.from_dict(subcp['contents'])
            p = p[['title', 'vimeoId']]

            p['section_name']=subcp['name']
            p['chapter_name']=s['name']
            p['chapter_id']=s['chapterId']# optional
            p['subject_name']=subject_name
            p['subject_id']=s['subject']['_id']# optional
            p['paper']=paper

            with self.dbe.connect() as con:
                p.to_sql(subject_name, con, index=False)


    def get_content(self):
        r = requests.request("GET", self.url, headers=headers, cookies=cookies)
        return r.json()

    def loop_hool(self):
        c=0
        while 1:# how do i know where to stop
            c+=1
            print(c, end='\r')

            content = self.get_content()
            chapter_id = content.get('chapterId')
            if not chapter_id:
                continue
            
            sub_name = content['subject']['name']
            cwd = self.root_dir.joinpath(sub_name)
            cwd.mkdir(exist_ok=True)# might raise exception for non existing parent folder
            
            cwd.joinpath(chapter_id)
            if cwd.exists(): continue
            with open(cwd, 'w') as f:
                json.dump(content, f)
            
            print(content['name'])
            # temporarily
            if chapter_id=='62bbe16c7025da7cee5e0f9a':
                break

f='data/eduheive/hsc/subjects.json'
e=EduHive(f)
e.pull_subject_by_name()
# e.pull_all_subject()