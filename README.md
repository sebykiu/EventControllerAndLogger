# Event Controller and Logger (ECAL)

> ⚠️ This project is designed to only run in a local network and therefore doesn't provide advanced security features.<br>


ECAL is a subpart of the [GitHub - 3D Unity Stack](https://github.com/skiunke/CrownetUnity) based on [CrowNet](https://crownet.org/) and
enables message logging to a local InfluxDB instance, that can later be played back to Unity with InfluxPlay. Alternatively JSON files are used.

### Dependencies
- Docker
- Docker Compose
- Python3 (required for InfluxPlay)

### Installation

```shell
git clone https://github.com/skiunke/EventControllerAndLogger.git ecal
```

### Usage
By Default ECAL only records and stores Messages in InfluxDB and does not forward them to Unity as InfluxPlay allows more granular controls.
Settings can be change in the [Config](https://github.com/skiunke/EventControllerAndLogger/blob/main/EventControllerAndLogger/config.yaml) file. This requires a rerun of the build_and_run script.

The shell script:
- Pulls InfluxDB and builds ECAL.
- Waits for OMNeT++ to connect or InfluxPlay to be used for message playback.


```shell
# /ecal
bash build_and_run.sh
```

 

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
# /ecal/InfluxPlay
python3 run.py --help
```

Execution of a JSON based scenario:

```shell
# /ecal/InfluxPlay
python3 run.py --json-path Scenarios/Freiheit.json
```

Execution of a InfluxDB based scenario:

```shell
# /ecal/InfluxPlay
python3 run.py --scenario vruMec 
```