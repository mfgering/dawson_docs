import dotenv
import re
import os
import sys
import json
import shutil
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from lxml import etree

def get_docs_dir():
    # return path to docs dir
    relative_path = '../docs'

    # Get the absolute path
    absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))
    return absolute_path

def copy_file(source, target):
    with open(source, 'rb') as src_file:
        with open(target, 'wb') as tgt_file:
            tgt_file.write(src_file.read())

def get_element_text(element):
    # etree.tostring can be used to get raw XML content
    # text extraction by decoding and then manipulation
    text = etree.tostring(element, method='text', encoding='unicode')
    return ' '.join(text.split())

def split_stuff(file_path, chunk_paths):
    tree = etree.parse(file_path)
    split = []
    mdata = []
    for chunk in chunk_paths:
        elems = []
        ids = []
        txt_arr = []
        for xpth in chunk:
            id = (None, None)
            search_elems = tree.xpath(xpth)
            assert search_elems is not None
            for elem in search_elems:
                if elem.tag == 'section':
                    section_id = elem.get('id')
                    parent = elem.getparent()
                    article_id = parent.get('id')
                    id = (article_id, section_id)
                    prefix = f"Section {section_id}: " if len(search_elems) > 1 else ''
                elif elem.tag == 'article':
                    id = (elem.get('id'), None)
                    prefix = ''
                ids.append(id)
                txt_str = f"{prefix}{elem.text.strip()}".replace('\n', ' ')
                txt_arr.append(txt_str)
        txt = "\n".join(txt_arr)
        m = {}
        articles = {x[0] for x in ids if x[0]}
        sections = (x[1] for x in ids if x[1])
        m['articles'] = ", ".join(articles) if articles else ''
        m['sections'] = ", ".join(sections) if sections else ''

        mdata.append(m)
        split.append(txt)

    return split, mdata
def cpy_xml_txt_declarations():
    copy_file(f := f'{get_docs_dir()}/dawson_declarations-2018.xml', f'{f}.txt')

def split_declarations():
    chunk_paths = [ 
    ["./article[@id='I']/section"],
    ["./article[@id='II']/section", "./article[@id='III']/section", 
     "./article[@id='IV']/section[@id='4.1' or @id='4.2']"],
    ["./article[@id='IV']/section[@id='4.3']"],
    ["./article[@id='V']/section[@id='5.1']"],
    ["./article[@id='V']/section[@id='5.2']"],
    ["./article[@id='V']/section[@id='5.3']"],
    ["./article[@id='V']/section[@id='5.4']"],
    ["./article[@id='V']/section[@id='5.5']"],
    ["./article[@id='VI']/section", "./article[@id='VII']/section"],
    ["./article[@id='VIII']/section[@id='8.1']"],
    ["./article[@id='VIII']/section[@id='8.2']"],
    ["./article[@id='VIII']/section[@id='8.3']"],
    ["./article[@id='VIII']/section[@id='8.4']"],
    ["./article[@id='VIII']/section[@id='8.5']"],
    ["./article[@id='VIII']/section[@id='8.6']"],
    ["./article[@id='VIII']/section[@id='8.7']"],
    ["./article[@id='VIII']/section[@id='8.8']"],
    ["./article[@id='VIII']/section[@id='8.9']"],
    ["./article[@id='VIII']/section[@id='8.10']"],
    ["./article[@id='VIII']/section[@id='8.11']"],
    ["./article[@id='VIII']/section[@id='8.12']"],
    ["./article[@id='VIII']/section[@id='8.13']"],
    ["./article[@id='VIII']/section[@id='8.14']"],
    ["./article[@id='VIII']/section[@id='8.15']"],
    ["./article[@id='VIII']/section[@id='8.16']"],
    ["./article[@id='VIII']/section[@id='8.17']"],
    ["./article[@id='IX']/section"],
    ["./article[@id='X']/section[@id='10.1']"],
    ["./article[@id='X']/section[@id='10.2']"],
    ["./article[@id='X']/section[@id='10.3']"],
    ["./article[@id='X']/section[@id='10.4']"],
    ["./article[@id='X']/section[@id='10.5']"],
    ["./article[@id='X']/section[@id='10.6']"],
    ["./article[@id='X']/section[@id='10.7']"],
    ["./article[@id='XI']/section","./article[@id='XII']/section",
        "./article[@id='XIII']/section","./article[@id='XIV']/section",
        "./article[@id='XV']/section","./article[@id='XVI']/section",
        "./article[@id='XVII']/section","./article[@id='XVIII']/section",
        "./article[@id='XIX']/section",
        "./article[@id='XX']","./article[@id='XXI']","./article[@id='XVIII']","./article[@id='XIX']",
        "./article[@id='XX']","./article[@id='XXI']"]
    ]
    split, mdata = split_stuff(f := f'{get_docs_dir()}/dawson_declarations-2018.xml', chunk_paths)
    return split, mdata, "declarations"

