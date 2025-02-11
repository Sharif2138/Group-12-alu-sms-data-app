import xml.etree.ElementTree as ET

xml_file = "modified_sms_V2.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

messages = []
for sms in root.findall('sms'):
    body = sms.find("body").text
    messages.append(body)

print(messages[:5])