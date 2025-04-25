import requests

# Your XML data
xml_data = '''<OJP xmlns="http://www.vdv.de/ojp" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xsi:schemaLocation="http://www.vdv.de/ojp" version="2.0">
    <OJPRequest>
        <siri:ServiceRequest>
            <siri:ServiceRequestContext>
                <siri:Language>de</siri:Language>
            </siri:ServiceRequestContext>
            <siri:RequestTimestamp>2025-04-24T14:11:26.795Z</siri:RequestTimestamp>
            <siri:RequestorRef>SKIPlus</siri:RequestorRef>
            <OJPStopEventRequest>
                <siri:RequestTimestamp>2025-04-24T14:11:26.795Z</siri:RequestTimestamp>
                <siri:MessageIdentifier>SER_1</siri:MessageIdentifier>
                <Location>
                    <PlaceRef>
                        <siri:StopPointRef>8507000</siri:StopPointRef>
                        <Name>
                            <Text>Bern</Text>
                        </Name>
                    </PlaceRef>
                    <DepArrTime>2025-04-24T14:11:26.795Z</DepArrTime>
                </Location>
                <Params>
                    <NumberOfResults>2</NumberOfResults>
                    <StopEventType>departure</StopEventType>
                    <IncludePreviousCalls>false</IncludePreviousCalls>
                    <IncludeOnwardCalls>false</IncludeOnwardCalls>
                    <UseRealtimeData>full</UseRealtimeData>
                </Params>
            </OJPStopEventRequest>
        </siri:ServiceRequest>
    </OJPRequest>
</OJP>'''

# The endpoint you're sending the request to
url = 'https://api.opentransportdata.swiss/ojp20'

# Assuming you have your API key
api_key = 'eyJvcmciOiI2NDA2NTFhNTIyZmEwNTAwMDEyOWJiZTEiLCJpZCI6IjQyNjVkM2RjODEyODQ3ZDJhZjg5MTQ1Mzg2MTYyY2IwIiwiaCI6Im11cm11cjEyOCJ9'

# Additional headers with the Authorization header
headers = {
    'Content-Type': 'application/xml',  # This header is important for telling the server the type of the content
    'Authorization': f'Bearer {api_key}'  # API key for authorization
}

# Sending the request
response = requests.post(url, data=xml_data, headers=headers)

# Checking the response
if response.status_code == 200:
    print("Success!")
    print(response.text)  # Or process the response in a way that's appropriate for your application

    # Save the response to a xml file
    with open('response.xml', 'w') as file:
        file.write(response.text)

else:
    print("Error:", response.status_code)
    print(response.text)
