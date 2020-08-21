import classifier.settings as settings
import logging
import traceback
import json
from elasticsearch import Elasticsearch

index_exists = settings.client.indices.exists(index=settings.INDEX_NAME)
LOG = logging.getLogger(__name__)

def all_rules():
    if index_exists == False:
        LOG.exception("Database not found")
        return ({"ERROR":"Database not found"},False)
        
    else:
        try:
            rules = settings.client.search(index=settings.INDEX_NAME)
            count = settings.client.count(index=settings.INDEX_NAME)['count']
            rule = rules['hits']['hits']
            output = []            
            dictionary = {}
            
            if(count > 0):
                for rule in rules['hits']['hits']:
                    output.append(rule['_source'])
                
                for i, b in enumerate(output):
                    dictionary[f"rule_{i}"] = b
                return dictionary, True
            else:
                LOG.exception("No rule found: Database is empty")
                return({"ERROR":"No rule found: Database is empty"},False)

        except Exception as err:
            return({"EXCEPTION":LOG.error(traceback.format_exc())},False)
            
if __name__ == '__main__':
    all_rules()