import re
import xml.etree.ElementTree as ET

def parse_raleigh_city_code(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    front_matter = []
    have_front = False
    content2 = []
    for line in content.split('\n'):
        if not have_front:
            if line.startswith('PART'):
                have_front = True
                content2.append(line)
            else:
                front_matter.append(line)
        else:
            content2.append(line)
    # Create the root element
    root = ET.Element('raleigh-city-code')

    # Regular expressions to match different levels of the hierarchy
    part_regex = r'^PART (\d+)(.*)'
    chapter_regex = r'^CHAPTER (\d+)\.'
    article_regex = r'^ARTICLE ([A-Z]+)\.'
    division_regex = r'^DIVISION (\d+)\.'
    section_regex = r'^Sec\. (\d+[-]\d+)'

    # Initialize variables to keep track of the current hierarchy
    current_part = None
    current_chapter = None
    current_article = None
    current_division = None

    # Iterate through each line of the content
    for line in content2:
        # Check for matches at each level of the hierarchy
        part_match = re.search(part_regex, line)
        chapter_match = re.search(chapter_regex, line)
        article_match = re.search(article_regex, line)
        division_match = re.search(division_regex, line)
        section_match = re.search(section_regex, line)

        # Create or update elements based on the matches
        if part_match:
            current_part = ET.SubElement(root, 'part', num=part_match.group(1))
            current_part_title= part_match.group(2).strip()
        elif chapter_match and current_part:
            current_chapter = ET.SubElement(current_part, 'chapter', num=chapter_match.group(1))
        elif article_match and current_chapter:
            current_article = ET.SubElement(current_chapter, 'article', label=article_match.group(1))
        elif division_match and current_article:
            current_division = ET.SubElement(current_article, 'division', num=division_match.group(1))
        elif section_match:
            section_num = section_match.group(1)
            if current_division is not None:
                ET.SubElement(current_division, 'section', num=section_num)
            elif current_article is not None:
                ET.SubElement(current_article, 'section', num=section_num)
            else:
                ET.SubElement(current_chapter, 'section', num=section_num)

    return root

# Usage example
#/home/mgering/projects/mfg_django_morgan/morgan_ai/dawson_docs/docs/CODE_OF_THE_CITY_OF_RALEIGH__NORTH_CAROLINA.txt
xml_root = parse_raleigh_city_code('./morgan_ai/dawson_docs/docs/CODE_OF_THE_CITY_OF_RALEIGH__NORTH_CAROLINA.txt')
xml_tree = ET.ElementTree(xml_root)
xml_tree.write('./morgan_ai/dawson_docs/docs/CODE_OF_THE_CITY_OF_RALEIGH__NORTH_CAROLINA.xml', encoding='utf-8', xml_declaration=True)