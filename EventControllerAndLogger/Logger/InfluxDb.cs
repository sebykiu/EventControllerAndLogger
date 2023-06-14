using EventControllerAndLogger.Json;
using InfluxDB.Client;
using InfluxDB.Client.Api.Domain;
using InfluxDB.Client.Writes;

namespace EventControllerAndLogger.Logger;



public class InfluxDb
{
    const string Token = "secret-token";
    const string Bucket = "crownet";
    const string Org = "rovernet";

    private string _influxAddr;
    private int _influxPort;
    private InfluxDBClient _client;
    private string _specificTag;

    public InfluxDb(string influxAddr, int influxPort, string specificTag)
    
    
    {
        _client = InfluxDBClientFactory.Create("http://"+influxAddr+":" +influxPort, Token);
        _specificTag = specificTag;
    }

    public void WriteToDatabase(Message message)
    {
        PointData msg = PointData.Measurement("omnet++")
            .Field("Id", message.Id)
            .Field("Path", message.Path)
            .Field("Instruction", message.Instruction)
            .Field("X", message.Coordinates.X)
            .Field("Y", message.Coordinates.Y)
            .Field("Z", message.Coordinates.Z)
            .Timestamp(DateTime.UtcNow, WritePrecision.Ns);

        if (_specificTag != "default")
        {
            msg = msg.Tag("scenario", _specificTag);
        }






        using var writeApi = _client.GetWriteApi();
        writeApi.WritePoint(bucket: Bucket, org: Org, point: msg);
        
        Console.WriteLine("[Notification] Message logged to InfluxDB");
      
    }

}