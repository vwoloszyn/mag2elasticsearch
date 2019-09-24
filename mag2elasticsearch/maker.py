import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch



def paperAuthorAffiliations2elastic(config, arg):

    institutions=arg.onlyInstitutions
    file_name=config["mag"]["PaperAuthorAffiliations"]
    limit=arg.limit
    cs=1000000
    dataset=[]
    count=0
    print ("reading "+file_name)
    for chunk in pd.read_csv(file_name,error_bad_lines=False, sep="\t", header=None, names=["PaperId","AuthorId","AffiliationId","AuthorSequenceNumber","OriginalAuthor","OriginalAffiliation"], chunksize=cs, iterator=True, low_memory=False):
        if (institutions):
            sample_df = chunk[(chunk["AffiliationId"].isin(institutions))]
        else:
            sample_df=chunk
        if len(sample_df)>0:
            #print ("achou")
            dataset.append(sample_df)
        count+=cs
        if ((limit>0) and (count>limit)):
            print ("break")
            print (count)
            break

    pdf = pd.concat(dataset)

    es=Elasticsearch([{'host':config["es"]["host"],'port':config["es"]["port"]}])
    df2elasticsearch(pdf,es,INDEX=config["es"]["index"],TYPE= "PaperAuthorAffiliations")

    return pdf


def papers2elastic(papersId, config, arg):
    #print (papersId)
    limit=arg.limit
    cs=1000000
    dataset=[]
    count=0
    file_name=config["mag"]["Papers"]
    print ("reading "+file_name)
    for chunk in pd.read_csv(file_name,error_bad_lines=False, sep="\t", header=None, names=["0","PaperId","Rank","Doi","DocType", "PaperTitle","OriginalTitle","BookTitle","Year","Date","Publisher","JournalId","ConferenceSeriesId","ConferenceInstanceId","Volume","Issue","FirstPage","LastPage","ReferenceCount","CitationCount","EstimatedCitation","OriginalVenue","CreatedDate"]
, chunksize=cs, iterator=True, low_memory=False):
        if papersId:
            #print (set(list(chunk["PaperId"])))
            sample_df = chunk[chunk["PaperId"].isin(papersId)]
        else:
            sample_df = chunk
        if len(sample_df)>0:
            #print("achou")
            dataset.append(sample_df)
        count+=cs
        if ((limit>0) and (count>limit)):
            #print ("break")
            #print (count)
            break

    pdf = pd.concat(dataset)

    if len(pdf)>0:
        es=Elasticsearch([{'host':config["es"]["host"],'port':config["es"]["port"]}])
        df2elasticsearch(pdf,es,INDEX=config["es"]["index"],TYPE= "Papers")

    return pdf








def df2elasticsearch(df,e,INDEX="dataframe",TYPE= "record"):
    def rec_to_actions(df):
        import json
        for record in df.to_dict(orient="records"):
            yield ('{ "index" : { "_index" : "%s", "_type" : "%s" }}'% (INDEX, TYPE))
            yield (json.dumps(record, default=int))

    r = e.bulk(rec_to_actions(df)) # return a dict
    #if not e.indices.exists(INDEX):
    #    raise RuntimeError('index does not exists, use `curl -X PUT "localhost:9200/%s"` and try again'%INDEX)
    print(not r["errors"])
