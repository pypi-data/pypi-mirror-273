import re
from functools import lru_cache

import paperqa
import requests
from paperqa.types import Answer, PromptCollection
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    computed_field,
    field_validator,
    validator,
)

from .utils import get_pqa_key, get_pqa_url


class AgentPromptCollection(BaseModel):
    agent_prompt: str = ""
    agent_search_tool: str = ""
    search_count: int = 8
    wipe_context_on_answer_failure: bool = True
    timeout: float = 500  # seconds


def _extract_doi(citation: str) -> str | None:
    doi = re.findall(r"10\.\d{4}/\S+", citation, re.IGNORECASE)
    if len(doi) > 0:
        return doi[-1]
    return None


# we have to put it here to avoid circular imports
# because we use this in the default factory of the QueryRequest
@lru_cache(maxsize=100)
def get_prompts() -> tuple[dict[str, PromptCollection], AgentPromptCollection]:
    url = f"{get_pqa_url()}/api/prompts/all"
    with requests.Session() as session:
        response = session.get(
            url,
            headers={"Authorization": f"Bearer {get_pqa_key()}"},
        )
        response.raise_for_status()
        result = response.json()
    return (
        {
            k: PromptCollection.model_validate(v["prompt-collection"])
            for k, v in result.items()
        },
        AgentPromptCollection.model_validate(result["default"]["agent-prompt"]),
    )


class UploadMetadata(BaseModel):
    filename: str
    citation: str
    key: str | None = None


class Doc(paperqa.Doc):
    doi: str | None = None

    @validator("doi", pre=True)
    def citation_to_doi(cls, v: str | None, values: dict) -> str | None:  # noqa: N805
        if v is None and "citation" in values:
            return _extract_doi(values["citation"])
        return v


class DocsStatus(BaseModel):
    name: str
    llm: str
    summary_llm: str
    docs: list[Doc]
    doc_count: int
    writeable: bool = False


# COPIED FROM paperqa-server!
class QueryRequest(BaseModel):
    query: str
    group: str | None = None
    llm: str = "gpt-4-0613"
    summary_llm: str = "gpt-3.5-turbo-0125"
    length: str = "about 200 words, but can be longer if necessary"
    summary_length: str = "about 100 words"
    max_sources: int = 7
    consider_sources: int = 12
    named_prompt: str | None = None
    # if you change this to something other than default
    # modify code below in update_prompts
    prompts: PromptCollection = Field(
        default_factory=lambda: get_prompts()[0]["json"], validate_default=True
    )
    agent_tools: AgentPromptCollection = Field(default_factory=lambda: get_prompts()[1])
    texts_index_mmr_lambda: float = 0.9
    docs_index_mmr_lambda: float = 0.5
    embedding: str = "hybrid-text-embedding-3-small"
    # concurrent number of summary calls to use inside Doc object
    max_concurrent: int = 12
    temperature: float = 0.0
    summary_temperature: float = 0.0

    @field_validator("max_sources")
    @classmethod
    def max_sources_for_gpt(cls, v: int, info: ValidationInfo) -> int:
        values = info.data
        if "gpt" in values["llm"] and v > 10:  # noqa: PLR2004
            raise ValueError("Max sources for GPT models is 10")
        return v

    @field_validator("prompts")
    @classmethod
    def update_prompts(
        cls,
        v: PromptCollection,
        info: ValidationInfo,
    ) -> PromptCollection:
        STATIC_PROMPTS, _ = get_prompts()
        values = info.data
        if values["named_prompt"] is not None:
            if values["named_prompt"] not in STATIC_PROMPTS:
                raise ValueError(
                    f"Named prompt {values['named_prompt']} not in {list(STATIC_PROMPTS.keys())}"
                )
            v = STATIC_PROMPTS[values["named_prompt"]]
        if values["summary_llm"] == "none":
            v.skip_summary = True
            # for simplicity (it is not used anywhere)
            # so that Docs doesn't break when we don't have a summary_llm
            values["summary_llm"] = "gpt-3.5-turbo"
        return v


class AnswerResponse(BaseModel):
    answer: Answer
    usage: dict[str, list[int]]
    bibtex: dict[str, str]
    status: str
    timing_info: dict[str, dict[str, float]] | None = None
    duration: float = 0


class ScrapeRequest(BaseModel):
    """This was copied from paperqa-server as of shortened commit 452c6fc."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    question: str = ""
    limit: int = Field(
        default=5,
        description=(
            "Target minimum number of papers to scrape. Note that we may not pull this"
            " many in some scenarios (e.g. if scraper fails on many papers)."
        ),
    )
    query: str | None = None
    year: str | None = None
    search_type: str = "default"
    offset: int = 0

    @computed_field  # type: ignore[misc]
    @property
    def use_internal_scrapers(self) -> bool: ...  # type: ignore[empty-body]
