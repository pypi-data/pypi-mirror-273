"""LLM Judge for context relevance"""

from typing import Optional, List

from mlflow.metrics.genai import make_genai_metric, EvaluationExample
from mlflow.metrics import EvaluationMetric

# TODO: Add support for multiple versions. Right now this is pinned to v1.
_V1 = {
    "definition": (
        """
        Given the following question (which is labeled as "input") and document (which is labeled as "output"), you must 
        analyze the provided document and determine whether it is 
        sufficient for answering the question. In your evaluation, you should consider the content of the document and 
        how it relates to the provided question. Scores should reflect "
        "the extent to which the document (given as "output") is relevant to amd can sufficiently answer "
        "the question (given as "input").
        """
    ),
    "grading_prompt": (
        "Context relevance: Below are the details for different scores:"
        "- Score 1: The document is irrelevant or insufficient for answering the question. "
        "- Score 5: The document is relevant and sufficient for answering the question."
    ),
    "default_examples": [
        EvaluationExample(
            input="what is non controlling interest on balance sheet",
            output="""In accounting, minority interest (or non-controlling interest) is the portion of a subsidiary 
            corporation's stock that is not owned by the parent corporation. The magnitude of the minority interest 
            in the subsidiary company is generally less than 50% of outstanding shares, or the corporation would 
            generally cease to be a subsidiary of the parent.[1]""",
            grading_context={},
            score=5,
            justification="The document explains what is a non-controlling interest and is thus relevant and sufficient "
            "in addressing the question about a non controlling interest on a balance sheet.",
        ),
        EvaluationExample(
            input="how many episodes are in chicago fire season 4",
            output="""The fourth season of Chicago Fire, an American drama television series with executive producer 
            Dick Wolf, and producers Derek Haas, Michael Brandt, and Matt Olmstead, was ordered on February 5, 2015, 
            by NBC,[1] and premiered on October 13, 2015 and concluded on May 17, 2016.[2] The season
            contained 23 episodes.[3]""",
            grading_context={},
            score=5,
            justification="The document provides information about the fourth season of Chicago fire, including the"
            "number of episodes in that season. Hence, it is relevant and sufficient to answer the input"
            "question.",
        ),
        EvaluationExample(
            input="how many episodes are in chicago fire season 4",
            output=""""Love Will Keep Us Alive" is a song written by Jim Capaldi, Paul Carrack, and Peter Vale, and 
            produced by the Eagles, Elliot Scheiner, and Rob Jacobs. It was first performed by the Eagles in 1994, 
            during their "Hell Freezes Over" reunion tour, with lead vocals by bassist Timothy B. Schmit.""",
            grading_context={},
            score=1,
            justification="The document provides information about a song perfomed by the Eagles, which is neither "
            "relevant nor sufficient to answer the input question about the number of episodes in "
            "the fourth season of chicago fire.",
        ),
        EvaluationExample(
            input="who is the leader of the ontario pc party",
            output=""""According to Unfinished Tales, at the start of the War of the Elves and Sauron, Celebrimbor gave 
            Narya together with the Ring Vilya to Gil-galad, High King of the Noldor. Gil-galad entrusted Narya to his 
            lieutenant Círdan, Lord of the Havens of Mithlond, who kept it after Gil-galad's death. According to The 
            Lord of the Rings, Gil-galad received only Vilya, while Círdan received Narya from the very beginning 
            along with Galadriel receiving Nenya from the start.""",
            grading_context={},
            score=1,
            justification="The document provides information about the lore of the Lord of the Rings, which is neither"
            "relevant nor sufficient to answer the input question about the leader of the pc party in "
            "Ontario",
        ),
    ],
    "default_parameters": {"temperature": 0.0},
}


def content_relevance(
    model: str,
    examples: Optional[List[EvaluationExample]] = None,
) -> EvaluationMetric:
    """
    Content relevance judge for LLMs.

    :param model: The model name to use for the judge.
    :param examples: A list of examples to use for the judge. If not provided, the default examples will be used.
    :return: A metric for content relevance.
    """
    metric = make_genai_metric(
        name="content_relevance_to_question",
        model=model,
        examples=examples if examples is not None else _V1["default_examples"],
        definition=_V1["definition"],
        grading_prompt=_V1["grading_prompt"],
        grading_context_columns=[],
        parameters=_V1["default_parameters"],
        version="v1",
        aggregations=[],
        greater_is_better=True,
    )

    original_eval_fn = metric.eval_fn

    def wrapped_eval_fn(inputs, retrieved_content):
        """
        Wrapper that exposes the signature (inputs, retrieved_content) for the eval_fn and routes
        to the metric's eval_fn with an argument translation.

        NOTE: the name of the parameter `retrieved_content` should be kept in sync with constants.RETRIEVED_CONTENT
        """
        return original_eval_fn(
            retrieved_content,  # predictions
            {},  # metrics
            inputs,  # inputs
        )

    metric.eval_fn = wrapped_eval_fn
    return metric
