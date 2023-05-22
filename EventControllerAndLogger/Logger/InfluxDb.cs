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
    private InfluxDBClient _client;

    public InfluxDb()
    { _client = InfluxDBClientFactory.Create("http://influxdb:8086", Token);
    }

    public void WriteToDatabase(Message message)
    {
        
        var msg = PointData
            .Measurement("omnet++")
            .Field("Id", message.Id).Field("Instruction", message.Instruction)
            .Field("X", message.Coordinates.X)
            .Field("Y", message.Coordinates.Y).Field("Z", message.Coordinates.Z)
            .Timestamp(DateTime.UtcNow, WritePrecision.Ns);
        


        using var writeApi = _client.GetWriteApi();
        writeApi.WritePoint(bucket: Bucket, org: Org, point: msg);
        
        Console.WriteLine("Wrot to database");
      
    }

}