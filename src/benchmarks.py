
Eleven Benchmark Founders — calibration database.

Source: Ivan Dundarov's curated dataset of 9 Eleven portfolio founders,
mapped to archetype labels and key trait patterns.

Note: Mihail Stoychev (SMSBump) intentionally excluded pending verification
of his attribution against Eleven's published portfolio materials.
"""

from .model import BenchmarkFounder


BENCHMARK_FOUNDERS = [
    BenchmarkFounder(
        name="Hristo Borisov",
        company="Payhawk",
        archetype="Scale-Up Visionary",
        key_traits=[
            "Massive global ambition",
            "Radical honesty with downstream investors",
            "Strong complementary partnership",
        ],
        summary=(
            "Co-founder & CEO of Payhawk. Scaled from Eleven's seed check to a "
            "$1B+ unicorn outcome. The reference profile for high-ambition CEE "
            "operator-founders who can carry a category from local to global."
        ),
        notable_pattern=(
            "Combines aggressive scale ambition with operator-grade execution. "
            "Hires senior international executives — pattern of bringing in "
            "capability above own level."
        ),
    ),

    BenchmarkFounder(
        name="Boyko Karadzhov",
        company="Payhawk",
        archetype="Technical Architect",
        key_traits=[
            "Deeply technical",
            "Capital efficient infrastructure builder",
            "Low ego",
        ],
        summary=(
            "Co-founder & CTO of Payhawk. The technical anchor behind the "
            "company's product depth and reliability at scale. Operates "
            "from a strong engineering identity rather than a public persona."
        ),
        notable_pattern=(
            "Builds infrastructure that compounds over years, not features that "
            "spike. Low ego means decisions follow product logic rather than "
            "founder preference."
        ),
    ),

    BenchmarkFounder(
        name="Georgi Petrov",
        company="SMSBump",
        archetype="Capital-Efficient Builder",
        key_traits=[
            "Built robust tech on lean budget",
            "Perfect alignment with GTM partner",
        ],
        summary=(
            "Co-founder of SMSBump (acquired by Yotpo). Built the technical "
            "foundation that allowed SMSBump's GTM motion to scale without "
            "blowing the burn rate. The textbook capital-efficient CEE engineer."
        ),
        notable_pattern=(
            "Engineering choices made under capital constraint produce more "
            "durable systems than well-funded equivalents. The opposite of "
            "'we'll fix it when we raise more.'"
        ),
    ),

    BenchmarkFounder(
        name="Svilen Rangelov",
        company="Dronamics",
        archetype="Regulatory Navigator",
        key_traits=[
            "Extreme patience and resilience",
            "Ability to navigate massive bureaucratic hurdles",
        ],
        summary=(
            "Co-founder & CEO of Dronamics, autonomous cargo drone airline. "
            "Has carried the company through a multi-year pre-revenue cycle "
            "across multiple regulatory regimes. The benchmark for resilience "
            "in deeptech contexts where the bureaucratic moat is the moat."
        ),
        notable_pattern=(
            "Resilience expressed as endurance across slow cycles, not heroics "
            "in fast ones. Comfortable with multi-year ambiguity."
        ),
    ),

    BenchmarkFounder(
        name="Konstantin Rangelov",
        company="Dronamics",
        archetype="Deep-Tech Specialist",
        key_traits=[
            "Subject matter obsession",
            "Hardware engineering brilliance",
        ],
        summary=(
            "Co-founder & CTO of Dronamics. Carries the technical ownership "
            "of the autonomous cargo drone platform. Pairs with brother Svilen "
            "in a clean technical/business division of labor."
        ),
        notable_pattern=(
            "Problem obsession at extreme — has spent years inside hardware "
            "and autonomy fundamentals. The depth of focus is itself the moat."
        ),
    ),

    BenchmarkFounder(
        name="Dimitar Karaivanov",
        company="Kanbanize",
        archetype="Enterprise Pragmatist",
        key_traits=[
            "Highly methodical",
            "Process-driven",
            "Obsessed with sustainable unit economics",
        ],
        summary=(
            "Founder & CEO of Kanbanize, enterprise-focused work management "
            "platform. Built sustainable unit economics on enterprise B2B "
            "sales without chasing hypergrowth. Operates at the methodical, "
            "process-driven end of the founder spectrum."
        ),
        notable_pattern=(
            "Capital efficiency expressed as methodical sales discipline rather "
            "than scrappy improvisation. Predictable enterprise GTM motion."
        ),
    ),

    BenchmarkFounder(
        name="Ivan Osmak",
        company="Quantive (formerly Gtmhub)",
        archetype="Global Expander",
        key_traits=[
            "Fearless in entering the US market",
            "Strong enterprise sales DNA",
        ],
        summary=(
            "Co-founder & CEO of Quantive, OKR/strategy execution platform. "
            "Made the early bet to compete in the US enterprise market and "
            "raised a $120M Series C against US-headquartered peers. The "
            "benchmark for CEE founders willing to plant flag in San Francisco."
        ),
        notable_pattern=(
            "Global ambition treated as an early decision, not a later milestone. "
            "Comfortable selling to US enterprises against incumbent vendors."
        ),
    ),

    BenchmarkFounder(
        name="Volen Vulkov",
        company="Enhancv",
        archetype="Design Purist",
        key_traits=[
            "Product-led growth (PLG) focus",
            "Obsessive attention to user experience",
        ],
        summary=(
            "Co-founder of Enhancv, online resume builder. Built a PLG "
            "consumer-facing product where the design quality and user flow "
            "are the primary acquisition mechanism."
        ),
        notable_pattern=(
            "Problem obsession expressed as relentless UX iteration. The "
            "product is the marketing channel."
        ),
    ),

    BenchmarkFounder(
        name="Alexander Tsvetkov",
        company="Boleron",
        archetype="Industry Veteran",
        key_traits=[
            "Deep legacy industry knowledge",
            "Leveraged past corporate experience to disrupt",
        ],
        summary=(
            "Founder of Boleron, insurance-tech platform. Used deep insurance "
            "industry experience to identify and disrupt structural inefficiencies "
            "that outsiders would miss. The benchmark for the operator-turned-"
            "founder profile in a regulated vertical."
        ),
        notable_pattern=(
            "Domain credibility from the inside lets him solve problems "
            "outsiders cannot see. Insurance is the case where industry "
            "tenure is more valuable than youthful disruption."
        ),
    ),
]


def get_benchmark_by_name(name: str) -> BenchmarkFounder:
    for f in BENCHMARK_FOUNDERS:
        if f.name == name:
            return f
    raise KeyError(f"Unknown benchmark founder: {name}")


def get_archetypes() -> list:
    """Return all unique archetypes for filtering."""
    return sorted(set(f.archetype for f in BENCHMARK_FOUNDERS))