def cpy_xml_txt_bylaws():
    copy_file(f := f'{get_docs_dir()}/dawson_bylaws.xml', f'{f}.txt')

def split_bylaws():    
    chunk_paths = [ 
    ["./article[@id='I']", "./article[@id='II']/section", "./article[@id='III']/section"],
    ["./article[@id='IV']/section[@id='4.1']"],
    ["./article[@id='IV']/section[@id='4.2']"],
    ["./article[@id='IV']/section[@id='4.3']"],
    ["./article[@id='IV']/section[@id='4.4']"],
    ["./article[@id='IV']/section[@id='4.5']"],
    ["./article[@id='IV']/section[@id='4.6']"],
    ["./article[@id='IV']/section[@id='4.7']"],
    ["./article[@id='IV']/section[@id='4.8']"],
    ["./article[@id='IV']/section[@id='4.9']"],
    ["./article[@id='IV']/section[@id='4.10']"],
    ["./article[@id='IV']/section[@id='4.11']"],
    ["./article[@id='V']/section[@id='5.1']"],
    ["./article[@id='V']/section[@id='5.2']"],
    ["./article[@id='V']/section[@id='5.3']"],
    ["./article[@id='V']/section[@id='5.4']"],
    ["./article[@id='V']/section[@id='5.5']"],
    ["./article[@id='V']/section[@id='5.6']"],
    ["./article[@id='V']/section[@id='5.7']"],
    ["./article[@id='V']/section[@id='5.8']"],
    ["./article[@id='V']/section[@id='5.9']"],
    ["./article[@id='V']/section[@id='5.10']"],
    ["./article[@id='V']/section[@id='5.11']"],
    ["./article[@id='V']/section[@id='5.12']"],
    ["./article[@id='V']/section[@id='5.13']"],
    ["./article[@id='V']/section[@id='5.14']"],
    ["./article[@id='VI']/section[@id='6.1']",
     "./article[@id='VI']/section[@id='6.2']",
     "./article[@id='VI']/section[@id='6.3']",
     "./article[@id='VI']/section[@id='6.4']",
     "./article[@id='VI']/section[@id='6.5']"],
    ["./article[@id='VII']/section[@id='7.1']"],
    ["./article[@id='VII']/section[@id='7.2']"],
    ["./article[@id='VII']/section[@id='7.3']"],
    ["./article[@id='VII']/section[@id='7.4']"],
    ["./article[@id='VII']/section[@id='7.5']"],
    ["./article[@id='VII']/section[@id='7.6']"],
    ["./article[@id='VII']/section[@id='7.7']"],
    ["./article[@id='VII']/section[@id='7.8']"],
    ["./article[@id='VII']/section[@id='7.9']"],
    ["./article[@id='VII']/section[@id='7.10']"],
    ["./article[@id='VII']/section[@id='7.11']"],
    ["./article[@id='VII']/section[@id='7.12']"],
    ["./article[@id='VII']/section[@id='7.13']"],
    ["./article[@id='VIII']/section[@id='8.1']"],
    ["./article[@id='VIII']/section[@id='8.2']"],
    ["./article[@id='VIII']/section[@id='8.3']"],
    ["./article[@id='VIII']/section[@id='8.4']"],
    ["./article[@id='VIII']/section[@id='8.5']"],
    ["./article[@id='VIII']/section[@id='8.6']"],
    ["./article[@id='VIII']/section[@id='8.7']"],
    ["./article[@id='VIII']/section[@id='8.8']"],
    ["./article[@id='VIII']/section[@id='8.9']"],
    ["./article[@id='VIII']/section[@id='8.10']"],
    ["./article[@id='VIII']/section[@id='8.11']"],
    ["./article[@id='VIII']/section[@id='8.12']"],
    ["./article[@id='VIII']/section[@id='8.13']"],
    ["./article[@id='VIII']/section[@id='8.14']"],
    ["./article[@id='IX']","./article[@id='X']/section"]
    ]
    split, mdata = split_stuff(f := f'{get_docs_dir()}/dawson_bylaws.xml', chunk_paths)
    return split, mdata, "bylaws"

