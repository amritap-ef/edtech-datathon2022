import os
import json
from elasticsearch import Elasticsearch

INDEX_NAME = "test"
def _get_elasticsearch_url():
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    elasticsearch_fpath = os.path.join(curr_dir, "..", "secrets/elasticsearch.json")
    with open(elasticsearch_fpath) as f:
        d = json.load(f)
        es_url = d["url"] + ":" + d["port"]
    return es_url


def index_exact_search_relevance_metadata(phrase, cefr_level, content_type: list, es_url):
    es = Elasticsearch(
        es_url,
        max_retries=10
    )

    body = {
      "_source": [
        "metadata.headline",
        "metadata.url",
        "metadata.article_body_html",
        "metadata.author",
        "cefr.pred",
        "topic_classification.topic",
        "metadata.type",
        "captions.start"
      ],
      "query": {
        "bool": {
          "must": [
            {
                "terms": {
                  "metadata.type": content_type
                }
            },
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

def index_exact_search_relevance_captions(keywords: str, cefr_level: str, es_url) -> dict:
    es = Elasticsearch(
        es_url,
        max_retries=10
    )

    query_exact_search = {
        "_source": [
            "metadata.source",
            # "metadata.show_name",
            "metadata.author",
            "metadata.description",
            "metadata.headline",
            "metadata.date_published",
            "metadata.publisher",
            "metadata.url",
            "captions.evp.tags.label",
            "captions.evp.tags.text",
            "captions.evp.tags.url",
            "captions.evp.tags.text",
            "cefr.pred",
            "sentiment",
            "evp",
            "style"
        ],
        "size": 3,
        "query": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "metadata.type": ["video"]
                        }
                    },
                    {
                        "terms": {
                            "cefr.pred.keyword": [cefr_level]
                        }
                    },
                    {
                        "nested": {
                            "path": "captions",
                            "score_mode": "avg",
                            "query": {
                                "multi_match": {
                                    "query": keywords,
                                    "type": "phrase",
                                    "fields": ["captions.text"]
                                }
                            },
                            "inner_hits": {
                                "highlight": {
                                    "pre_tags": ["<mark>"],
                                    "post_tags": ["</mark>"],
                                    "fields": {
                                        "captions.text": {}
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }
    }

    results = es.search(index=INDEX_NAME, body=query_exact_search)
    results = results["hits"]["hits"]
    return results
