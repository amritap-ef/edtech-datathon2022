import os
import json
from elasticsearch import Elasticsearch

def _get_elasticsearch_url():
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    elasticsearch_fpath = os.path.join(curr_dir, "..", "secrets/elasticsearch.json")
    with open(elasticsearch_fpath) as f:
        d = json.load(f)
        es_url = d["url"] + ":" + d["port"]
    return es_url


def recomm_content(phrase, cefr_level, content_type: list, es_url):
    es = Elasticsearch(
        es_url,
        max_retries=10
    )
    INDEX_NAME = "test"
    body = {
      "_source": [
        "metadata.headline",
        "metadata.url",
        "metadata.article_body_html",
        "metadata.author",
        "cefr.pred"
        ],
      "query": {
        "bool": {
          "must": [
            {
            "terms": {
              "cefr.pred": [
                cefr_level
              ]
            }
            },
            {
              "multi_match": {
                  "query": phrase,
                  "fields": ["metadata.headline^4", "metadata.description^2"],
                  "type": "best_fields"
                }
            }
        ]}
      }
    }
    results = es.search(index=INDEX_NAME, body=body)
    results = results["hits"]["hits"][:3]

    return results

