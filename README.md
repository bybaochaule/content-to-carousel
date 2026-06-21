# Content To Carousel

## Overview

Content To Carousel turns raw ideas, articles, transcripts, notes, briefs, or any topic into a complete, ready-to-post social media carousel/post series without using design tools.

The skill covers strategy, copy, image-by-image structure, visual direction, safe image-generation prompts, one-at-a-time image generation, verification, and refinement.

## What changed in this rewrite

This version is rebuilt around the supplied `carousel-prompt-v4.md` workflow:

- Mandatory brand context before any design planning.
- Fast one-question-at-a-time briefing.
- Platform specs for Instagram, TikTok, Facebook, LinkedIn, and YouTube.
- Format recommendation before drafting.
- Image-by-image plan that must be approved before generation.
- Safe image prompts that avoid terms known to cause multi-image layouts.
- One generated image per user message.
- Verification and refinement rules.

The image-prompt reset phrase was sanitized so the actual prompts do not contain the forbidden image-generation terms.

## Use cases

Use this skill to create:

- LinkedIn carousel posts.
- Instagram carousel posts.
- TikTok photo-mode style posts.
- Facebook educational or promotional post sequences.
- YouTube community cards.
- Sales, launch, education, authority, lead-generation, case-study, tutorial, and thought-leadership content.
- Image-generation prompts for each post image.
- Generated images one at a time.

## Package contents

- `SKILL.md`: agent instructions, workflow, boundaries, output format, safety rules, and quality checks.
- `README.md`: human-readable package overview.
- `agents/openai.yaml`: display metadata and invocation policy.
- `references/style-guide.md`: copywriting and visual style standards.
- `references/format-options.md`: supported content formats and when to use them.
- `references/image-prompt-rules.md`: forbidden prompt terms, safe prompt template, and verification rules.
- `assets/briefing-template.md`: reusable brand and briefing questions.
- `assets/image-prompt-template.md`: reusable safe image prompt template.
- `assets/post-series-plan-template.json`: reusable JSON planning schema.
- `scripts/image_prompt_linter.py`: deterministic checker for image prompts.
- `scripts/plan_linter.py`: deterministic checker for JSON plans.
- `scripts/example_helper.py`: safe placeholder helper.

## Default behavior

The skill first asks for brand colors and visual style. After brand context is locked, it asks for the idea and essential briefing inputs. It then recommends a format, creates an image-by-image plan, waits for approval, outputs all prompts, and generates only one image per user message.

## Package structure

```text
content-to-carousel/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── briefing-template.md
│   ├── image-prompt-template.md
│   └── post-series-plan-template.json
├── references/
│   ├── format-options.md
│   ├── image-prompt-rules.md
│   └── style-guide.md
└── scripts/
    ├── example_helper.py
    ├── image_prompt_linter.py
    └── plan_linter.py
```
