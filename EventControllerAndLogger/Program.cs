// See https://aka.ms/new-console-template for more information

using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Configuration.Yaml;

namespace EventControllerAndLogger;

abstract class Program
{
    static void Main()
    {
        var builder = new ConfigurationBuilder().SetBasePath(Directory.GetCurrentDirectory())
            .AddYamlFile("config.yaml", optional: false, reloadOnChange: true);
        IConfiguration configuration = builder.Build();
        var appConfig = new AppConfig();
        configuration.Bind(appConfig);

        Console.WriteLine(
            $"UseUnity: OmnetPort: {appConfig.OmnetPort}, InfluxAddr: {appConfig.InfluxAddr}, InfluxPort: {appConfig.InfluxPort}. SpecificTag: {appConfig.SpecificTag}");

        Ecal _ = new Ecal(appConfig);
    }
}