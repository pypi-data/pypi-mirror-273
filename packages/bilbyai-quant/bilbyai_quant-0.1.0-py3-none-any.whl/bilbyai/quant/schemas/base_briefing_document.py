from typing import Optional

from pydantic import BaseModel

base_briefing_document_mappings = {
    "properties": {
        # ID should be a keyword because it is structured content
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html
        "id": {"type": "keyword", "index": False},
        #
        # Date is a date
        "date": {"type": "date"},
        #
        # Title, summary, and subtitle are human-readable and searchable text fields,
        # so they should be text fields
        "titleEn": {
            "type": "text",
            # The keyword field is used for sorting and aggregations
            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
        },
        "summaryEn": {
            "type": "text",
            # The keyword field is used for sorting and aggregations
            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
        },
        "subtitleEn": {
            "type": "text",
            # The keyword field is used for sorting and aggregations
            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
        },
        #
        # policyLifecyclePrediction is a fixed set of numbers,
        # so it should be an integer field
        # early [1, 2, 3, 4, 5, 6] late
        "policyLifecyclePrediction": {"type": "integer"},
        #
        # importancePrediction is categorical, so it should be a keyword field
        # least important [1, 2, 3, 4, 5] most important
        "importancePrediction": {"type": "integer"},
        #
        # url is a URL string, so it should be a keyword field
        "url": {"type": "keyword"},
        #
        # copies is a natural number (i.e. 0, 1, 2, 3, ...),
        # so it should be an integer field
        "copies": {"type": "integer"},
        #
        # source is a keyword because it is structured content
        "source": {"type": "keyword"},
        #
        # sourceLabel is a keyword because it is structured content
        "sourceLabel": {"type": "keyword"},
        #
        # sentiment is categorical, so it should be a keyword field
        # ["positive", "neutral", "negative"]
        "sentiment": {"type": "keyword"},
        #
        # sentimentScore is a float value between 0 and 1, so it should be a float field
        "sentimentScore": {"type": "float"},
        #
        # relevanceRank is a natural number (i.e. 1, 2, 3, ...),
        # so it should be an integer field
        "relevanceRank": {"type": "integer"},
        #
        # theme is is categorical, but the list of values evolves continuously,
        # so it should be a text field with a keyword subfield for sorting and aggregations
        "theme": {
            "type": "text",
            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
        },
    }
}


class BaseBriefingDocument(BaseModel):
    id: str
    date: str
    titleEn: str
    summaryEn: str
    subtitleEn: Optional[str]
    policyLifecyclePrediction: int
    importancePrediction: int
    sentiment: str
    sentimentScore: float
    sentimentExtremity: float
    theme: str
    relevanceRank: int
    url: str
    copies: int
    source: str
    sourceLabel: str
