import xml.etree.ElementTree as ET
import re

def title_case(text):
    words = text.split()
    # Capitalize the first word and any subsequent words that should generally always be capitalized
    title_words = [words[0].capitalize()] + [word.lower() if word.lower() in ('of', 'the', 'and', 'for', 'in', 'on', 'at', 'by', 'with', 'or', 'to') else word.capitalize() for word in words[1:]]
    text_title =  ' '.join(title_words)
    return text_title

def convert_titles_in_xml(file_path, output_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Iterate over all elements and convert title attributes
    for element in root.iter():
        if 'title' in element.attrib:
            initial_title = element.attrib['title']
            element.attrib['title'] = title_case(initial_title)

    # Write the modified XML tree to the output file
    tree.write(output_path, encoding='utf-8', xml_declaration=True)

# Define input and output file paths
input_file = 'files/src/dawson_rules.xml'
output_file = 'files/src/dawson_rules-title-case.xml'

# Run the conversion
convert_titles_in_xml(input_file, output_file)

print(f"Converted titles and saved the output to {output_file}")
