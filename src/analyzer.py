"""
Eleven Lens — Analysis orchestration.

Supports two modes:
- Live (with API key): runs the system prompt + analysis prompt through Claude API
- Mock (no API key): returns pre-computed assessments for demo prospects
"""

import json
import os
from typing import Optional

from .model import (
    ProspectAssessment, TraitScore, PatternMatch, RedFlag, VerificationQuestion,
    Verdict, Confidence, calculate_overall_confidence,
)
from .prompts import build_eleven_lens_system_prompt, build_prospect_analysis_prompt


CLAUDE_MODEL = "claude-opus-4-7"
MAX_TOKENS = 3000


def _parse_json_response(raw: str) -> dict:
    """Robust JSON parser handling common LLM quirks."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().strip("`").strip()
    return json.loads(raw)


def run_live_analysis(
    prospect_name: str,
    company: str,
    is_team: bool,
    source_content: str,
    sources_analyzed: list,
    api_key: Optional[str] = None,
) -> ProspectAssessment:
    """Run the Eleven Lens analysis against Claude API."""
    from anthropic import Anthropic
    
    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "No Anthropic API key. Set ANTHROPIC_API_KEY or pass api_key parameter."
        )
    
    client = Anthropic(api_key=api_key)
    system = build_eleven_lens_system_prompt()
    user = build_prospect_analysis_prompt(prospect_name, company, is_team, source_content)
    
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    raw = response.content[0].text
    data = _parse_json_response(raw)
    
    return _build_assessment_from_json(
        prospect_name, company, is_team, data, sources_analyzed
    )


def _build_assessment_from_json(
    prospect_name: str,
    company: str,
    is_team: bool,
    data: dict,
    sources_analyzed: list,
) -> ProspectAssessment:
    """Convert Claude's JSON output into a ProspectAssessment object."""
    trait_scores = [
        TraitScore(
            trait_key=ts["trait_key"],
            score=int(ts["score"]),
            justification=ts["justification"],
            confidence=Confidence(ts.get("confidence", "Medium")),
        )
        for ts in data["trait_scores"]
    ]
    
    pattern_matches = [
        PatternMatch(
            benchmark_founder_name=pm["benchmark_founder_name"],
            similarity_strength=pm["similarity_strength"],
            rationale=pm["rationale"],
        )
        for pm in data["pattern_matches"]
    ]
    
    red_flags = [
        RedFlag(
            category=rf["category"],
            description=rf["description"],
            severity=rf["severity"],
        )
        for rf in data.get("red_flags", [])
    ]
    
    verification_questions = [
        VerificationQuestion(
            target_trait=vq["target_trait"],
            question=vq["question"],
            what_to_listen_for=vq["what_to_listen_for"],
        )
        for vq in data.get("verification_questions", [])
    ]
    
    verdict = Verdict(data["verdict"])
    
    return ProspectAssessment(
        prospect_name=prospect_name,
        company=company,
        is_team=is_team,
        trait_scores=trait_scores,
        pattern_matches=pattern_matches,
        red_flags=red_flags,
        verdict=verdict,
        strategic_recommendation=data["strategic_recommendation"],
        sources_analyzed=sources_analyzed,
        overall_confidence=calculate_overall_confidence(trait_scores),
        verification_questions=verification_questions,
    )
