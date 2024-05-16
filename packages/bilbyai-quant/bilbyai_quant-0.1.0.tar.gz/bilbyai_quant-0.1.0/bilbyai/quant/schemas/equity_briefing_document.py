from .base_briefing_document import BaseBriefingDocument, base_briefing_document_mappings

equity_briefing_document_mappings = {
    "properties": {
        # Include the base mappings
        **base_briefing_document_mappings["properties"],
    }
}


class EquityBriefingDocument(BaseBriefingDocument):
    # inherits fields from BaseBriefingDocument.
    pass
