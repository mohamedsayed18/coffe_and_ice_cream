import xml.etree.ElementTree as ET

tree = ET.parse('./period_checker/sample_period.xml')

root = tree.getroot()

for child in root:
    print(type(child))
    print(child.tag, child.attrib)

# print(root)

# TODO I could parse data, create a Period class and then check if data exist in this period object or not