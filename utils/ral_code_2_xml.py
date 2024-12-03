import re
from lxml import etree
from typing import List

def print_tree(element):
    print(etree.tostring(element, pretty_print=True, encoding='unicode'))

def find_parent_element(subtree_root, child):
    stack = [(None, subtree_root)]   
    while stack:
        parent, element = stack.pop()
        if element == child:
            return parent
        for subelement in element:
            stack.append((element, subelement))
    return None

def get_indices(content, markers)->List[int]:
    result = []
    idx = 0
    for marker in markers:
        idx2 = 0
        for line in content[idx:]:
            if line.startswith(marker):
                idx = idx + idx2
                result.append(idx)
                break
            idx2 += 1
    return result

def parse_front_matter(content, start_idx, end_idx, tag_name):
    elem = etree.Element(tag_name)
    elem.text = "\n".join(content[start_idx:end_idx])
    return elem

def parse_charter(content, start_idx, end_idx, tag_name):
    elem = etree.Element(tag_name)
    article_regex = r'^ARTICLE[ \xA0]+([IVXLC]+)\.[ \xA0]+(.*)'
    division_regex = r'^DIVISION (\d+)\.'
    section_regex = r'^Sec\.[ \xA0]+([\d\.]+)[ \xA0]+(.*)'

    current_article = None
    current_section = None
    prev_elem = None
    text_lines = []
    for line in content[start_idx+1:end_idx]:
        # Check for matches at each level of the hierarchy
        article_match = re.search(article_regex, line)
        section_match = re.search(section_regex, line)
        if article_match:
            current_article = etree.SubElement(elem, 'article', id=article_match.group(1), title=article_match.group(2))
            if len(text_lines) > 0 and prev_elem is not None:
                prev_elem.text = "\n".join(text_lines)
                text_lines = []
            prev_elem = current_article
        elif section_match is not None and current_article is not None:
            current_section = etree.SubElement(current_article, 'section', num=section_match.group(1), title=section_match.group(2))
            if len(text_lines) > 0 and prev_elem is not None:
                prev_elem.text = "\n".join(text_lines)
                text_lines = []
            prev_elem = current_section
        else:
            text_lines.append(line)
    if len(text_lines) > 0 and prev_elem is not None:
        prev_elem.text = "\n".join(text_lines)
        text_lines = []
    
    return elem

def parse_back(content, start_idx, end_idx, tag_name):
    elem = etree.Element(tag_name)
    elem.text = "\n".join(content[start_idx:end_idx])
    return elem

def parse_back(content, start_idx, end_idx, tag_name):
    elem = etree.Element(tag_name)
    elem.text = "\n".join(content[start_idx:end_idx])
    return elem

def parse_code(content, start_idx, end_idx, tag_name):
    root = etree.Element('raleigh-city-code')
    part_regex = r'^PART[ \xA0]+(\d+)[ \xA0]+(.*)'
    chapter_regex = r'^CHAPTER[ \xA0]+(\d+)\.[ \xA0]+(.*)'
    article_regex = r'^ARTICLE[ \xA0]+([A-Z]+)\.[ \xA0]+(.*)'
    division_regex = r'^DIVISION[ \xA0]+(\d+)\.[ \xA0]+(.*)'
    section_regex = r'^Secs?\. ((\d+-\d+)(\s+[—-]\s+(\d+-\d+))?)\.[ \xA0]+(.*)'

    current_part = None
    current_chapter = None
    current_article = None
    current_division = None
    prev_elem = root
    current_parent = root
    text_lines = []
    # Iterate through each line of the content
    for line in content[start_idx:end_idx]:
        # Check for matches at each level of the hierarchy
        part_match = re.search(part_regex, line)
        chapter_match = re.search(chapter_regex, line)
        article_match = re.search(article_regex, line)
        division_match = re.search(division_regex, line)
        section_match = re.search(section_regex, line)

        # Create or update elements based on the matches
        if part_match:
            if len(text_lines) > 0 and prev_elem is not None:
                prev_elem.text = "\n".join(text_lines)
                text_lines = []
            title = part_match.group(2).strip()
            num = part_match.group(1)
            current_part = current_parent = prev_elem = etree.SubElement(root, 'part', num=num, title=title)
        elif chapter_match is not None:
            if len(text_lines) > 0 and prev_elem is not None:
                prev_elem.text = "\n".join(text_lines)
                text_lines = []
            title = chapter_match.group(2).strip()
            num = chapter_match.group(1)
            current_chapter = current_parent = prev_elem = etree.SubElement(current_part, 'chapter', num=num, title=title)
        elif article_match is not None and current_chapter is not None:
            if len(text_lines) > 0 and prev_elem is not None:
                prev_elem.text = "\n".join(text_lines)
                text_lines = []
            title = article_match.group(2).strip()
            num = article_match.group(1)
            current_article = current_parent = prev_elem = etree.SubElement(current_chapter, 'article', label=article_match.group(1))
        elif division_match is not None and current_article is not None:
            if len(text_lines) > 0 and prev_elem is not None:
                prev_elem.text = "\n".join(text_lines)
                text_lines = []
            title = division_match.group(2).strip()
            num = division_match.group(1)
            current_division = prev_elem = etree.SubElement(current_article, 'division', num=division_match.group(1))
        elif section_match is not None:
            if len(text_lines) > 0 and prev_elem is not None:
                prev_elem.text = "\n".join(text_lines)
                text_lines = []
            title = section_match.group(5).strip()
            num = section_match.group(1)
            if prev_elem.tag == "section":
                parent_elem = find_parent_element(root, prev_elem)
            else:
                parent_elem = prev_elem
            current_section = current_parent = prev_elem = etree.SubElement(parent_elem, 'section', num=num, title=title)
        else:
            text_lines.append(line)
    if len(text_lines) > 0 and prev_elem is not None:
        prev_elem.text = "\n".join(text_lines)
        text_lines = []
    return root

def parse_raleigh_city_code(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
    indices = get_indices(content, ['CHARTER', 'PART', 'ORDINANCE DISPOSITION TABLE'])

    front_matter_elem = parse_front_matter(content, 0, indices[0], 'front-matter')
    charter_elem = parse_charter(content, indices[0], indices[1]+1, 'charter')
    code_elem = parse_code(content, indices[1], indices[2], 'code')
    back_matter_elem = parse_back(content, indices[2], len(content), 'back-matter')

    root = etree.Element('root')
    root.append(front_matter_elem)
    root.append(charter_elem)
    root.append(code_elem)
    root.append(back_matter_elem)

    tree = etree.ElementTree(root)
    return tree

xml_tree = parse_raleigh_city_code('./morgan_ai/dawson_docs/docs/CODE_OF_THE_CITY_OF_RALEIGH__NORTH_CAROLINA.txt')
xml_tree.write('./morgan_ai/dawson_docs/docs/CODE_OF_THE_CITY_OF_RALEIGH__NORTH_CAROLINA.xml', encoding='utf-8', xml_declaration=True)