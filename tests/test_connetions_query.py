from backend.connections_query import ConnectionsQueryEngine
import pytest
from datetime import datetime

def test_connections_query():
    """
    Test the ConnectionsQueryEngine class.
    """
    # Create an instance of the ConnectionsQueryEngine
    connections_query = ConnectionsQueryEngine()

    # Define test parameters
    stop_point_ref = '8507000'
    departure_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # Call the get_connections method
    response = connections_query.get_connections(stop_point_ref, departure_time)

    print (response)

    # Check if the response is not None
    assert response is not None, "Response should not be None"