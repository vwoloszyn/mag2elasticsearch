
## Using Elasticsearch on Microsoft Academic Graph MAG
Exploring more than 161.4 GiB of publications from Microsoft Academic Graph (MAG) using Elasticsearch!


## 1. Download Microsoft Academic Graph

https://docs.microsoft.com/en-us/academic-services/graph/reference-data-schema
https://zenodo.org/record/2628216

4564007 Affiliations.txt
 16528778635 Authors.txt
     2224843 ConferenceInstances.txt
      428103 ConferenceSeries.txt
    55188690 FieldsOfStudy.txt
     5689662 Journals.txt
 40976541540 PaperAuthorAffiliations.txt
 32446006785 PaperReferences.txt
     7763592 PaperResources.txt
 60213784152 Papers.txt
 23096534376 PaperUrls.txt
 ----------------------------------------
173337504385 (~161.4) GiB


## 2. Install Elasticsearch with Docker
```
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.3.2
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.3.
```

For more information: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

## 3. Install mag2elasticsearch

Expected package dependencies are listed in the "requirements.txt" file for PIP, you need to run the following command to get dependencies:
```
git clone https://github.com/vwoloszyn/mag2elasticsearch/
pip install -r requirements.txt
```

### Command-line usage
Index --PaperAuthorAffiliations.
```
    python main.py --PaperAuthorAffiliations
```
- read only N records
```
    python main.py --authors --limit 6000000
```
- Only institutions with id_
```
    python main.py --onlyInstitutions 75951250 4577782 39343248 7877124
```
