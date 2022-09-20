#%%
from itertools import chain
import sys
from script.data_base import DB
from script.vimeo import Vimeo
import os
import shutil
from pyperclip import copy


#%%
def get_terminal_size():
    """get terminal window size, return 2-tuple (width, height)"""
    try:
        size = shutil.get_terminal_size()
    except:
        # default fallback values
        size = (100, 20)
    return size

def get_user_response(msg, options):
    """a mimic for a popup window in terminal, to get user response, 
    example: if msg =   "File with the same name already exists\n
                        /home/mahmoud/Downloads/7z1900.exe\n
                        Do you want to overwrite file? "

    and option = ['Overwrite', 'Cancel download']
    the resulting box will looks like:

    *******************************************
    * File with the same name already exists  *
    * /home/mahmoud/Downloads/7z1900.exe      *
    * Do you want to overwrite file?          *
    * --------------------------------------- *
    * Options:                                *
    *   1: Overwrite                          *
    *   2: Cancel download                    *
    *******************************************
    Select Option Number: 

    """
    # map options to numbers starting from 1
    options_map = {i: x for i, x in enumerate(options)}

    # split message to list of lines
    msg_lines = msg.split('\n')

    # format options in lines example: "  1: Overwrite",  and "  2: Cancel download"  
    options_lines = [f'  {k}: {str(v)}' for k, v in options_map.items()]

    # get the width of longest line in msg body or options
    max_line_width = max(max([len(line) for line in msg_lines]), max([len(line) for line in options_lines])) 
    
    # get current terminal window size (width)
    terminal_width = get_terminal_size()[0]

    # the overall width of resulting msg box including border ('*' stars in our case)
    box_width = min(max_line_width + 4, terminal_width)

    # build lines without border
    output_lines = []
    output_lines += msg_lines
    separator = '-' * (box_width - 4)
    output_lines.append(separator)
    output_lines.append("Options:")
    output_lines += options_lines

    # add stars and space padding for each line
    for i, line in enumerate(output_lines):
        allowable_line_width = box_width - 4

        # calculate the required space to fill the line
        delta = allowable_line_width - len(line) if allowable_line_width > len(line) else 0

        # add stars
        line = '* ' + line + ' ' * delta + ' *'

        output_lines[i] = line
    
    # create message string
    msg = '\n'.join(output_lines)
    msg = '\n' + '*' * box_width + '\n' + msg + '\n' + '*' * box_width
    msg += '\n Select Option Number: '

    while True:
        txt = input(msg)
        try:
            # get user selection
            # it will raise exception if user tries to input number not in options_map
            response = options_map[int(txt)]  
            print() # print empty line
            break  # exit while loop if user entered a valid selection
        except:
            print('\n invalid entry, try again.\n')

    return response


#%%
data = 'data/eduheive/hsc.db'
# course_list = filter(lambda x: x.endswith('.db'), os.listdir(data))
d = DB(data)

while 1:
    p = get_user_response('chose a course', chain(d.list_subject(), ['exit']))
    if p=='exit': sys.exit(0)
    d.select_subject(p)
    while 1:
        cp = get_user_response(
            'chose a chapter',
            chain(d.list_all_chapter().index, ['back', 'exit'])
        )
        if cp=='back': break
        elif cp=='exit': sys.exit(0)
        while 1:
            sec = get_user_response(
                'chose a listion',
                chain(d.list_section(cp), ['back', 'exit'])
            )
            if sec=='back': break
            elif sec=='exit': sys.exit(0)
            while 1:
                lec=d.list_listion(sec[0])
                title = get_user_response(
                    'chose a lecture',
                    chain(lec.index, ['back', 'exit'])
                )
                if title=='back': break
                elif title=='exit': sys.exit(0)
                video_id = lec.loc[title][0]
                
                v = Vimeo(video_id)
                try:
                    v.get_quality()
                except ConnectionError:
                    print('[!] internet not avqilable')
                    break
                
                while 1:
                    q = get_user_response(
                        'select a quality',
                        chain(v.content, ['back', 'exit'])
                    )
                    if q=='back': break
                    elif q=='exit': sys.exit(0)

                    link = v.content[q]
                    print('[+]', link, sep='\n')
                    copy(link)
                    print('[+] link copied to the clipboard')

# %%
{
    # subjects
    "math" :{
        # paper
        "1":{
            # chapters
            "অধ্যায় ১: ম্যাট্রিক্স ও নির্ণায়ক":[
                # sections
                "অনুশীলনী ১.১ঃ ম্যাট্রিক্স"
            ]
        }
    }
}