# Event Controller and Logger (ECAL)

> ⚠️ This project is designed to only run in a local network and therefore doesn't provide advanced security features.<br>


ECAL is a subpart of the [GitHub - 3D Unity Stack](https://github.com/skiunke/CrownetUnity) based on [CrowNet](https://crownet.org/) and
enables message logging to a local InfluxDB instance, that can later be played back to Unity with InfluxPlay. Alternatively JSON files are used.

### Dependencies
- Docker
- Docker - Compose
- Python3

### Installation

```shell
git clone https://github.com/skiunke/EventControllerAndLogger.git ecal
```

### Usage

The shell script:
- Instantiates InfluxDB
- Builds ECAL
- Sets up the Docker Network
- and starts the service to record messages or play back with InfluxPlay

```shell
# /ecal
bash build_and_run.sh
```

By default ECAL only records and does not forward to Unity automatically as the InfluxPlay module allows more granular controls. The default ports 
and settings 
can be viewed and changed 
in the
[Config](https://github.com/skiunke/EventControllerAndLogger/blob/main/EventControllerAndLogger/config.yaml). This requires a restart. 
 

> InfluxDB is locally accessible under: https://localhost:8086 <br>
> > Username: admin <br>
> > Password: password

## Message Playback

Messages stored in the InfluxDB database or in JSON files are played back to Unity by the InfluxPlay module.

### Installation

```shell
# /ecal/InfluxPlay
pip3 install -r requirements.txt
```

### Usage

Usage options:

```shell
python3 run.py --help
```

Execution of a JSON based scenario:

```shell
python3 run.py --json-path Scenarios/Freiheit.json
```

Execution of a InfluxDB based scenario:

```shell
python3 run.py --scenario vruMec 
```