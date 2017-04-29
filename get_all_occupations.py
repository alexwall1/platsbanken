import requests
import json
import xml.etree.ElementTree as ET

# prepare call
url='http://api.arbetsformedlingen.se/af/v0/Occupation/wsoccupation.asmx'
headers={'Content-Type':'text/xml;charset=utf-8'}

# read body to GetAllOccupationsShort
get_all_occupations_short=open('GetAllOccupationsShort.xml','r').read()
ET.register_namespace('soap','http://schemas.xmlsoap.org/soap/envelope/')
ET.register_namespace('xsi','http://www.w3.org/2001/XMLSchema-instance')
ET.register_namespace('xsd','http://www.w3.org/2001/XMLSchema')
ET.register_namespace('','urn:ams.se:wsoccupation')
get_occupation_by_id=ET.parse('GetOccupationById.xml')

# get list of all occupations
resp=requests.post(url,data=get_all_occupations_short,headers=headers) 
print resp.status_code
dom=ET.fromstring(resp.text.encode('utf-8'))
occupations_short=dom.findall('.//{urn:ams.se:wsoccupation}OccupationShort')

# create results element
results=ET.Element('GetOccupationByIdResponse')
n=len(occupations_short)

# iterate through all occupations to get full details
for el in enumerate(occupations_short):
    occupation_id=el[1].find('.//{urn:ams.se:wsoccupation}Id').text
    occupation_name=el[1].find('.//{urn:ams.se:wsoccupation}Name').text
    get_occupation_by_id.find('.//{urn:ams.se:wsoccupation}occupationId').text=occupation_id
    resp=requests.post(url,data=ET.tostring(get_occupation_by_id.getroot()),headers=headers)
    print '(%s/%s) Getting occupation id: %s (%s). Status: %s' % (el[0] + 1, n, occupation_id, occupation_name, resp.status_code)
    dom=ET.fromstring(resp.text.encode('utf-8'))
    get_occupation_by_id_result=dom.find('.//{urn:ams.se:wsoccupation}GetOccupationByIdResult')
    if get_occupation_by_id_result is not None:
        results.append(get_occupation_by_id_result)

# write to output
ET.ElementTree(results).write('output.xml', encoding='utf-8', xml_declaration=True)
