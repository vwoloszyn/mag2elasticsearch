import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch



def authors2elastic(config,arg):
    def read_authors_file(institutions,file_name,limit):
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
                print ("achou")
                dataset.append(sample_df)
            count+=cs
            if ((limit>0) and (count>limit)):
                print ("break")
                print (count)
                break
        sample_df = pd.concat(dataset)
        return sample_df


    #########
    pdf= read_authors_file(arg.onlyInstitutions,config["mag"]["PaperAuthorAffiliations"],arg.limit)

    es=Elasticsearch([{'host':config["es"]["host"],'port':config["es"]["port"]}])
    df2elasticsearch(pdf,es,INDEX=config["es"]["index"],TYPE= "user")











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
