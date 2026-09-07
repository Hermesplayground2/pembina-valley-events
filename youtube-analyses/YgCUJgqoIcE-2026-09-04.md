# YouTube Video Analysis

## Metadata
- Title: A Self-Written Skill Beats 95% of Skills You Can Download
- Channel: ?
- Duration: ~15:50
- Date: 2026-09-04
- URL: https://youtu.be/YgCUJgqoIcE
- Video ID: YgCUJgqoIcE

## Transcript Summary
- Core claim: A 20-minute self-written skill outperforms most downloaded skills.
- Tested 55 popular skills; 27 have no trigger/description, load on every message, cost tokens, give nothing back.
- Five-step skill-building process:
  1. Pick the job: use things you have asked for repeatedly; ask agent what should be a skill.
  2. Capture corrections from real runs: “Go back through the last three times we did this, insert your skill, write down every single thing I corrected you on.”
  3. Write the description as a trigger: say what it does AND when to use it; 49% of top skills miss this.
  4. Separate steps from references: steps = procedure; references = material needed only sometimes; move optional material to references folder.
  5. Prefer scripts over instructions for exact steps: anything with numbers/arithmetic/fixed logic must be a script; models improvise through instructions.
- Size rule: body under ~500 lines / ~5,000 tokens; median skill audited was 1,665 tokens; worst offender was 19,000 tokens.
- Deletion test: remove a paragraph, rerun; if output unchanged, that paragraph was dead weight.
- Safety rule: mark skills that send messages/deploy/spend money as user-only invocable.
- Security warning: one popular memory skill had a name-squatting package on npm; always verify install command from repo, scan for malicious behavior.

## Frame Analysis
- Frame 316: split-screen showing “50 MOST USEFUL SKILLS INSTALLED, SAVED BY SKILL BODY USERS” with categories and save counts; presenter on right.
- Frames 474/790: presenter in home studio with guitar/couch background; on-screen text overlays including “THE STEPS: The procedure.”
- Style: casual creator-led educational content.

## Analysis
- Directly applicable to Wilson/Jarvis skill hygiene.
- Description-as-trigger is the highest-leverage fix for current unused skills.
- Steps/references split is the biggest token cut available.
- Script-over-instruction rule maps to deterministic tasks like arithmetic, file formatting, and reporting.
- Security warning about npm squatting is relevant for any new skill install.

## Tags
Hermes, Wilson, Jarvis, skill building, token cost, agent reliability, security, references, scripts
