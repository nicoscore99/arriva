import requests

# Your XML data
xml_data = '''<?xml version="1.0" encoding="UTF-8"?>
<Trias version="1.1" xmlns="http://www.vdv.de/trias" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <ServiceRequest>
        <siri:RequestTimestamp>2024-02-19T21:45:55.102Z</siri:RequestTimestamp>
        <siri:RequestorRef>API-Explorer</siri:RequestorRef>
        <RequestPayload>
            <StopEventRequest>
                <Location>
                    <LocationRef>
                        <StopPointRef>8507000</StopPointRef>
                    </LocationRef>
                    <DepArrTime>2024-03-19T22:45:55</DepArrTime>
                </Location>
                <Params>
                    <NumberOfResults>1</NumberOfResults>
                    <StopEventType>departure</StopEventType>
                    <IncludePreviousCalls>true</IncludePreviousCalls>
                    <IncludeOnwardCalls>true</IncludeOnwardCalls>
                    <IncludeRealtimeData>true</IncludeRealtimeData>
                </Params>
            </StopEventRequest>
        </RequestPayload>
    </ServiceRequest>
</Trias>'''

# The endpoint you're sending the request to
url = 'https://api.opentransportdata.swiss/trias2020'

# Assuming you have your API key
api_key = 'eyJvcmciOiI2NDA2NTFhNTIyZmEwNTAwMDEyOWJiZTEiLCJpZCI6ImIwODQ1ZGI2MTdjMDRmNzhhMDAwMWMwZjMwOTllYTZhIiwiaCI6Im11cm11cjEyOCJ9'

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
