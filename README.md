
## mag2elasticsearch


## Install Elasticsearch with Docker
```
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.3.2
```

```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.3.2
```



## Prerequisites
Expected package dependencies are listed in the "requirements.txt" file for PIP, you need to run the following command to get dependencies:
```
pip install -r requirements.txt
```

### Command-line usage
Index --authors .
- Get help use  [under implementation]
```
    python main.py --authors --onlyInstitutions 75951250 4577782 39343248 7877124 --limit 6000000
```
- limit by number of record read from files
```
    python main.py --authors --limit 6000000
```
