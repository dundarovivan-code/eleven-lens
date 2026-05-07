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
            "capability lines, when they describe disagreements as productive
