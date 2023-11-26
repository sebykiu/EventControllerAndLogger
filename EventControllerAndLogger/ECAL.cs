using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using System.Text;
using EventControllerAndLogger.Json;
using Newtonsoft.Json;

namespace EventControllerAndLogger;

public class Ecal
{
    private readonly IPAddress _ipAddress = IPAddress.Any;
    private readonly Socket _clientSocket;

    private readonly Socket _unityClient;
    private readonly InfluxDb _influxDb;

    private readonly AppConfig _appConfig;


    public Ecal(AppConfig appConfig)
    {
        _appConfig = appConfig;
        if (appConfig.UseCrownet)
        {
            Console.WriteLine("[Notification] Logging to InfluxDB enabled.");

            _influxDb = new(appConfig.InfluxAddr, appConfig.InfluxPort, appConfig.SpecificTag);
        }
        else
        {
            Console.WriteLine("[Notification] Logging to InfluxDB disabled.");
        }
        

        var serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        var endPoint = new IPEndPoint(_ipAddress, _appConfig.OmnetPort);
        serverSocket.Bind(endPoint);

        serverSocket.Listen(1);
        Console.WriteLine("[Notification] Waiting for Omnet++ Simulation to connect on Port: {0}", _appConfig.OmnetPort.ToString());
        _clientSocket = serverSocket.Accept();
        Console.WriteLine("[Notification] Omnet++ connected");


        var messageThread = new Thread(ReceiveData);
        messageThread.Start();
    }


    private void ReceiveData()
    {
        Console.WriteLine("[Notification] Waiting to receive messages from Omnet++");

        int count = 0;

        while (true)
        {
            var lengthBuffer = new byte[4];
            _clientSocket.Receive(lengthBuffer, SocketFlags.None);

            Console.WriteLine("[Notification] Received Message Length");



            if (BitConverter.IsLittleEndian)
            {
                Array.Reverse(lengthBuffer);
            }

            int messageLength = BitConverter.ToInt32(lengthBuffer, 0);

            if (messageLength == 0)
            {
                Console.WriteLine("[Notification] Received empty message. Client is disconnected!");
                break;
            }


            var messageBuffer = new byte[messageLength];
            var received = _clientSocket.Receive(messageBuffer, SocketFlags.None);
            Console.WriteLine("[Notification] Received Message Payload");


            count += 1;
            
            var response = Encoding.UTF8.GetString(messageBuffer, 0, received);

            var message = JsonConvert.DeserializeObject<Message>(response);

            Debug.Assert(message != null, nameof(message) + " != null");
            Console.WriteLine(
                "[Notification] Count: {0} Deserialized: " + "SourceId: {1},TargetID: {2}, ObjectType:{3}, Coordinates: X:{4}, Y:{5}, Z:{6}, SimTime:{7}", count,
                message.SourceId, message.TargetId, message.ObjectType, message.Coordinates.X, message.Coordinates.Y, message.Coordinates.Z,message.SimTime);
            _influxDb.WriteToDatabase(message);
        }

        _clientSocket.Shutdown(SocketShutdown.Both);
    }
}