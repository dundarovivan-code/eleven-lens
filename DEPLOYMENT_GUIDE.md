# Deployment Guide for Ivan

**Goal:** Get a public URL you can send Rene that loads the Eleven Lens app.

**Time required:** ~30-45 minutes if everything goes smoothly.

**Two paths.** Pick one. Both are free.

- **Path A: GitHub + Streamlit Community Cloud** — More polished URL (`elevenlens-yourname.streamlit.app`). Requires a GitHub account.
- **Path B: Hugging Face Spaces** — No Git knowledge needed, web-only upload. URL is `huggingface.co/spaces/yourname/eleven-lens`.

I recommend **Path A** because the URL looks more "real product." But if you get stuck, **Path B is faster and bulletproof.**

---

## Path A: GitHub + Streamlit Community Cloud

### Step 1 — Create a GitHub account (5 min)

1. Go to **github.com**
2. Click **Sign up** (top right)
3. Pick a username — this becomes part of your URLs, so keep it professional. `idundarov` or `ivan-dundarov` is fine.
4. Verify email
5. Choose the **Free** plan when prompted

### Step 2 — Create a new repository (3 min)

1. Once logged in, click the **+** icon (top right) → **New repository**
2. Repository name: `eleven-lens`
3. Description: *(optional)* "AI VC Intelligence Engine prototype"
4. Choose **Public** (Streamlit Community Cloud requires public repos for free tier)
5. Check **Add a README file**
6. Click **Create repository**

### Step 3 — Upload the code (10 min)

You need to upload all files from the `eleven_lens/` folder. Two ways:

**Option 3a: Drag-and-drop (easiest, recommended)**

1. From your repo page, click **Add file** → **Upload files**
2. From your local computer, **unzip** the project package I gave you
3. Drag-and-drop **all files and folders** from the unzipped folder into the GitHub upload page:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - The `src/` folder (with all 5 files inside)
   - The `docs/` folder
4. Scroll down, add commit message: "Initial commit"
5. Click **Commit changes**

**⚠️ Important:** GitHub's web upload preserves folder structure when you drag entire folders. If something breaks, upload `src/` files into a folder you create on GitHub first — click **Add file** → **Create new file** and type `src/model.py` to create the folder.

**Option 3b: GitHub Desktop (if drag-and-drop fails)**

1. Download **GitHub Desktop** from desktop.github.com
2. Sign in
3. File → Clone repository → select `eleven-lens`
4. Copy all project files into the cloned folder on your computer
5. Back in GitHub Desktop, you'll see all the changes
6. Add commit message → **Commit to main** → **Push origin**

### Step 4 — Deploy to Streamlit Community Cloud (5 min)

1. Go to **share.streamlit.io**
2. Click **Sign in** → **Continue with GitHub**
3. Authorize Streamlit to access your GitHub
4. Click **New app**
5. Fill in:
   - **Repository:** `yourusername/eleven-lens`
   - **Branch:** `main`
   - **Main file path:** `app.py`
6. Click **Deploy**
7. Wait 2-3 minutes for the first deploy

Your URL will be something like: **`https://elevenlens-yourname.streamlit.app`**

### Step 5 — Test it (5 min)

1. Open the URL in a fresh browser tab (or incognito, to confirm it works publicly)
2. Click through every page in the sidebar — Overview, Benchmark Founders, Demo Prospect Analysis, Framework, Strategic Memo
3. On the Demo page, switch between all three prospects (Stefan Radov, Nikola Lazarov, Fictional Weak Profile)
4. Open all four tabs (Trait Matrix, Pattern Matching, Red Flags, Sources)
5. **If anything looks broken or unstyled**, take a screenshot, share with me, we fix before sending

### Step 6 — Send to Rene (5 min)

Use the email template at the bottom of this document.

---

## Path B: Hugging Face Spaces (fallback if GitHub feels like too much)

### Step 1 — Create Hugging Face account (3 min)

1. Go to **huggingface.co**
2. Click **Sign Up**
3. Pick a username — same advice, professional handle
4. Verify email

### Step 2 — Create a Space (5 min)

1. Click your profile (top right) → **New Space**
2. Space name: `eleven-lens`
3. License: **MIT** (or any, doesn't matter for this)
4. **Space SDK: Streamlit**
5. **Public** visibility
6. Click **Create Space**

### Step 3 — Upload files (10 min)

1. On your new Space page, click the **Files** tab
2. Click **Add file** → **Upload files**
3. Upload the files from the unzipped project:
   - `app.py`
   - `requirements.txt`
   - `README.md`
4. For the `src/` folder: click **Add file** → **Create new file** → type `src/model.py` → paste the content from your local `src/model.py` → commit
5. Repeat for `src/__init__.py`, `src/benchmarks.py`, `src/prompts.py`, `src/analyzer.py`, `src/mock_assessments.py`

(Yes, this is tedious. That's why I recommend Path A. But if Git is scaring you, this works.)

### Step 4 — Wait for build

Hugging Face will automatically build and deploy the Space. Watch the **Logs** tab for progress. Takes 2-5 minutes.

### Step 5 — Get your URL

Once built, your URL is `https://huggingface.co/spaces/yourusername/eleven-lens`.

Click the URL, test the same way as Path A Step 5.

---

## Common issues and fixes

**"App failed to deploy" / "ModuleNotFoundError: No module named 'src'"**  
The `src/` folder didn't upload as a folder. Re-upload making sure `src/` is preserved as a directory with `__init__.py` inside it.

**"AttributeError" or layout looks broken**  
Streamlit version mismatch. The `requirements.txt` should pin `streamlit==1.57.0`. If issues persist, try unpinning: change to just `streamlit` in `requirements.txt`.

**Page loads but is mostly blank**  
Streamlit cache issue. Add `?embed=false` to the end of the URL, or wait 2 minutes and refresh.

**Can't sign in to GitHub from Streamlit Cloud**  
Make sure you're logged into GitHub in another tab first. Streamlit Cloud uses OAuth, which requires an active GitHub session.

---

## Email template for Rene

Once the app is live and you've tested it, send Rene something like:

> Subject: Eleven Lens — working prototype following our chat
>
> Hi Rene,
>
> Following up on our conversation. You mentioned the team is looking for someone to build AI optimization processes for analyst-level work. Rather than describe what that looks like in abstract, I built a working prototype:
>
> **Eleven Lens** — [your URL here]
>
> It's a founder evaluation engine calibrated against 9 of your portfolio founders, with the framework anchored in your stated core evaluation traits. Three things to look at:
>
> 1. **Demo: Prospect Analysis** — see the tool's output on Stefan Radov, Nikola Lazarov, and a deliberately weak fictional profile to show full range
> 2. **Benchmark Founders** — the calibration set with archetype filters
> 3. **Strategic Memo** — the rollout proposal and what I'd build in the first 30 days
>
> A few things I'd value your honest feedback on:
> - Do the 5 traits match how you actually think about founder fit in IC?
> - Is the pattern-matching against the benchmark archetypes useful, or noise?
> - One founder (Mihail Stoychev) is intentionally excluded pending verification of his attribution between SMSBump and Nitropack — happy to add him once confirmed
>
> Mock-only mode for now — happy to switch to live Claude API mode if Petar wants to test it on real pipeline founders.
>
> 15 minutes of your feedback would meaningfully sharpen this. Thank you for the time.
>
> — Ivan

---

## What to do if everything breaks

DM me. I'll help you troubleshoot. **It is much better to send Rene nothing than to send her a broken URL.**

Good luck.
