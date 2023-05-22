using System.Diagnostics;
using System.Net;
using System.Net.Sockets;
using System.Text;
using EventControllerAndLogger.Json;
using Newtonsoft.Json;

namespace EventControllerAndLogger.Controller;

public class Server
{

    private const int PORT = 12345;
    private  readonly IPAddress _ipAddress = IPAddress.Any;
    private Socket _clientSocket;
    private Thread _messageThread;
    
   // private InfluxDb _influxDb = new InfluxDb();


    public Server()
    {

        var serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        var endPoint = new IPEndPoint(_ipAddress, PORT);
        serverSocket.Bind(endPoint);
        serverSocket.Listen(1);
        Console.WriteLine("Waiting for Omnet++ Simulation to connect on Port:");
        _clientSocket = serverSocket.Accept();
        Console.WriteLine("Simulation Connected!");
        _messageThread = new Thread(ReceiveData);
        _messageThread.Start();
        


    }


    private void ReceiveData()
    {

        while (true)
        {
            
            var lengthBuffer = new byte[4];
            _clientSocket.Receive(lengthBuffer, SocketFlags.None);
            
            if (BitConverter.IsLittleEndian)
            {
                Array.Reverse(lengthBuffer);
            }
            
            int messageLength = BitConverter.ToInt32(lengthBuffer, 0);

            if (messageLength == 0)
            {
                Console.WriteLine("Received empty message. Client is disconnected!");
                break;
            }
            
            var messageBuffer = new byte[messageLength];
            var received = _clientSocket.Receive(messageBuffer, SocketFlags.None);

            var response = Encoding.UTF8.GetString(messageBuffer, 0, received);

            var message = JsonConvert.DeserializeObject<Message>(response);

            Debug.Assert(message != null, nameof(message) + " != null");
            Console.WriteLine("{0},{1},{2},{3},{4}", message.Id, message.Instruction, message.Coordinates.X, message.Coordinates.Y, message.Coordinates.Z);
            //_influxDb.WriteToDatabase(message);
            
        }
        
        _clientSocket.Shutdown(SocketShutdown.Both);

        
    }


}