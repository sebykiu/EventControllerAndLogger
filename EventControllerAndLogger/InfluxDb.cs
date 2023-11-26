using EventControllerAndLogger.Json;
using InfluxDB.Client;
using InfluxDB.Client.Api.Domain;
using InfluxDB.Client.Writes;

namespace EventControllerAndLogger;

public class InfluxDb
{
    const string Token = "secret-token";
    const string Bucket = "crownet";
    const string Org = "rovernet";

    private readonly InfluxDBClient _client;
    private readonly string _specificTag;
    private readonly List<PointData> _pointDataBuffer;
    private readonly int _maxBufferSize;
    public InfluxDb(string influxAddr, int influxPort, string specificTag, int maxBufferSize)


    {
        _client = new InfluxDBClient($"http://{influxAddr}:{influxPort}", Token);
        _specificTag = specificTag;
        _pointDataBuffer = new List<PointData>();
        _maxBufferSize = maxBufferSize;
    }

    public void WriteToDatabase(Message message)
    {
        PointData msg = PointData.Measurement("omnet++")
            .Field("SourceId", message.SourceId)
            .Field("TargetId", message.TargetId)
            .Field("ObjectType", message.ObjectType)
            .Field("X", message.Coordinates.X)
            .Field("Y", message.Coordinates.Y)
            .Field("Z", message.Coordinates.Z)
            .Field("SimTime", message.SimTime)
            .Timestamp(DateTime.UtcNow, WritePrecision.Ns);

        if (_specificTag != "default")
        {
            msg = msg.Tag("scenario", _specificTag);
        }

        _pointDataBuffer.Add(msg);

        if (_pointDataBuffer.Count >= _maxBufferSize)
        {
            FlushData();
        }
    }

    private void FlushData()
    {
        using var writeApi = _client.GetWriteApi();
        writeApi.WritePoints(bucket: Bucket, org: Org, points: _pointDataBuffer);
        _pointDataBuffer.Clear();
        Console.WriteLine($"[Notification] {_pointDataBuffer.Count} messages logged to InfluxDB");
    }

    public void Dispose()
    {
        if (_pointDataBuffer.Count > 0)
        {
            FlushData();
            
        }
        _client.Dispose();
    }
}