def cpy_xml_txt_faqs():
    copy_file(f := f'{get_docs_dir()}/dawson_faqs.xml', f'{f}.txt')

def split_faqs():    
    tree = ET.parse(f := f'{get_docs_dir()}/dawson_faqs.xml')
    split = [ET.tostring(tree.getroot(), encoding="unicode")]
    mdata = [[]]
    return split, mdata, "faqs"

def cpy_xml_txt_rules():
    copy_file(f := f'{get_docs_dir()}/dawson_rules.xml', f'{f}.txt')

def split_rules():    
    split = []
    mdata = []
    tree = ET.parse(f'{get_docs_dir()}/dawson_rules.xml')
    for elem in tree.getroot().findall('./rule'):
        elem_string = ET.tostring(elem, encoding="unicode").replace('\n', ' ')
        split.append(elem_string)
        mdata.append([])
    return split, mdata, "rule"

def cpy_xml_txt_maintenance():
    pass

def split_maintenance():    
    split = []
    mdata = []
    p1 = r"\|(.*?)\|(.*?)\|(.*?)\|"
    with open(f := f'{get_docs_dir()}/dawson_maintenance.txt', 'r') as f:
        #curr_mdata = None
        #curr_content = None
        is_header = True
        for line in f:
            if is_header:
                if '------' in line:
                    is_header = False
                continue
            m = re.match(p1, line)
            if m:
                split.append(m.group(3))
                mdata.append({'item': m.group(1), 'responsibility': m.group(2)})
                pass
    return split, mdata, "maint"

def clean_dir(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):  # checks if it's a file or symlink
                os.unlink(file_path)  # removes file or symlink
                #print(f'Removed file: {file_path}')
            elif os.path.isdir(file_path):  # if it's a directory, you can decide to skip or delete
                shutil.rmtree(file_path)  # removes an entire directory tree
                #print(f'Removed directory: {file_path}')
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def cpy_xml_txt_test():
    pass

def split_test():
    chunk_paths =[    
        ["./article[@id='VIII']/section[@id='8.14']"],        
    ]
    split, mdata = split_stuff(f := f'{get_docs_dir()}/dawson_declarations-2018.xml', chunk_paths)

    return [], [], "test"

if __name__ == "__main__":
    is_split = True if len(sys.argv) > 1 and sys.argv[1].strip().lower() == 'split' else False
    for d in ['test', 'declarations', 'faqs', 'rules', 'maintenance', 'bylaws']:
        f = globals().get(f"cpy_xml_txt_{d}")
        f()
        if is_split:
            build_dir = f"build/rag/{d}"
            if os.path.exists(build_dir):
                clean_dir(build_dir)
            else:
                os.makedirs(build_dir)
            f = globals().get(f"split_{d}")
            split, mdata, fn_template = f()
            assert len(split) == len(mdata), "Length mismatch"
            # Create directory if it doesn't exist
            
            # Process each item in split and mdata
            for i, (text, data) in enumerate(zip(split, mdata)):
                with open(f"{build_dir}/{fn_template}-{i}.txt", 'w') as txt_file:
                    txt_file.write(text)
                if len(data) > 0:
                    with open(f"{build_dir}/{fn_template}-{i}.json", 'w') as json_file:
                        json.dump(data, json_file)

        
    print("Done")