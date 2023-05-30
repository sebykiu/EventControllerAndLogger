# EventControllerAndLogger

Event Controller and Logger (ECAL) is a subpart of the [3D Unity Stack](https://github.com/skiunke/CrownetUnity) based on the [Crownet Project](https://crownet.org/).

ECAL is completely optional as Crownet supports direct communication to Unity, but has some unique and helpful features.


## Installation


```shell
git clone https://github.com/skiunke/EventControllerAndLogger.git ecal
```
## Usage
Verify the [Config](https://github.com/skiunke/EventControllerAndLogger/blob/main/EventControllerAndLogger/config.yaml) before running ECAL to change ip-addresses where needed or to disable / enable services.

```shell
cd ecal
docker-compose up
```


### 1. Precise InfluxDB logging
By default ECAL loggs every message received to [InfluxDB](https://www.influxdata.com/) a time-series database.


> Data can be viewed and queried under: https://localhost:8086
> > Username: admin <br>
> > Password: password

### 2. Unity of playback
Use stored messages in InfluxDB or any other source to control unity to gain the following benefits:
- Control playback speed
- Select specific time frame
- Disable / modify specific message


### 3. Accelerated development

Change the functionality in ECAL and rebuild the docker images instead of recompiling the whole Omnet++ simulation.