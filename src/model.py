"""
Eleven Lens — Core Data Model
==============================

A founder evaluation engine for Eleven Ventures, anchored in their stated
core evaluation traits and benchmarked against a curated set of portfolio
founders.

Architecture matches the Eleven Lens system prompt specification:
- 5-trait Behavioral Matrix (4 behavioral + 1 capital efficiency)
- Pattern Matching against benchmark founders
- Red Flags & Blind Spots
- Verification Questions for next meeting
- 3-state Readiness Verdict (Investment Ready / Incubation Needed / Pass)

Author: Ivan Dundarov
Version: 0.4 (Eleven Lens spec)
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


# =============================================================================
# Enums
# =============================================================================

class Verdict(str, Enum):
    INVESTMENT_READY = "Investment Ready"
    INCUBATION_NEEDED = "Incubation Needed"
    PASS = "Pass"

    @property
    def emoji(self) -> str:
        return {
            Verdict.INVESTMENT_READY: "🟢",
            Verdict.INCUBATION_NEEDED: "🟡",
            Verdict.PASS: "🔴",
        }[self]

    @property
    def color(self) -> str:
        return {
            Verdict.INVESTMENT_READY: "#1e7e34",
            Verdict.INCUBATION_NEEDED: "#b88600",
            Verdict.PASS: "#a02020",
        }[self]


class Confidence(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# =============================================================================
# The Five Eleven Traits
# =============================================================================

@dataclass(frozen=True)
class ElevenTrait:
    key: str
    label: str
    short_description: str
    long_description: str
    team_only: bool = False  # True for traits that only apply to multi-founder teams


ELEVEN_TRAITS: List[ElevenTrait] = [
    ElevenTrait(
        key="problem_obsession",
        label="Problem Obsession",
        short_description=(
            "Deeply in love with solving the problem, not attached to first solution."
        ),
        long_description=(
            "Founders score high here when they obsess over the problem space "
            "rather than their initial product hypothesis. They can articulate "
            "the customer pain in granular detail, they have spent time inside "
            "the problem before building, and they treat their own solution as "
            "version one of many. Low scores indicate solution-first founders "
            "who are romanced by their idea rather than the customer reality."
        ),
    ),
    ElevenTrait(
        key="radical_honesty",
        label="Radical Honesty / Transparency",
        short_description=(
            "Does not sugarcoat bad metrics; transparent about weaknesses."
        ),
        long_description=(
            "Founders score high when they openly disclose unfavorable metrics, "
            "name their gaps without prompting, and present numbers in good "
            "months and bad with the same confidence. Low scores indicate "
            "founders who reveal data selectively, dodge specific numerical "
            "questions, or frame weaknesses as features."
        ),
    ),
    ElevenTrait(
        key="resilience_humility",
        label="Resilience & Humility",
        short_description=(
            "Past failures are an asset if learned from. Open to feedback "
            "without becoming defensive."
        ),
        long_description=(
            "Founders score high when they describe past failures with "
            "specificity and clear lessons drawn, when they receive critical "
            "feedback without becoming defensive, and when their narrative "
            "centers on the work rather than their own credentials. Low scores "
            "indicate founders who avoid discussing failure, push back "
            "reflexively on hard questions, or speak of their journey in "
            "overly heroic terms."
        ),
    ),
    ElevenTrait(
        key="capital_efficiency",
        label="Capital Efficiency",
        short_description=(
            "Ability to achieve significant milestones on a lean budget."
        ),
        long_description=(
            "Founders score high when they articulate specific milestones "
            "achievable on the proposed round, when their burn plan is grounded "
            "rather than aspirational, when they have history of doing more "
            "with less, and when they understand the AI-native unit economics "
            "shift (7-8x revenue per FTE potential). Low scores indicate "
            "founders who plan around hiring sprees, treat capital as the "
            "primary unlock, or do not benchmark against AI-native peers."
        ),
    ),
    ElevenTrait(
        key="complementary_team",
        label="Complementary Team Dynamics",
        short_description=(
            "Clear Hustler / Hacker divide. High mutual respect; "
            "practices 'disagree and commit'."
        ),
        long_description=(
            "Applies only to multi-founder teams. Founders score high when "
            "responsibilities are clearly divided along complementary "
            "capability lines, when they describe disagreements as productive "
            "rather than personal, when each co-founder credits the other "
            "publicly, and when there is visible mutual respect. Low scores "
            "indicate teams with overlapping responsibilities, single-voice "
            "communication, or signs of unresolved tension."
        ),
        team_only=True,
    ),
]


def get_trait(key: str) -> ElevenTrait:
    for t in ELEVEN_TRAITS:
        if t.key == key:
            return t
    raise KeyError(f"Unknown trait: {key}")


# =============================================================================
# Benchmark Founders
# =============================================================================

@dataclass
class BenchmarkFounder:
    """A calibration founder from the Eleven portfolio."""
    name: str
    company: str
    archetype: str
    key_traits: List[str]
    summary: str  # 2-3 sentence narrative for pattern matching
    notable_pattern: str  # The single behavioral signature this founder represents


# =============================================================================
# Prospect Assessment
# =============================================================================

@dataclass
class TraitScore:
    trait_key: str
    score: int  # 1-10
    justification: str  # Single sentence per spec
    confidence: Confidence = Confidence.MEDIUM


@dataclass
class PatternMatch:
    benchmark_founder_name: str
    similarity_strength: str  # Strong / Moderate / Loose
    rationale: str  # Why this match


@dataclass
class RedFlag:
    category: str  # "Behavioral" or "Business"
    description: str
    severity: str  # "Watch" / "Concern" / "Blocker"


@dataclass
class VerificationQuestion:
    """A specific question to ask in the next meeting to validate or invalidate
    the highest-uncertainty signals in the assessment."""
    target_trait: str  # Which trait this question is probing
    question: str  # The actual question to ask the founder
    what_to_listen_for: str  # What a strong vs weak answer looks like


@dataclass
class ProspectAssessment:
    """Full Eleven Lens output on a prospective founder/team."""
    prospect_name: str  # e.g., "Stefan Radov" or "Stefan Radov & Stoyan Ivanov"
    company: str
    is_team: bool  # If True, scoring includes complementary_team trait
    trait_scores: List[TraitScore]
    pattern_matches: List[PatternMatch]
    red_flags: List[RedFlag]
    verdict: Verdict
    strategic_recommendation: str  # 2-3 sentences for IC
    sources_analyzed: List[str]
    overall_confidence: Confidence
    verification_questions: List[VerificationQuestion] = field(default_factory=list)


# =============================================================================
# Helpers
# =============================================================================

def get_applicable_traits(is_team: bool) -> List[ElevenTrait]:
    """Return the traits that apply for solo vs team founders."""
    if is_team:
        return ELEVEN_TRAITS
    return [t for t in ELEVEN_TRAITS if not t.team_only]


def calculate_overall_confidence(scores: List[TraitScore]) -> Confidence:
    """Aggregate confidence across traits."""
    rank = {Confidence.LOW: 1, Confidence.MEDIUM: 2, Confidence.HIGH: 3}
    avg = sum(rank[s.confidence] for s in scores) / len(scores)
    if avg < 1.7:
        return Confidence.LOW
    if avg < 2.4:
        return Confidence.MEDIUM
    return Confidence.HIGH
