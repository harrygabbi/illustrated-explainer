---
name: illustrated-explainer
description: Produce illustrated YouTube explainers and companion Shorts from a script or topic. Use for still-led ink drawings, an opening hook, shot and narration timing, optional ElevenLabs voiceover, captions, thumbnails, and an edited MP4.
---

# Illustrated explainer

Use the narration to determine when the picture changes. Build each beat around a readable drawing, then change the composition, cut to a prop or diagram, or swap a pose when the meaning changes. Reserve movement for a story action or a small detail such as firelight, smoke, or a pointer.

## Choose the deliverable

- **Hook or style test.** Start with a concrete object, action, or consequence in the first frame. A silent review cut can use timed subtitles and local artwork. Use the requested duration and check it in the export.
- **Full episode.** Extract the spoken lines from the supplied script and count them before recording. Keep the author's wording and scene order when they request a faithful reading. Flag any material conflict between the requested runtime and the actual word count. Check substantive factual claims against primary sources and make sure the script distinguishes evidence, interpretation, and fiction.
- **Companion Short.** When the user wants to reuse the long film, select clean excerpts from its dialogue stems and reframe the pictures for portrait. Give the excerpt a coherent arc and preserve a reason to watch the full episode. Treat a requested outro as additional to the stated main-cut duration when the user says it follows the cut.
- **Thumbnail.** Use the requested references to understand headline placement, palette, detail, and composition. Draw an original scene that adds a question or tension to the title. Check the headline and focal expression at about 320 pixels wide.

Read [visual and writing direction](references/direction.md) when developing the hook, scene design, or cover. Read [production and export](references/production.md) when estimating narration, recording, aligning, or delivering a video.

## Match the production to the review stage

Use the accepted visual reference and the user's script to plan the scenes. Establish the main character, palette, recurring props, and one visual thread across chapters. Build a small set of reusable locations and props. Vary the framing with a wide location, an expressive medium shot, and close-ups of evidence or objects.

Use an existing voice and settings when continuity matters. If the user requests a cost check, use the provider's estimate mode on the spoken text only. Record the estimated and actual units separately. For a silent or subtitle-only request, render locally without making a speech-generation call.

Align captions and shot changes to the final recording. Check the rough cut for reading time, visible faces and props, chapter labels that stay clear of diagrams, clean audio edits, and a readable last frame. Deliver the requested MP4 and any requested companion assets. The bundled [still-cut renderer](scripts/render_stills.py) can build a review cut or final still-led video from timed images and optional mixed audio and SRT captions.
