# Eleven Lens — Strategic Memo

## What this is

A working prototype of a founder evaluation engine, calibrated against Eleven's stated evaluation traits and pattern-matched against 9 Eleven portfolio founders. Designed to accelerate analyst-level DD work and provide structured, defensible inputs to IC.

## Why this fits Eleven specifically

Most VC DD frameworks evaluate founders on universal traits. Eleven's competitive moat is its platform — the operational support that compounds value after the check is written. The 8x follow-on multiple does not happen because every founder is great. It happens because the platform team compounds value with founders who are coachable, strategically flexible, and self-aware enough to absorb help.

Eleven Lens is built around that distinction. The five traits and the pattern matching are designed to predict not just "will this founder succeed" but "will Eleven's platform model work on them."

## How it changes the analyst workflow

Today (rough sketch of existing process):
- Analyst reads founder pitch deck, LinkedIn, podcasts
- Analyst forms qualitative impression
- Analyst writes founder section of IC memo (~3-4 hours)
- Quality varies by analyst experience and energy on that day

With Eleven Lens integrated:
- Analyst pastes available founder material into the tool
- Tool runs in seconds, produces structured assessment
- Analyst spends time verifying and challenging the AI's assessment, not generating it
- IC memo founder section now grounded in standardized rubric — defensible across analysts

The unlock is consistency across analysts and across time. A junior analyst's founder assessment is now anchored to the same rubric as a partner's.

## Three-step rollout

**Step 1 — Pilot (weeks 1-2):**
Run the tool on the next 5 prospective deals in parallel with the existing process. Compare tool output to analyst impression. Calibrate trait weights based on which scores most predicted partner gut feel.

**Step 2 — Integrate (weeks 3-6):**
Add tool output as a standard section of the IC memo template. Train analysts on input quality. Build a small library of completed assessments for benchmarking.

**Step 3 — Compound (months 2-6):**
Track follow-on outcomes against initial scores over 6 months of investments. Use the data to recalibrate trait weights based on what actually predicted Eleven-specific success. This is the part that makes the tool Eleven's, not generic.

## What this prototype does NOT yet do

- Source ingestion is manual. Material has to be pasted in. Auto-scraping LinkedIn violates ToS, and quality of input matters more than convenience.
- No portfolio benchmarking against historical outcomes yet. The framework scores in isolation. With Eleven's historical data, it could compare new deals against successful and unsuccessful past portfolio founders.
- English only. Bulgarian, Greek, Polish founder materials would need translation pre-processing.
- One founder skipped pending verification — Mihail Stoychev attribution between SMSBump and Nitropack needs to be confirmed before inclusion.

## Calibration assumptions

The current trait weights and benchmark scoring are based on public material — investment announcements, LinkedIn posts, press coverage. Calibration against Eleven's actual portfolio data would meaningfully improve precision. The framework is built to be tuned, not to be final.

— Ivan Dundarov
