#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import xml.etree.ElementTree as ET
import yaml

# Add file to system path
import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class ConnectionsQueryEngine:
    def __init__(self):
        
        credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.yaml')

        # Read the API key from the YAML file
        with open(credentials_path, 'r') as file:
            config = yaml.safe_load(file)
            self.api_key = config['api_key']
            self.url = config['url']

        self.headers = {
            'Content-Type': 'application/xml',
            'Authorization': f'Bearer {self.api_key}'
        }

        ns = {
            'siri': 'http://www.siri.org.uk/siri',
            'ojp': 'http://www.vdv.de/ojp'
        }
        self.ns = ns

    def get_connections(self, stop_point_ref, departure_time, number_of_results=4):
        """
        Get connections from the API based on stop point reference and departure time.
        """
        # Prepare the XML request body
        xml_request = f'''
            <OJP xmlns="http://www.vdv.de/ojp" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xsi:schemaLocation="http://www.vdv.de/ojp" version="2.0">
                <OJPRequest>
                    <siri:ServiceRequest>
                        <siri:ServiceRequestContext>
                            <siri:Language>de</siri:Language>
                        </siri:ServiceRequestContext>
                        <siri:RequestTimestamp>{departure_time}</siri:RequestTimestamp>
                        <siri:RequestorRef>SKIPlus</siri:RequestorRef>
                        <OJPStopEventRequest>
                            <siri:RequestTimestamp>{departure_time}</siri:RequestTimestamp>
                            <siri:MessageIdentifier>SER_1</siri:MessageIdentifier>
                            <Location>
                                <PlaceRef>
                                    <siri:StopPointRef>{stop_point_ref}</siri:StopPointRef>
                                    <Name>
                                        <Text>Bern</Text>
                                    </Name>
                                </PlaceRef>
                                <DepArrTime>{departure_time}</DepArrTime>
                            </Location>
                            <Params>
                                <NumberOfResults>{number_of_results}</NumberOfResults>
                                <StopEventType>departure</StopEventType>
                                <IncludePreviousCalls>false</IncludePreviousCalls>
                                <IncludeOnwardCalls>false</IncludeOnwardCalls>
                                <UseRealtimeData>full</UseRealtimeData>
                            </Params>
                        </OJPStopEventRequest>
                    </siri:ServiceRequest>
                </OJPRequest>
            </OJP>'''
        
        # Send the request to the API
        response = requests.post(self.url, headers=self.headers, data=xml_request)

        if not response.status_code == 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        # Parse the XML response
        root = ET.fromstring(response.content)

        # Extract relevant StopEventResult leave (departure) information
        data = []
        for stop_event_result in root.findall('.//ojp:StopEventResult', self.ns):
            stop_event = stop_event_result.find('ojp:StopEvent', self.ns)
            if stop_event is not None:
                this_call = stop_event.find('ojp:ThisCall/ojp:CallAtStop', self.ns)
                service = stop_event.find('ojp:Service', self.ns)
                if this_call is not None and service is not None:
                    stop_point_ref = this_call.find('siri:StopPointRef', self.ns)
                    stop_point_name = this_call.find('ojp:StopPointName/ojp:Text', self.ns)
                    planned_quay = this_call.find('ojp:PlannedQuay/ojp:Text', self.ns)
                    departure_time = this_call.find('ojp:ServiceDeparture/ojp:TimetabledTime', self.ns)
                    destination = service.find('ojp:DestinationText/ojp:Text', self.ns)
                    train_number = service.find('ojp:TrainNumber', self.ns)
                    service_name = service.find('ojp:PublishedServiceName/ojp:Text', self.ns)

                    data.append({
                        'StopPointRef': stop_point_ref.text if stop_point_ref is not None else None,
                        'StopPointName': stop_point_name.text if stop_point_name is not None else None,
                        'PlannedQuay': planned_quay.text if planned_quay is not None else None,
                        'DepartureTime': departure_time.text if departure_time is not None else None,
                        'TrainNumber': train_number.text if train_number is not None else None,
                        'ServiceName': service_name.text if service_name is not None else None,
                        'Destination': destination.text if destination is not None else None
                    })

        return data
    
def main():
    # Example usage
    engine = ConnectionsQueryEngine()
    stop_point_ref = '8573984'  # Example stop point reference
    departure_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    number_of_results = 4  # Example number of results

    connections = engine.get_connections(stop_point_ref, departure_time, number_of_results)
    
    print(connections)

if __name__ == "__main__":
    main()

