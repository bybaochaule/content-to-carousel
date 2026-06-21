# Safe Image Prompt Template

Use this template for every individual image-generation prompt.

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

Before sending the prompt to image generation, run the forbidden-term check from `references/image-prompt-rules.md` or use `scripts/image_prompt_linter.py`.
