# EventControllerAndLogger

Event Controller and Logger (ECAL) is a subpart of the [3D Unity Stack](https://github.com/skiunke/CrownetUnity) based on the [Crownet Project](https://crownet.org/).

ECAL is completely optional as Omnet++ supports direct communication to Unity, but has some unique and helpful features.


## Installation


```shell
git clone https://github.com/skiunke/EventControllerAndLogger.git ecal
```
## Usage
> ECAL runs inside the rovernet network and is therefore accessibly by accessing the corresponding docker name (ecal, influxdb)


Verify the [Config](https://github.com/skiunke/EventControllerAndLogger/blob/main/EventControllerAndLogger/config.yaml) before running ECAL to change ip-addresses where needed or to disable / enable services.

```shell
cd ecal
# This will create and run images of ECAL and local influxdb 
# see: https://github.com/skiunke/EventControllerAndLogger/blob/main/docker-compose.yaml
bash run.sh
```


### 1. Precise InfluxDB logging
By default ECAL loggs every message received to [InfluxDB](https://www.influxdata.com/) a time-series database.


> Data can be viewed and queried under: https://localhost:8086
> > Username: admin <br>
> > Password: password

### 2. InfluxPlay
- Playback stored messages in InfluxDB from a specific scenario.
- Speed up or slow down the playback.
- Load custom scenarios from json files

Run [run.py](https://github.com/skiunke/EventControllerAndLogger/blob/main/InfluxPlay/run.py) to execute Scenario1 by default.


Supported Scenarios:

| Name            	 | Description                                                               	|
|-------------------|---------------------------------------------------------------------------	|
| ConnectionTest  	 | Sends packet to Unity. On success a green message is displayed.    	|
| Scenario2       	 | Creates a person, vehicle and stationary.                                 	|
|  Scenario1       	 | Creates 3 persons and moves them to a different location after 5 seconds.       	|


### 3. Accelerated development

Change the functionality in ECAL and rebuild the docker images instead of recompiling the whole Omnet++ simulation.