import socket
import time
import json
import influxdb_client
from json_object import Message, Coordinates
import datetime


# Custom encoder to support datetime and Message object
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Message):
            return obj.__dict__
        elif isinstance(obj, Coordinates):
            return obj.__dict__
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

def retrieve_messages_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    messages = []
    for record in data:
        sourceId = record.get('SourceId', None)
        targetId = record.get("TargetId")
        objectType = record.get('ObjectType', None)
        coordinates = record.get('Coordinates', None)
        timestamp = record.get('Timestamp', None)

        if sourceId is not None and objectType is not None and coordinates is not None and timestamp is not None:
            x = coordinates.get('X', None)
            y = coordinates.get('Y', None)
            z = coordinates.get('Z', None)
            coordinates = Coordinates(x, y, z)

            # Convert the timestamp from string to datetime
            timestamp = datetime.datetime.fromtimestamp(float(timestamp))
            message = Message(sourceId,targetId, objectType, coordinates, timestamp)
            messages.append(message)

    return messages



def retrieve_messages_from_influx(scenario, org, bucket):
    # Create an InfluxDB client
    client = influxdb_client.InfluxDBClient(url='http://localhost:8086', token='secret-token', org=org)
    query_api = client.query_api()

    # InfluxDB query to load values for specific scenario and pivot them together for them to be returned in one column
    query = f'from(bucket: "{bucket}") \
        |> range(start: 0) \
        |> filter(fn: (r) => r._measurement == "omnet++" and r.scenario == "{scenario}") \
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value") \
        |> sort(columns: ["_time"])'

    # Execute the query
    tables = query_api.query(org=org, query=query)
    
    # Print number of tables returned
    print(f"Number of tables: {len(tables)}")

    # Parse the query result and convert it to a list of messages
    messages = []
    for table in tables:
        print(f"Number of records in this table: {len(table.records)}")
        for record in table.records:
            sourceId = record.values.get('SourceId', None)
            targetId = record.values.get('TargetId', None)
            objectType = record.values.get('ObjectType', None)
            x = record.values.get('X', None)
            y = record.values.get('Y', None)
            z = record.values.get('Z', None)
            timestamp = record.values.get('_time', None)

            # If all necessary fields are present, create a message
            if sourceId is not None and objectType is not None and x is not None and y is not None and z is not None:
                coordinates = Coordinates(x, y, z)
                message = Message(sourceId,targetId, objectType, coordinates, scenario, timestamp)
                messages.append(message)

    return messages






def send_message(ip, port, scenario, org, bucket, use_json = False, json_file=None):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((ip, port))
    print("Connected to the server.")

    # Retrieve messages from InfluxDB for the specified scenario or from a JSON file
    if use_json:
        if json_file is None:
            print("No JSON file specified.")
            return
        messages = retrieve_messages_from_json(json_file)
    else:
        messages = retrieve_messages_from_influx(scenario, org, bucket)

    print(len(messages))

    # If there are no messages, close the socket and return
    if not messages:
        client_socket.close()
        return

    # Get the time of the first message
    first_message_time = messages[0].Timestamp  # Use the Timestamp attribute

    # Calculates the time difference between the current and previous message and let's the execution sleep accordingly
    for i, message in enumerate(messages):
        # First message doesn't have previous message
        if i == 0:  
            time_diff = 0
        else:
            time_diff = (message.Timestamp - messages[i-1].Timestamp).total_seconds()  

        # Convert the message to JSON using the custom encoder
        message_json = json.dumps(message, cls=CustomEncoder)
        encoded_message = message_json.encode()

        # Calculate the length of the encoded message and convert it to bytes
        message_length = len(encoded_message).to_bytes(4, byteorder='big')

        # Send the length of the message to the server
        client_socket.sendall(message_length)
        # Send the JSON message to the server
        print('Sending message to Unity')
        client_socket.sendall(encoded_message)
        print('Going to wait' , time_diff, " seconds")
        # Wait for the calculated time difference before sending the next message
        time.sleep(time_diff)

    # Close the socket
    client_socket.close()



# Set the IP address, port, scenario name, org, and bucket
ip_address = "192.168.178.63"  
port = 54321  
scenario_name = "Scenario1"  
org = 'rovernet'
bucket = 'crownet'
use_json = True
json_path = 'Scenarios/Scenario1.json'

# Call the send_message function with the specified parameters
send_message(ip_address, port, scenario_name, org, bucket,use_json, json_path)
