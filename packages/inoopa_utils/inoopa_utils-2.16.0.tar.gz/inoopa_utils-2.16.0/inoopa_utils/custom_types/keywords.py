from bson import ObjectId
from typing import Literal
from dataclasses import dataclass


@dataclass(slots=True)
class Keyword:
    """Keyword dataclass to store the extracted keywords from a copmany's online content."""
    # The id of the keyword in the wikidata database, this used to standerdize the keywords
    wiki_data_id: str
    # The keyword's text itself
    label: str
    keyword_type: Literal["topic", "entity"]
    # Scores are from TextRazor
    confidence_score: float # Between 0 and 1
    relevance_score: float | None = None # Between 0 and 1



@dataclass(slots=True)
class CompanyKeywords:
    _id: ObjectId
    company_id: str # _id filed from a Company
    keywords: list[Keyword]
    language: Literal["fr", "en", "nl"]


def convert_dict_to_keyword_list(company_keywords_dict: dict) -> CompanyKeywords:
    """
    Convert a dict to a CompanyKeywords object.

    :param company_keywords_dict: The dict to convert.
    :return: A CompanyKeywords object.
    """
    return CompanyKeywords(
        _id=company_keywords_dict['_id'],
        company_id=company_keywords_dict['company_id'],
        language=company_keywords_dict['language'],
        keywords=[Keyword(**keyword) for keyword in company_keywords_dict['keywords']]
    )
