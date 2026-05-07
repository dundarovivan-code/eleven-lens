"""Eleven Lens — AI Venture Capital Intelligence Engine for Eleven Ventures."""

from .model import (
    ELEVEN_TRAITS, ProspectAssessment, TraitScore, PatternMatch, RedFlag,
    Verdict, Confidence, BenchmarkFounder,
    get_trait, get_applicable_traits, calculate_overall_confidence,
)
from .benchmarks import BENCHMARK_FOUNDERS, get_benchmark_by_name, get_archetypes
from .mock_assessments import DEMO_PROSPECTS, FORM_SAMPLE_ASSESSMENT

__version__ = "0.2.0"
