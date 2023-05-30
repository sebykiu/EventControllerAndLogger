// See https://aka.ms/new-console-template for more information

using EventControllerAndLogger.Controller;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Configuration.Yaml;

namespace EventControllerAndLogger;

class Program
{
    static void Main(string[] args)
    {
        var builder = new ConfigurationBuilder().SetBasePath(Directory.GetCurrentDirectory())
            .AddYamlFile("config.yaml", optional: false, reloadOnChange: true);
        IConfiguration configuration = builder.Build();
        var appConfig = new AppConfig();
        configuration.Bind(appConfig);
        
        Console.WriteLine($"UseUnity: {appConfig.UseUnity}, UseCrownet: {appConfig.UseCrownet}, UseInflux: {appConfig.UseInflux}, OmnetPort: {appConfig.OmnetPort}, UnityAddr: {appConfig.UnityAddr}, UnityPort: {appConfig.UnityPort}, InfluxAddr: {appConfig.InfluxAddr}, InfluxPort: {appConfig.InfluxPort}");

        
        
        var ecal = new ECAL(appConfig);
    }
}