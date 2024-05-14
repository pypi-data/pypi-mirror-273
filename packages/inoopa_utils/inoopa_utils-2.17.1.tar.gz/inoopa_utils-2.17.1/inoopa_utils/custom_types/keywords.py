from bson import ObjectId
from typing import Literal
from dataclasses import dataclass


@dataclass(slots=True)
class Keyword:
    """Keyword dataclass to store the extracted keywords from a copmany's online content."""
    # The id of the keyword in the wikidata database, this used to standerdize the keywords
    wiki_data_id: str
    keyword_type: Literal["topic", "entity"]
    # Scores are from TextRazor
    confidence_score: float # Between 0 and 1
    label_en: str
    label_fr: str | None = None
    label_nl: str | None = None
    relevance_score: float | None = None # Between 0 and 1
    # The keyword's text itself



@dataclass(slots=True)
class CompanyKeywords:
    _id: ObjectId
    company_id: str # _id filed from a Company
    keywords: list[Keyword]


def convert_dict_to_keyword_list(company_keywords_dict: dict) -> CompanyKeywords:
    """
    Convert a dict to a CompanyKeywords object.

    :param company_keywords_dict: The dict to convert.
    :return: A CompanyKeywords object.
    """
    return CompanyKeywords(
        _id=company_keywords_dict['_id'],
        company_id=company_keywords_dict['company_id'],
        keywords=[Keyword(**keyword) for keyword in company_keywords_dict['keywords']]
    )
