// See https://aka.ms/new-console-template for more information

using EventControllerAndLogger;
using EventControllerAndLogger.Controller;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Configuration.Yaml;


class Program
{
    static void Main(string[] args)
    {
        var builder = new ConfigurationBuilder().SetBasePath(Directory.GetCurrentDirectory())
            .AddYamlFile("config.yaml", optional: false, reloadOnChange: true);
        IConfiguration configuration = builder.Build();
        var appConfig = new AppConfig();
        configuration.Bind(appConfig);

        new ECAL();
        
    }
}

