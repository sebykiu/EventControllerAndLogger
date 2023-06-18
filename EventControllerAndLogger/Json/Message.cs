namespace EventControllerAndLogger.Json;

public class Message
{
    public string SourceId { get; set; }
    
    public string TargetId { get; set; }

    public Coordinates Coordinates { get; set; }
   
    public string ObjectType { get; set; }
}
