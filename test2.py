import xml.etree.ElementTree as ET

file_path = 'C:/Users/nicol/OneDrive/Projects/tramway_alert/response.xml'


# # Load your XML data into the variable `xml_data`
# xml_data = """
# <?xml version="1.0" encoding="UTF-8"?>
# <trias:Trias xmlns:siri="http://www.siri.org.uk/siri" xmlns:trias="http://www.vdv.de/trias"
#     xmlns:acsb="http://www.ifopt.org.uk/acsb" xmlns:ifopt="http://www.ifopt.org.uk/ifopt"
#     xmlns:datex2="http://datex2.eu/schema/1_0/1_0" version="1.1">
#     <!-- Your XML content here -->
# </trias:Trias>
# """

# # Parse the XML data
# root = ET.fromstring(xml_data)

tree = ET.parse(file_path)
root = tree.getroot()

# Define the namespaces used in the XML document
namespaces = {
    'trias': 'http://www.vdv.de/trias',
    'siri': 'http://www.siri.org.uk/siri'
}

# Initialize lists to hold the times
service_arrival_times = []
service_departure_times = []

# Iterate through the document and extract all ServiceArrival and ServiceDeparture times
for service_arrival in root.findall('.//trias:ServiceArrival/trias:TimetabledTime', namespaces):
    service_arrival_times.append(service_arrival.text)

for service_departure in root.findall('.//trias:ServiceDeparture/trias:TimetabledTime', namespaces):
    service_departure_times.append(service_departure.text)

print("Service Arrival Times:", service_arrival_times)
print("Service Departure Times:", service_departure_times)