"""
Eleven Lens — Streamlit App
============================

Entry point for the deployed web tool.

Run locally:
    streamlit run app.py

Deploy:
    Push this repo to GitHub, then connect to Streamlit Community Cloud
    (or Hugging Face Spaces). Set ANTHROPIC_API_KEY in secrets if you
    want live mode; otherwise the app runs in mock-only mode.
"""

import streamlit as st
from src import (
    BENCHMARK_FOUNDERS, DEMO_PROSPECTS, ELEVEN_TRAITS, FORM_SAMPLE_ASSESSMENT,
    get_archetypes, get_benchmark_by_name, get_trait,
)
from src.model import Verdict, Confidence, ProspectAssessment


# =============================================================================
# Page Setup
# =============================================================================

st.set_page_config(
    page_title="Eleven Lens — VC Intelligence Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Eleven brand alignment
st.markdown("""
<style>
    .main .block-container { padding-top: 2rem; max-width: 1100px; }
    h1 { color: #0c447c; font-weight: 600; }
    h2 { color: #0c447c; font-weight: 600; border-bottom: 1px solid #d0d7e0; padding-bottom: 6px; margin-top: 2rem; }
    h3 { color: #2e75b6; font-weight: 600; }
    .stMetric { background: #f4f7fb; padding: 12px; border-radius: 6px; }
    .verdict-pill {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { padding: 8px 16px; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# Sidebar
# =============================================================================

with st.sidebar:
    st.markdown("### 🔍 Eleven Lens")
    st.caption("VC Intelligence Engine — Founder Assessment Tool")
    st.markdown("---")
    
    page = st.radio(
        "Navigate",
        [
            "🏠 Overview",
            "🆕 Analyze a New Prospect",
            "🧬 Benchmark Founders",
            "📊 Demo: Prospect Analysis",
            "📐 The Framework",
            "📝 Strategic Memo",
        ],
        label_visibility="collapsed",
    )
    
    st.markdown("---")
    
    # Optional API key input for live mode
    with st.expander("🔑 Live mode (optional)"):
        st.caption(
            "By default, this tool runs in mock mode with pre-computed sample analyses. "
            "To run real-time Claude analysis on a new prospect, paste an Anthropic API key below. "
            "The key is used only for your session and is not stored."
        )
        user_api_key = st.text_input(
            "Anthropic API key",
            type="password",
            placeholder="sk-ant-...",
            help="Get a key at console.anthropic.com. Each analysis costs ~$0.30.",
        )
        if user_api_key:
            st.session_state["api_key"] = user_api_key
            st.success("Live mode active for this session")
    
    st.markdown("---")
    st.caption(
        "**v0.2 prototype**  \n"
        "Built for Rene Tomova at Eleven Ventures.  \n\n"
        "Calibrated against 9 portfolio founders."
    )
    st.markdown("---")
    st.caption("Built by Ivan Dundarov · May 2026")


# =============================================================================
# Helper Components
# =============================================================================

def render_score_bar(score: int, max_score: int = 10):
    """Render a horizontal score bar with color coding."""
    color = "#1e7e34" if score >= 8 else ("#b88600" if score >= 5 else "#a02020")
    pct = (score / max_score) * 100
    return f"""
    <div style="background:#e8e8e8; border-radius:4px; height:8px; width:140px; display:inline-block; vertical-align:middle; margin: 0 8px;">
        <div style="width:{pct}%; background:{color}; height:100%; border-radius:4px;"></div>
    </div>
    """


def render_verdict_pill(verdict: Verdict):
    """Render the verdict as a colored pill."""
    bg = {"Investment Ready": "#d4edda", "Incubation Needed": "#fff7e6", "Pass": "#fde0e0"}[verdict.value]
    return f"""
    <span class="verdict-pill" style="background:{bg}; color:{verdict.color};">
        {verdict.emoji} {verdict.value}
    </span>
    """


def render_confidence_badge(conf: Confidence):
    color = {"Low": "#a02020", "Medium": "#b88600", "High": "#1e7e34"}[conf.value]
    return f"<span style='color:{color}; font-weight:600; font-size:13px;'>{conf.value} confidence</span>"


def render_severity_badge(severity: str):
    color = {"Watch": "#b88600", "Concern": "#cc6600", "Blocker": "#a02020"}[severity]
    return f"<span style='background:{color}; color:white; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600;'>{severity}</span>"


def render_assessment_full(assessment: ProspectAssessment):
    """Render a complete ProspectAssessment with header + tabs.
    
    Used by both the Demo page and the Analyze-a-New-Prospect page.
    """
    # Header block
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"## {assessment.prospect_name}")
        st.caption(f"**{assessment.company}** · {'Multi-founder team' if assessment.is_team else 'Solo founder'}")
    with col2:
        st.markdown(render_verdict_pill(assessment.verdict), unsafe_allow_html=True)
        st.markdown(render_confidence_badge(assessment.overall_confidence), unsafe_allow_html=True)
    
    # Strategic recommendation
    st.markdown("### Strategic Recommendation")
    st.info(assessment.strategic_recommendation)
    
    # Four tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Trait Matrix",
        "🧬 Pattern Matching",
        "⚠️ Red Flags",
        "📁 Sources",
    ])
    
    with tab1:
        st.markdown("**Score on Eleven's core evaluation traits (1-10).**")
        for ts in assessment.trait_scores:
            trait = get_trait(ts.trait_key)
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"**{trait.label}**")
                    st.caption(trait.short_description)
                with col2:
                    st.markdown(
                        f"<div style='text-align:center; padding-top:8px;'>"
                        f"<span style='font-size:20px; font-weight:700; color:#0c447c;'>{ts.score}/10</span>"
                        f"{render_score_bar(ts.score)}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                with col3:
                    st.markdown(
                        f"<div style='text-align:right; padding-top:14px;'>{render_confidence_badge(ts.confidence)}</div>",
                        unsafe_allow_html=True,
                    )
                st.markdown(f"_{ts.justification}_")
                st.markdown("---")
    
    with tab2:
        st.markdown("**Closest archetype matches from the benchmark database.**")
        for pm in assessment.pattern_matches:
            try:
                benchmark = get_benchmark_by_name(pm.benchmark_founder_name)
            except KeyError:
                # Live mode might match against a name not in our DB; render gracefully
                benchmark = None
            with st.container():
                col1, col2 = st.columns([2, 1])
                with col1:
                    if benchmark:
                        st.markdown(f"### {benchmark.name}")
                        st.caption(f"**{benchmark.company}** · *{benchmark.archetype}*")
                    else:
                        st.markdown(f"### {pm.benchmark_founder_name}")
                with col2:
                    strength_color = {"Strong": "#1e7e34", "Moderate": "#b88600", "Loose": "#888888"}.get(pm.similarity_strength, "#666666")
                    st.markdown(
                        f"<div style='text-align:right; padding-top:12px;'>"
                        f"<span style='background:{strength_color}; color:white; padding:4px 12px; "
                        f"border-radius:12px; font-size:12px; font-weight:600;'>"
                        f"{pm.similarity_strength} match</span></div>",
                        unsafe_allow_html=True,
                    )
                st.markdown(f"**Why this match:** {pm.rationale}")
                if benchmark:
                    st.markdown(f"_{benchmark.notable_pattern}_")
                st.markdown("---")
    
    with tab3:
        if not assessment.red_flags:
            st.success("No red flags surfaced from the analyzed material.")
        else:
            st.markdown(f"**{len(assessment.red_flags)} concern(s) surfaced from the source material.**")
            for rf in assessment.red_flags:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{rf.category}** — {rf.description}")
                    with col2:
                        st.markdown(
                            f"<div style='text-align:right; padding-top:4px;'>{render_severity_badge(rf.severity)}</div>",
                            unsafe_allow_html=True,
                        )
                    st.markdown("---")
    
    with tab4:
        st.markdown("**Source material analyzed for this assessment.**")
        for source in assessment.sources_analyzed:
            st.markdown(f"- {source}")


# =============================================================================
# Page: Overview
# =============================================================================

def render_overview():
    st.title("🔍 Eleven Lens")
    st.markdown(
        "**A founder evaluation engine for Eleven Ventures, calibrated against the firm's "
        "stated evaluation traits and benchmarked against 9 portfolio founders.**"
    )
    
    st.markdown("""
    Eleven Lens reads source material on a prospective founder — pitch notes, LinkedIn, 
    podcasts, blog posts — and produces a structured assessment for IC preparation:
    
    - **Behavioral Trait Matrix** — Score 1-10 across Eleven's stated evaluation criteria
    - **Pattern Matching** — Closest archetype matches against the benchmark portfolio
    - **Red Flags & Blind Spots** — Specific concerns surfaced from the source material
    - **Readiness Verdict** — Investment Ready / Incubation Needed / Pass + strategic recommendation
    
    The framework anchors on Eleven's published thesis: capital efficiency, global ambition 
    from Day 1, and extraordinary founder resilience. It is built around Rene Tomova's IC 
    criterion: *"Can I help this founder?"*
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Benchmark Founders", len(BENCHMARK_FOUNDERS))
    with col2:
        st.metric("Eleven Core Traits", len(ELEVEN_TRAITS))
    with col3:
        st.metric("Demo Assessments", len(DEMO_PROSPECTS))
    
    st.markdown("---")
    
    st.markdown("### How to use this tool")
    st.markdown("""
    1. **🆕 Analyze a New Prospect** — *Start here.* Paste a founder profile in the structured 
       form and see Eleven Lens produce a full assessment. Mock-mode shows a sample output; 
       live mode (with API key) produces real-time analysis.
    2. **🧬 Browse the benchmark founders** to understand what each archetype looks like
    3. **📊 Read demo assessments** to see how Eleven Lens scores three pre-analyzed prospects
    4. **📐 Review the framework** to understand the trait rubric and the mapping to Eleven's stated criteria
    5. **📝 Read the strategic memo** for the rollout proposal and 30-day work plan
    
    *Want this tool run on a specific founder you're evaluating? Send me a name and I'll add 
    them to the next iteration. Or paste an Anthropic API key in the sidebar to run live analysis yourself.*
    """)
    
    st.info(
        "📌 **Note for Rene:** This is a v0.2 prototype calibrated against my reading of "
        "public material on 9 Eleven portfolio founders. The dimension weights and benchmark "
        "calibration are designed to be tuned against your actual portfolio data — that's "
        "the week-one work I'd do as an intern. I'd value 15 minutes of your feedback on "
        "whether the framework matches how you actually think about founder fit in IC."
    )


# =============================================================================
# Page: Benchmark Founders
# =============================================================================

def render_benchmarks():
    st.title("🧬 Benchmark Founders")
    st.markdown(
        "**The calibration set.** New prospects are pattern-matched against these archetypes. "
        "Filter by archetype to see which profile your new founder most resembles."
    )
    
    archetypes = ["All"] + get_archetypes()
    selected_archetype = st.selectbox("Filter by archetype", archetypes)
    
    filtered = (
        BENCHMARK_FOUNDERS if selected_archetype == "All"
        else [f for f in BENCHMARK_FOUNDERS if f.archetype == selected_archetype]
    )
    
    st.caption(f"Showing {len(filtered)} of {len(BENCHMARK_FOUNDERS)} founders")
    st.markdown("---")
    
    for founder in filtered:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {founder.name}")
                st.caption(f"**{founder.company}** · *{founder.archetype}*")
            with col2:
                st.markdown(
                    f"<div style='text-align:right; padding-top:12px;'>"
                    f"<span style='background:#0c447c; color:white; padding:4px 12px; "
                    f"border-radius:12px; font-size:12px;'>{founder.archetype}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            
            st.markdown(f"**Summary.** {founder.summary}")
            st.markdown(f"**Notable pattern.** {founder.notable_pattern}")
            
            st.markdown("**Key traits:**")
            for trait in founder.key_traits:
                st.markdown(f"- {trait}")
            
            st.markdown("---")


# =============================================================================
# Page: Demo Prospect Analysis
# =============================================================================

def render_prospect_demo():
    st.title("📊 Demo: Prospect Analysis")
    st.markdown(
        "**See Eleven Lens in action on three example prospects.** Each shows the full "
        "structured output: trait scoring, pattern matching, red flags, and verdict."
    )
    
    st.warning(
        "🔒 **Mock-only mode (default deployment).** These assessments were pre-computed "
        "offline based on careful reading of the prospects' public material. To run "
        "**live AI analysis** on a new prospect, see the **🆕 Analyze a New Prospect** "
        "page in the sidebar — paste source material and the tool will generate a "
        "structured assessment."
    )
    
    prospect_keys = list(DEMO_PROSPECTS.keys())
    prospect_labels = {
        "stefan_radov_nfuse": "🟢 Stefan Radov & Stoyan Ivanov (nFuse) — Multi-founder team",
        "nikola_lazarov_eilla": "🟢 Nikola Lazarov (Eilla AI) — Solo founder",
        "fictional_weak_example": "🔴 Demo Weak Profile — Shows what failure looks like",
    }
    
    selected_key = st.selectbox(
        "Select a prospect",
        prospect_keys,
        format_func=lambda k: prospect_labels.get(k, k),
    )
    
    assessment = DEMO_PROSPECTS[selected_key]
    
    st.markdown("---")
    render_assessment_full(assessment)


# =============================================================================
# Page: Analyze a New Prospect (the killer feature)
# =============================================================================

def render_analyze_new_prospect():
    st.title("🆕 Analyze a New Prospect")
    st.markdown(
        "**Paste a founder profile below and Eleven Lens will produce a structured "
        "assessment** — trait matrix, pattern matching, red flags, and a readiness verdict."
    )
    
    api_key = st.session_state.get("api_key")
    
    if api_key:
        st.success(
            "🟢 **Live mode active.** Submitting the form will run real-time Claude "
            "analysis on the input you provide. Each analysis costs approximately $0.30."
        )
    else:
        st.info(
            "🔒 **Mock-only mode (default).** Submitting the form will display a "
            "**pre-computed sample assessment** based on a real example founder profile. "
            "This shows what live mode produces without consuming API credits. "
            "To enable live mode, paste an Anthropic API key in the sidebar (🔑 Live mode)."
        )
    
    st.markdown("---")
    
    # Input form using Ivan's exact template structure
    with st.form("prospect_form"):
        st.markdown("### Founder Profile Input")
        
        founder_names = st.text_input(
            "Founder Name(s)",
            value="Maria Ivanova & Petar Georgiev" if not api_key else "",
            help="e.g., Maria Ivanova & Petar Georgiev",
        )
        
        is_team = st.checkbox(
            "This is a multi-founder team",
            value=True,
            help="Enables scoring on Complementary Team Dynamics trait",
        )
        
        startup_idea = st.text_input(
            "Startup Idea",
            value="AI-driven supply chain forecasting for mid-market logistics" if not api_key else "",
            help="e.g., AI-driven supply chain forecasting for mid-market logistics",
        )
        
        background = st.text_area(
            "Background",
            value=(
                "Maria spent 10 years at DHL in logistics management. "
                "Petar is a self-taught machine learning engineer whose last startup failed."
                if not api_key else ""
            ),
            height=100,
            help="Founder backgrounds, previous experience, domain depth",
        )
        
        pitch_notes = st.text_area(
            "Pitch / Conversation Notes",
            value=(
                "The pitch was highly technical. Maria dominated the conversation, but Petar "
                "stepped in perfectly when asked about the data pipeline. When Rene asked about "
                "their high customer acquisition cost, Maria admitted they are struggling with "
                "it and don't have a good solution yet. They built the current MVP using just "
                "$5,000 of their own savings."
                if not api_key else ""
            ),
            height=180,
            help="Behavioral observations, specific quotes, pitch dynamics, financial details",
        )
        
        submitted = st.form_submit_button("🔍 Analyze Prospect", type="primary")
    
    if submitted:
        if not founder_names or not startup_idea or not background or not pitch_notes:
            st.error("Please fill in all four fields before submitting.")
            return
        
        st.markdown("---")
        st.markdown("## Analysis Result")
        
        if api_key:
            # Live mode: actual Claude API call
            with st.spinner("Running Eleven Lens analysis (~30 seconds)..."):
                try:
                    from src.analyzer import run_live_analysis
                    
                    source_content = (
                        f"STARTUP IDEA: {startup_idea}\n\n"
                        f"BACKGROUND: {background}\n\n"
                        f"PITCH / CONVERSATION NOTES: {pitch_notes}"
                    )
                    
                    sources_analyzed = [
                        f"Form input: founder background ({len(background)} chars)",
                        f"Form input: pitch and conversation notes ({len(pitch_notes)} chars)",
                        f"Form input: startup idea description",
                    ]
                    
                    assessment = run_live_analysis(
                        prospect_name=founder_names,
                        company=startup_idea[:60] + "..." if len(startup_idea) > 60 else startup_idea,
                        is_team=is_team,
                        source_content=source_content,
                        sources_analyzed=sources_analyzed,
                        api_key=api_key,
                    )
                    
                    render_assessment_full(assessment)
                    
                except Exception as e:
                    st.error(f"**Live analysis failed:** {str(e)}")
                    st.caption(
                        "If this is an authentication error, check your API key. "
                        "If the model returned malformed JSON, try resubmitting once. "
                        "Otherwise, contact Ivan."
                    )
        else:
            # Mock mode: show the pre-computed sample
            st.success(
                "📋 **Sample assessment generated.** This is a pre-computed analysis based "
                "on the example input shown above. In live mode, the same form would produce "
                "a real-time analysis based on whatever input you provide."
            )
            render_assessment_full(FORM_SAMPLE_ASSESSMENT)


# =============================================================================
# Page: The Framework
# =============================================================================

def render_framework():
    st.title("📐 The Framework")
    st.markdown(
        "**Eleven Lens scores prospects on five core evaluation traits, mapped directly "
        "to Eleven's stated investment thesis.**"
    )
    
    st.markdown("---")
    
    st.markdown("### Mapping: Eleven's Stated Traits → Eleven Lens Scoring")
    st.markdown("""
    | Eleven's Stated Trait | Eleven Lens Implementation |
    |---|---|
    | Problem Obsession | Direct mapping (`problem_obsession`) |
    | Radical Honesty / Transparency | Direct mapping (`radical_honesty`) |
    | Resilience & Humility | Direct mapping (`resilience_humility`) |
    | Capital Efficiency | Direct mapping (`capital_efficiency`) |
    | Complementary Team Dynamics | `complementary_team` (multi-founder teams only) |
    """)
    
    st.markdown("---")
    
    st.markdown("### Trait Definitions")
    
    for trait in ELEVEN_TRAITS:
        with st.expander(f"**{trait.label}** {'(team-only)' if trait.team_only else ''}"):
            st.markdown(f"**Short:** {trait.short_description}")
            st.markdown(f"**Detail:** {trait.long_description}")
    
    st.markdown("---")
    
    st.markdown("### The Verdict Spec")
    st.markdown("""
    Each prospect is given one of three readiness states:
    
    - **🟢 Investment Ready** — Strong scores on at least 4 of 5 traits, no Blocker red flags, 
      clear pattern match to a Strong benchmark archetype.
    
    - **🟡 Incubation Needed** — Strong raw traits (especially Resilience & Humility), but 
      the idea, GTM, or capital plan needs heavy Eleven mentorship to succeed. The platform 
      can compound value here.
    
    - **🔴 Pass** — Fatal flaws in team dynamics, lack of honesty, low resilience, or 
      fundamental thesis mismatch. Platform support cannot compensate.
    """)


# =============================================================================
# Page: Strategic Memo
# =============================================================================

def render_memo():
    st.title("📝 Strategic Memo")
    st.markdown(
        "**Why this exists, how it scales, and what I'd build in the first 30 days.**"
    )
    
    st.markdown("---")
    
    st.markdown("""
    ### What this is
    
    A working prototype of a founder evaluation engine, calibrated against Eleven's stated 
    evaluation traits and pattern-matched against 9 Eleven portfolio founders. Designed to 
    accelerate analyst-level DD work and provide structured, defensible inputs to IC.
    
    Built specifically because Rene mentioned the team is looking for someone to build AI 
    optimization processes that help analysts work better. Rather than describe what that 
    looks like in abstract, this is the concrete v0.
    
    ### Why this fits Eleven specifically
    
    Most VC DD frameworks evaluate founders on universal traits. Eleven's competitive moat 
    is its platform — the operational support that compounds value after the check is written. 
    The 8x follow-on multiple does not happen because every founder is great. It happens because 
    Rene's platform team can compound value with founders who are coachable, strategically 
    flexible, and self-aware enough to absorb help.
    
    Eleven Lens is built around that distinction. The five traits and the pattern matching are 
    designed to predict not just "will this founder succeed" but "will Eleven's platform model 
    work on them."
    
    ### How it changes the analyst workflow
    
    **Today (rough sketch of existing process):**
    1. Analyst reads founder pitch deck, LinkedIn, podcasts
    2. Analyst forms qualitative impression
    3. Analyst writes founder section of IC memo (~3-4 hours)
    4. Quality varies by analyst experience and energy on that day
    
    **With Eleven Lens integrated:**
    1. Analyst pastes available founder material into the tool
    2. Tool runs in seconds, produces structured assessment
    3. Analyst spends time *verifying and challenging* the AI's assessment, not generating it
    4. IC memo founder section now grounded in standardized rubric — defensible across analysts
    
    The unlock is consistency across analysts and across time. A junior analyst's founder 
    assessment is now anchored to the same rubric as a partner's.
    
    ### Three-step rollout proposal
    
    **Step 1 — Pilot (weeks 1-2):**  
    Run the tool on the next 5 prospective deals in parallel with the existing process. 
    Compare tool output to analyst impression. Calibrate trait weights based on which scores 
    most predicted partner gut feel.
    
    **Step 2 — Integrate (weeks 3-6):**  
    Add tool output as a standard section of the IC memo template. Train analysts on input 
    quality. Build a small library of completed assessments for benchmarking.
    
    **Step 3 — Compound (months 2-6):**  
    Track follow-on outcomes against initial scores over 6 months of investments. Use the 
    data to recalibrate trait weights based on what actually predicted Eleven-specific 
    success. This is the part that makes the tool *Eleven's*, not generic.
    
    ### What this prototype does NOT yet do
    
    - **Source ingestion is manual.** Analyst pastes material in. Auto-scraping LinkedIn 
      violates ToS and quality of input matters more than convenience.
    - **No portfolio benchmarking yet.** The framework scores in isolation. With Eleven's 
      historical data, it could compare new deals against successful and unsuccessful past 
      portfolio founders.
    - **English only.** Bulgarian, Greek, Polish founder materials would need translation 
      pre-processing.
    - **One founder skipped pending verification** — Mihail Stoychev attribution between 
      SMSBump and Nitropack needs to be confirmed before inclusion.
    
    ### What I would build in the first 30 days as an intern
    
    **Week 1:** Run Eleven Lens on 10-15 founders from Eleven's recent investment cohort. 
    Validate scoring against partner gut feel. Tune trait weights.
    
    **Week 2:** Build an AEO Audit module as a parallel framework, extending the AI Visibility 
    Playbook into DD. Generate sample audits on 5 portfolio companies.
    
    **Week 3:** Integrate Eleven Lens into the IC memo template. Document the analyst workflow. 
    Train on first new deal.
    
    **Week 4:** Build an AI-Native Unit Economics module. Apply to current pipeline. Pre-flag 
    deals that clear the Tomov benchmark before partner review.
    
    End of month one: three modules in production, a quantitative founder benchmark, and a 
    workflow that compounds on itself.
    
    ### Why I built this before being hired
    
    Two reasons. First, when Rene said the team needs someone who builds AI optimization 
    processes, I wanted to show what that looks like in concrete form rather than describe 
    it in abstract. Second, this is the kind of work I want to do — encoding how thoughtful 
    investors actually evaluate founders into structured tooling that scales their judgment 
    across deals.
    
    If we work together, more of this. If we don't, you have a working prototype to use or 
    hand to whoever takes the role.
    
    Either way, I would value 15 minutes of your feedback on whether the framework matches 
    how you actually think about founder fit in IC. That is the part I cannot calibrate from 
    outside Eleven.
    
    — Ivan
    """)


# =============================================================================
# Router
# =============================================================================

if page == "🏠 Overview":
    render_overview()
elif page == "🆕 Analyze a New Prospect":
    render_analyze_new_prospect()
elif page == "🧬 Benchmark Founders":
    render_benchmarks()
elif page == "📊 Demo: Prospect Analysis":
    render_prospect_demo()
elif page == "📐 The Framework":
    render_framework()
elif page == "📝 Strategic Memo":
    render_memo()
