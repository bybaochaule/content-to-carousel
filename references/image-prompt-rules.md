# Image Prompt Rules

## Core rule

Every prompt sent to image generation must describe exactly one output as:

```text
one standalone social media post design
```

Never ask the image model for a combined view, preview board, gallery, template sample, or multiple post designs in one image.

## Forbidden prompt terms

The following terms must never appear in image-generation prompts:

- carousel
- slide
- slides
- slide deck
- multi-slide
- swipe
- sequence
- series
- panel
- set of
- collection
- contact sheet
- grid
- collage
- mockup
- preview
- part 1 of
- one of eight
- batch

These terms may appear in agent instructions, user-facing planning text, or documentation, but never in prompts sent to image generation.

## Safe reset text

Use this at the start of every prompt sent to image generation:

```text
You are creating ONE standalone social media post design.
This is the ONLY image.
One design fills the entire canvas edge to edge.
Use one focal point and one composition only.
Do not show multiple separate designs.
```

## Safe prompt template

```text
You are creating ONE standalone social media post design.
This is the ONLY image.
One design fills the entire canvas edge to edge.
Use one focal point and one composition only.
Do not show multiple separate designs.

Create one social media post design, [dimensions].

Brand: [colors from brand context], [style from brand context]
Logo: [logo placement if applicable]

Headline: "[headline]"
Text: "[supporting text]"
Visual: [visual direction]

Layout: large headline, short text, one focal point, generous whitespace, mobile-readable typography, premium composition, strong contrast. The design fills the entire canvas edge to edge.
```

## If the output is invalid

If the generated output contains multiple separate designs or an unwanted combined layout:

1. Tell the user: "That came out as a grid. Regenerating."
2. Try again with a simplified safe prompt:

```text
You are creating ONE standalone social media post design.
This is the ONLY image.
One design fills the entire canvas edge to edge.
Use one focal point and one composition only.
Do not show multiple separate designs.

Create one social media post design, [dimensions].
Background: [solid brand color]
Large headline: "[headline]"
Small text: "[supporting text]"
Use strong contrast, large readable type, generous whitespace, and one simple focal visual.
```

3. If it fails again, give the user the simplified prompt text and recommend pasting it into a fresh image-generation session.

## Cadence

- After plan approval, output all prompts as text first.
- Then generate only image 1.
- After each generated image, wait for the user's confirmation before generating the next image.
- Never generate more than one image per user message.
- Never pass the full plan into image generation.
