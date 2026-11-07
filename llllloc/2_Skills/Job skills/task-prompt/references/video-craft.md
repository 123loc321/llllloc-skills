# Video craft, every video model

Read for every video prompt: Seedance, Kling, Minimax, Veo, Sora, Runway. The model syntax lives in its own file: `seedance-video.md` for Seedance. Another model keeps this craft and its own syntax from its lesson file and the research cache (16 Oct 2026, split out of `seedance-video.md`).

## Contents
- Core Operating Logic (1 to 8)

## Core Operating Logic

### 1. Visual Heritage Lock
**Naming convention (Seedance — Type 2 numbered tags, the usual choice):** By default Seedance prompts reference uploaded assets by NUMBERED tags (Type 2) — `@Image 1`, `@Image 2`, `@Image 3`… and `@Video 1`, `@Video 2`… in upload order. Use Type 2 UNLESS the user chose **Type 1 / `@Filename`** (or wrote "name mention", or the target is Magnific) under SKILL.md rule 7b — in which case use name tags instead (see the Exception below). Per SKILL.md rule 7b, when media is attached and the user hasn't stated a style, ask Type 1 vs Type 2 before writing rather than assuming.

**Exception — Type 1 / "name mention" mode (overrides the numbered tags):** If the user chose **Type 1 / `@Filename`** (rule 7b) OR their request contains the phrase **"name mention"** (case-insensitive), do NOT use numbered tags — instead reference every image and video by its **name**, prefixed with `@`, no quotes, no extension (e.g. `@hjhjhj`, `@drone_shot`). Keep an existing name verbatim; for any unnamed asset, create a short descriptive name (1–3 words, no spaces) and tell the user in one line what you named it, reusing it for the rest of the chat. The name tag stays identical in BOTH the CN and EN versions — never translate it. Full spec in SKILL.md rules 6 & 7b.

Treat `@Image 1` as the primary visual truth unless the user clearly says otherwise, OR unless a storyboard is provided (in which case the storyboard takes structural precedence — see Storyboard Handling).

Rigorously preserve from `@Image 1`:
- Main subject identity
- Face, body, silhouette, costume, hairstyle, props
- Composition logic
- Lighting direction
- Color palette
- Material feel
- Original art style

Do not hallucinate new characters, objects, outfits, or scenery that are not supported by the image(s) or the brief, unless the user explicitly asks for them.

### 1.5. Character Likeness Lock — let the reference image carry appearance (🔴 key for character consistency)

**The problem this solves:** When a character sheet / character reference image is attached, describing the character's appearance in the prompt TEXT (face, hairstyle, costume, colors, build, distinctive features) makes that text COMPETE with the reference image. Seedance tries to reconcile words vs. image, the words "win" or average against the picture, and the generated character drifts off the reference — coming out looking like a different character. **The textual appearance description is itself the cause of the drift.**

**The rule:** When a character reference image / character sheet is provided (e.g. `@Image 1` or a tagged character sheet), DO NOT describe the character's appearance in the prompt. Point the model directly at the reference image as the single authoritative source of likeness, and let the image — not your words — define how the character looks.

**STOP describing — defer ALL of this to the reference image:**
- Face, facial features, skin tone, perceived age
- Hairstyle, hair color, facial hair
- Body type, build, height, silhouette
- Costume, outfit, garments, colors, materials, textures
- Distinctive marks, tattoos, scars, accessories, signature props
- The art style of the character render itself

**STILL direct in the prompt — these are dynamic and not in a static sheet:**
- What the character DOES — action, blocking, movement through the shot
- Expression and emotional trajectory over time (e.g. calm → alarmed → resolute)
- Pose and body mechanics during the action (weight, gesture, how they move)
- Cross-shot behavioral continuity (the same person carrying through cuts)

These are performance directions, not identity descriptions. Write them as verbs and beats, never as a re-description of who the character is.

**Phrasing to use INSTEAD of an appearance description** — drop in an explicit lock line that orders the model to read the sheet:
- CN: `角色外形（面部、发型、体型、服装、配饰、材质）一律严格以 @Image 1 角色设定图为唯一依据，请直接参照该图本身，禁止在提示词中重新描述或重新诠释角色长相。`
- EN: `All character appearance — face, hair, build, costume, accessories, materials — is defined solely by the @Image 1 character sheet. Read it directly from the image; do NOT re-describe or reinterpret the character's look in text.`

In the 【参考锁定 / Reference Lock】 section, name the character sheet explicitly as the appearance source — e.g. `@Image 1 = 角色设定图 / character sheet — sole source of likeness, preserve exactly`.

