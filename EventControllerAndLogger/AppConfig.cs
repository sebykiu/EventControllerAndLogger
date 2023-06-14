namespace EventControllerAndLogger;

public class AppConfig
{
    public bool UseUnity { get; set; }
    public bool UseCrownet { get; set; }
    public bool UseInflux { get; set; }
    public int OmnetPort { get; set; }
    public string UnityAddr { get; set; }
    public int UnityPort { get; set; }
    public string InfluxAddr { get; set; }
    public int InfluxPort { get; set; }

    public string SpecificTag { get; set; }

}