from .base_briefing_document import BaseBriefingDocument, base_briefing_document_mappings

commodity_briefing_document_mappings = {
    "properties": {
        # Include the base mappings
        **base_briefing_document_mappings["properties"],
        #
        # sentimentExtremity is a value between 0 and 1, so it should be a float field
        # 0.0 ~ 1.0
        "sentimentExtremity": {"type": "float"},
        #
        # relevantCommodity is categorical, but the list of values evolves continuously,
        # so it should be a text field. It should be the same value as theme
        "relevantCommodity": {
            "type": "text",
            # The keyword field is used for sorting and aggregations
            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
        },
        #
        # impactPrediction is categorical, so it should be a keyword field
        # ["impact", "no impact"]
        "impactPrediction": {"type": "keyword"},
        #
        # demandSupplyPrediction is categorical, so it should be a keyword field
        # ["demand", "supply", "no prediction"]
        "demandSupplyPrediction": {"type": "keyword"},
    }
}


class CommodityBriefingDocument(BaseBriefingDocument):
    # inherits fields from BaseBriefingDocument.
    relevantCommodity: str
    impactPrediction: str
    demandSupplyPrediction: str
