#!/usr/bin/python
from datetime import datetime
import logging
import time
import traceback
from transformations import on_raspi


# import the static image class
from displays import ConnectionsFrame
from backend.connections_query import ConnectionsQueryEngine

def connections_formatting(connections):
    conn_formatted = []
    for conn in connections:
        try:
            # Handle cases where fractional seconds are missing
            departure_time = conn['DepartureTime']
            if '.' not in departure_time:
                departure_time = departure_time.replace('Z', '.000000Z')
            
            # Calculate the time difference in minutes
            time_diff = datetime.strptime(departure_time, '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.utcnow()
            # Convert to minutes
            time_diff_minutes = int(time_diff.total_seconds() / 60)
            # Format the connection element
            conn_element = (conn['ServiceName'], conn['Destination'], str(time_diff_minutes))
            conn_formatted.append(conn_element)
        except ValueError as e:
            logging.error("Error parsing time for connection: %s", conn)
            logging.error(e)

    return conn_formatted


def main():

    # Create an instance of the StaticImage class
    frame = ConnectionsFrame()
    # Create an instance of the ConnectionsQuery class
    connections_query = ConnectionsQueryEngine()

    # Get the content
    stop_point_ref = '8573984'  # Example stop point reference
    current_location = 'Mosnang, Dorf'
    departure_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    number_of_results = 4  # Example number of results

    connections = connections_query.get_connections(stop_point_ref, departure_time, number_of_results)

    connections_formatted = connections_formatting(connections)

    # Get the image
    image = frame.get(current_location, connections_formatted)


    # Check if the current device is Raspberry Pi
    raspberry_pi = on_raspi()

    if raspberry_pi:
        try:
            # import waveshare_epd library for Raspberry Pi
            from waveshare_epd import epd2in7_V2

            # Initialize the display
            epd = epd2in7_V2.EPD()
            epd.init()
            epd.Clear()

            # Display the image
            
            for i in range(3):
                # Rotate image by 90 degrees
                image = frame.get(current_location, connections_formatted)
                epd.display(epd.getbuffer(image))
                time.sleep(5)

            # Clear the display
            # epd.Clear()

            # Sleep to save power
            epd.sleep()
        except IOError as e:
            logging.info(e)
        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd2in7_V2.epdconfig.module_exit(cleanup=True)
            exit()
        except Exception as e:
            logging.error("An error occurred: %s", e)
            traceback.print_exc()
        finally:
            # Cleanup the display instance
            if 'epd' in locals():
                epd2in7_V2.epdconfig.module_exit(cleanup=True)
    else:
        try:
            # Dispay the image on screen

            # Rotate image by 90 degrees
            # image = image.rotate(90, expand=True)
            image.show()
            image.save("connections_frame.png")
            time.sleep(5)
            # Close the image window
            image.close()
        except Exception as e:
            logging.error("An error occurred: %s", e)
            traceback.print_exc()
        finally:
            # Cleanup the image instance
            if 'image' in locals():
                image.close()

if __name__ == '__main__':
    main()
