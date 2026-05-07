# 🔍 Eleven Lens

**An AI Venture Capital Intelligence Engine for Eleven Ventures.**

A founder evaluation tool that scores prospective founders against Eleven's stated 
core evaluation traits and pattern-matches them against a benchmark database of 9 
Eleven portfolio founders.

Built by Ivan Dundarov, May 2026.

---

## What it does

Reads source material on a prospective founder (pitch notes, LinkedIn, podcasts) and 
produces:

1. **Behavioral Trait Matrix** — Score 1-10 across Eleven's 5 core evaluation traits
2. **Pattern Matching** — Closest archetype matches against 9 benchmark portfolio founders
3. **Red Flags & Blind Spots** — Specific concerns surfaced from source material  
4. **Readiness Verdict** — 🟢 Investment Ready / 🟡 Incubation Needed / 🔴 Pass

**The killer feature: 🆕 Analyze a New Prospect.** Paste a founder profile in the structured 
form (founder names, startup idea, background, pitch notes) and Eleven Lens produces a 
full assessment. Mock mode shows a pre-computed sample. Live mode (with API key) generates 
real-time analysis from any input.

---

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## Modes

**Mock-only mode (default):** Pre-computed assessments for 3 demo prospects. No API key 
needed, no costs, always works.

**Live mode (optional):** Set `ANTHROPIC_API_KEY` environment variable. The tool will 
generate real-time assessments using Claude API. Roughly $0.30-0.50 per assessment.

---

## Deploy to Streamlit Community Cloud (free)

1. Push this repo to GitHub (public or private)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub, select this repo
4. Main file path: `app.py`
5. Deploy

For live mode: in Streamlit Cloud → app settings → Secrets, add:
```
ANTHROPIC_API_KEY = "sk-ant-..."
```

---

## Deploy to Hugging Face Spaces (alternative, no Git required)

1. Create account at [huggingface.co](https://huggingface.co)
2. Create new Space → SDK: Streamlit
3. Upload all files via the web UI
4. App goes live at `huggingface.co/spaces/yourname/eleven-lens`

---

## Project structure

```
eleven_lens/
├── app.py                          ← Streamlit app entry point
├── requirements.txt                ← Python dependencies
├── README.md                       ← This file
├── src/
│   ├── model.py                    ← Core data classes & enums
│   ├── benchmarks.py               ← The 9 benchmark founder records
│   ├── prompts.py                  ← Eleven Lens system prompt + analysis prompt
│   ├── analyzer.py                 ← Claude API integration
│   └── mock_assessments.py         ← Pre-computed demo prospect assessments
└── docs/
    └── STRATEGIC_MEMO.md           ← Strategic context (also in app)
```

---

## Notes on the benchmark set

The 9 benchmark founders span 9 archetypes:
- Scale-Up Visionary, Technical Architect, Capital-Efficient Builder
- Regulatory Navigator, Deep-Tech Specialist, Enterprise Pragmatist
- Global Expander, Design Purist, Industry Veteran

**One founder excluded pending verification:** Mihail Stoychev. Source materials 
attribute him to both Nitropack and SMSBump in different places. Excluded from this 
v0.2 until that attribution is verified.

---

## Questions or feedback

Ivan Dundarov  
[your email]  
[your LinkedIn]

The framework dimensions and weights are deliberate v0 choices. They are designed to 
be tuned against Eleven's actual portfolio outcomes — that's the week-one work I'd do 
as an intern.
