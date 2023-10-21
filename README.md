# Event Controller and Logger (ECAL)

ECAL is a subpart of the [3D Unity Stack](https://github.com/skiunke/CrownetUnity) based on [CrowNet](https://crownet.org/) and
enables message logging to a local InfluxDB instance, that can later be played back to Unity with InfluxPlay. Alternatively JSON files are used.

### Installation

```shell
git clone https://github.com/skiunke/EventControllerAndLogger.git ecal
```

### Usage

> ⚠️ The containers must run for both recording and InfluxPlay as it deploys the InfluxDB instance.

Builds a local InfluxDB instance and the ECAL C# project in the same docker network as OMNeT++ and therefore allows accessing by
the corresponding docker name (ecal, influxdb).

```shell
# /ecal
bash build.sh
```

By default ECAL only records and does not forward to Unity automatically. The default ports and settings can be viewed and changed in the
[Config](https://github.com/skiunke/EventControllerAndLogger/blob/main/EventControllerAndLogger/config.yaml).


> InfluxDB is locally accessible under: https://localhost:8086
> > Username: admin <br>
> > Password: password

## Message Playback

Messages stored in the InfluxDB database or in JSON files are played back to Unity with the InfluxPlay package.

### Installation

```shell
# /ecal/InfluxPlay
pip3 install -r requirements.txt
```

### Usage

> ⚠️ Both ECAL and Unity must be running before executing the scenario.

To execute a default testing scenario:

```shell
python3 run.py
```

To execute another JSON Scenario:

```shell
python3 run.py --ip localhost --port 54321 --json-path Scenarios/Freiheit.json
```

To execute a Scenario from InfluxDB:

```shell
python3 run.py --ip localhost --port 54321 --scenario vruMec 
```