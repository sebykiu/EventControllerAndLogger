namespace EventControllerAndLogger.Json;

public class Message
{
    public string Id { get; set; }
    
    public string Path { get; set; }
    public string Instruction { get; set; }
    public Coordinates Coordinates { get; set; }
}