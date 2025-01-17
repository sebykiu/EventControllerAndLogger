import socket
import threading
import time
import json
import influxdb_client
from json_object import Message, Coordinates
import datetime
import argparse
import subprocess
import functools

time_control_constant = 1


# Custom encoder to support datetime and Message object
@functools.singledispatch
def default(obj):
    if isinstance(obj, Message):
        return obj.__dict__
    elif isinstance(obj, Coordinates):
        return obj.__dict__
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return json.JSONEncoder.default(obj)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        return default(obj)


def update_time_control_constant():
    # Allows the waiting time between messages to be manipulated by the user.

    global time_control_constant

    while True:
        updated_constant = input("Enter the new time multiplication factor: ")
        try:
            time_control_constant = float(updated_constant)
        except ValueError:
            print("Please enter a valid number: ")


def retrieve_messages(
        data_source, scenario=None, org=None, bucket=None, json_path=None, start_time=0
):
    if data_source == "influx":
        # Create an InfluxDB client
        client = influxdb_client.InfluxDBClient(
            url="http://localhost:8086", token="secret-token", org=org
        )
        query_api = client.query_api()

        # InfluxDB query to load values for specific scenario and pivot them together for them to be returned in one
        # column
        query = f'from(bucket: "{bucket}") \
            |> range(start: {start_time}) \
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
                source_id = record.values.get("SourceId", None)
                target_id = record.values.get("TargetId", None)
                object_type = record.values.get("ObjectType", None)
                x = record.values.get("X", None)
                y = record.values.get("Y", None)
                z = record.values.get("Z", None)
                sim_time = record.values.get("SimTime", None)

                # If all necessary fields are present, create a message
                if (
                        source_id is not None
                        and object_type is not None
                        and x is not None
                        and y is not None
                        and z is not None

                ):
                    coordinates = Coordinates(x, y, z)
                    sim_time = datetime.datetime.fromtimestamp(float(sim_time))
                    message = Message(
                        source_id,
                        target_id,
                        object_type,
                        coordinates,
                        sim_time,
                        scenario,
                    )
                    messages.append(message)
    elif data_source == "json":
        with open(json_path, "r") as f:
            data = json.load(f)

        messages = []
        for record in data:
            source_id = record.get("SourceId", None)
            target_id = record.get("TargetId")
            object_type = record.get("ObjectType", None)
            coordinates = record.get("Coordinates", None)
            sim_time = record.get("SimTime", None)

            if (
                    source_id is not None
                    and object_type is not None
                    and coordinates is not None
                    and sim_time is not None
            ):
                x = coordinates.get("X", None)
                y = coordinates.get("Y", None)
                z = coordinates.get("Z", None)
                coordinates = Coordinates(x, y, z)
                message = Message(
                    source_id, target_id, object_type, coordinates, sim_time
                )

                messages.append(message)

    return messages


def send_message_length(client_socket, message_length):
    # Send the length of the message to the server
    client_socket.sendall(message_length)


def send_message_json(client_socket, message_json):
    # Send the JSON message to the server
    client_socket.sendall(message_json.encode())


def send_message(
        ip, port, scenario, org, bucket, start_time, json_path=None, debug=False, ignore_file=None
):
    ignore_list = read_ignore_list(ignore_file) if ignore_file else []

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Try to Connect to the server
    try:
        client_socket.connect((ip, port))
    except ConnectionRefusedError:
        print(
            '[Critical Exception] ConnectionRefusedError: Couldn\'t connect to Unity. Is it running? Check the ports '
            'and address!')
        exit(1)

    print("Connected to the server.")
    print("Loading messages.")
    # Retrieve messages from InfluxDB for the specified scenario or from a JSON file
    if json_path:
        messages = retrieve_messages("json", json_path=json_path)
    else:
        messages = retrieve_messages("influx", scenario=scenario, org=org, bucket=bucket, start_time=start_time)

    print("Loaded {}".format(len(messages)))

    # If there are no messages, close the socket and return
    if not messages:
        client_socket.close()
        return

    # Calculates the time difference between the current and previous message and lets the execution sleep accordingly
    for i, message in enumerate(messages):
        # Check if the message source_id is in the ignore list
        if message.SourceId in ignore_list:
            print(f"SourceId {message.SourceId} was found in the ignore list and is therefore skipped!")
            continue

        if i == 0:
            time_diff = 0
        else:
            print(f"{message.SimTime} this is the simTime", message.SimTime)
            time_diff = (
                                message.SimTime - messages[i - 1].SimTime
                        ).total_seconds() * time_control_constant

        # Convert the message to JSON using the custom encoder
        message_json = json.dumps(message, cls=CustomEncoder)

        # Calculate the length of the encoded message and convert it to bytes
        message_length = len(message_json.encode()).to_bytes(4, byteorder="big")

        # Send the length of the message to the server
        send_message_length(client_socket, message_length)

        # Send the JSON message to the server
        send_message_json(client_socket, message_json)

        if debug:
            print("Time difference:", time_diff)

        # Wait for the calculated time difference before sending the next message
        time.sleep(time_diff)

    # Close the socket
    client_socket.close()


def read_ignore_list(file_path):
    ignore_list = []
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('#'):
                ignore_list.append(stripped_line)
    print(ignore_list)
    return ignore_list


if __name__ == "__main__":
    # Check if InfluxDB container is running
    influxdb_check_cmd = 'docker ps --format "{{.Names}}" | grep -q "^influxdb$"'
    if subprocess.call(influxdb_check_cmd, shell=True) == 0:
        print("InfluxDB is reachable and health check succeeded!")
    else:
        print(
            "[Critical Warning] InfluxDB is NOT running. Did you run bash build_and_run.sh? You can ignore this "
            "Warning if you only want to use JSON files.")
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="Load a scenario from InfluxDB or JSON and send the messages to Unity"
    )

    # Define command-line arguments
    parser.add_argument(
        "--ip", type=str, default="localhost", help="Unity Address (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=54321, help="Unity Port (default: 54321)"
    )
    parser.add_argument(
        "--org",
        type=str,
        default="rovernet",
        help="InfluxDB Organisation (default: rovernet)",
    )
    parser.add_argument(
        "--bucket",
        type=str,
        default="crownet",
        help="InfluxDB Bucket (default: crownet)",
    )
    group = parser.add_argument_group("only one of this Arguments must be set:")
    group.add_argument("--scenario", type=str, help="InfluxDB Scenario Name (see SpecificTag in config.yaml)")
    group.add_argument("--json-path", type=str, help="JSON path")
    parser.add_argument(
        "--start",
        type=int,
        default=0,
        help="Start time of the scenario (default: 0)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Log time difference of messages to console (default: False)",
    )
    parser.add_argument(
        "--ignore_file",
        type=str,
        default="",
        help="Path to ignore file listing objects to not be send to Unity."
    )

# Parse the command-line arguments
args = parser.parse_args()

# Check that either scenario or json-path is provided, but not both
if not (args.scenario is None) ^ (args.json_path is None):
    parser.error("Please provide either --scenario or --json-path, but not both.")

# Call the send_message function with the specified arguments
send_message(
    args.ip,
    args.port,
    args.scenario,
    args.org,
    args.bucket,
    args.start,
    args.json_path,
    args.debug,
    args.ignore_file
)

time_control_constant = 1
time_control_constant_thread = threading.Thread(target=update_time_control_constant)
time_control_constant_thread.daemon = True  # Exit when main thread stops
time_control_constant_thread.start()