**Exception:** If NO character reference image is attached (pure text-to-video), you obviously must describe appearance in text — there is no image to defer to. This rule applies only when a character reference / sheet exists.

### 2. Multi-Image Handling
If the user provides multiple images, explicitly reference them inside the prompt as `@Image 1`, `@Image 2`, `@Image 3`, etc.

State the role of each image when relevant, for example:
- `@Image 1`: primary character continuity (主体形象基准)
- `@Image 2`: outfit / material reference (服装/材质参考)
- `@Image 3`: environment / mood reference (环境/氛围参考)

If only one image is provided, still mention it as `@Image 1`.

The `@Image N` tags must remain in their original English form in BOTH the English and Chinese prompt versions. Do NOT translate the tags themselves.

### 3. Storyboard Handling (NEW)
If the user uploads a storyboard — a multi-panel image showing the planned shot sequence — treat it as the **authoritative structural blueprint** for the entire video.

Rules:
- Identify the storyboard image and label it as `@Image [N] (storyboard / 分镜稿)` in the Reference Lock section.
- Map every storyboard panel one-to-one to a corresponding shot in the second-by-second action script.
- Preserve panel order, framing, composition, camera angle, subject placement, and action intent EXACTLY as drawn.
- Do not add, remove, merge, or reorder panels unless the user explicitly allows it.
- If the storyboard contains fewer than 7 or more than 12 panels, retain the storyboard's panel count and override the default 7–12 shot range. The storyboard always wins on shot count.
- If panels contain hand-written notes (camera moves, dialogue, SFX cues, timing), incorporate those notes faithfully into the corresponding shot description.
- If a panel is ambiguous, infer the most cinematically logical interpretation but do not invent unrelated content.

### 4. Video Reference Handling (NEW)
If the user uploads videos, label them as `@Video 1`, `@Video 2`, `@Video 3`, etc., in the order they were uploaded.

By default a video gives motion and mood. It is used to inform:
- Motion pacing and rhythm
- Camera dynamics (handheld feel, whip pans, dolly behavior, etc.)
- Transition style
- Mood, energy, atmosphere
- Lighting behavior over time
- Color grading feel
- Cut tempo

**What carries over:** by default not the subject of an outside video (characters, faces, costumes, locations, props, logos, set pieces, dialogue), because a prompt that copies a subject from someone else's video makes a copy, not a new film. When he or the client says a video is their own, or names an element to keep (their logo, their face, their product, their set), that element is carried into the prompt as given. No legal rule caps a job (his words, 17 Oct 2026).

In the Reference Lock section, explicitly state what each video is being used for and what it does not contribute. Example:
- `@Video 1`: handheld whip-pan rhythm and chaotic energy; subject, location and props not carried.
- `@Video 2`: the client's own film; carry the product, the logo and the warm dusk lighting as seen.

The `@Video N` tags must remain in their original English form in BOTH the English and Chinese versions.

### 5. Dynamic Rhythm Planning
Automatically decide the number of shots based on story complexity:
- Minimum 7 shots
- Maximum 12 shots
- Gentle, elegant, emotional, or one-take concepts → fewer and longer shots.
- Intense, destructive, action-heavy, or high-energy concepts → more cuts and tighter timing.

**Exception:** If a storyboard is provided, follow the storyboard's panel count instead.

The whole structure must still feel smooth and intentional, not randomly fragmented.

### 6. Narrative Logic
**Default mode:** Create a complete 15-second arc with:
beginning → development → escalation → climax → resolution.

**Instruction mode:** If the user provides a specific sequence OR a storyboard, obey it precisely and do not force the default arc.

### 7. Physical Sensory Language
Describe action in a cinematic, tactile, physically readable way.
Favor sensory details such as:
- drifting dust / 飘散的尘埃
- cloth drag / 衣料拖曳
- surface tremor / 表面震颤
- splintering fragments / 碎裂飞溅
- pressure ripples / 气压涟漪
- lens breathing / 镜头呼吸
- light streaks / 光痕拉丝
- smoke shear / 烟雾切层
- shockwave flutter / 冲击波震颤
- rain scatter / 雨点散射
- embers peeling through air / 火星在空中剥离

### 8. Prompt Discipline
Write with precise, visual, cinematic language in BOTH languages.
- Prefer direct cause-and-effect motion.
- Avoid vague filler.
- Avoid conflicting actions in the same moment.
- Make every shot readable, generatable, and cool on screen.
