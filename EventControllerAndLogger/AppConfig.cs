namespace EventControllerAndLogger;

public class AppConfig
{
    public int OmnetPort { get; set; }
    public string InfluxAddr { get; set; }
    public int InfluxPort { get; set; }

    public string SpecificTag { get; set; }

}