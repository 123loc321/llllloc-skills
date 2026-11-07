# 🏆 Visual Quality Codex — what makes an image read as premium

## Contents
- 1. The one idea under everything: design first, surface second
- 2. The craft dimensions — what to specify, and how to test it
- 3. Fake-premium signals — necessary but not sufficient
- 4. When something looks off — diagnose and fix
- 5. Pre-ship craft check (runs with the rule 5c second pass)
- 6. Taking this into video (without breaking rule 9)
- 🔓 OPT-IN — photoreal / game concept-art / key-art realism layer


A craft reference every mode draws on (IMAGE, VIDEO, SHOTLIST, DESIGN). It is **knowledge, not structure** — it does not change how a prompt is built, named, versioned, or delivered. Those rules live in SKILL.md and the mode modules and still rule.

What this file is *for*: it makes rule 2b ("specific, never generic") concrete. Rule 2b says spend words on the thing that causes quality instead of on adjectives — this file is the list of *which* things, and the tests that tell you whether the prompt actually has them. Use it while writing (to choose what to specify) and during the rule 5c second pass (to catch what's missing).

Two boundaries before anything else:

- **This is style-neutral by default.** Everything in the core sections is true for a hand-painted oil/gouache frame, an Arcane-style 2.5D shot, a flat graphic illustration, or a photoreal render alike. It is about composition, light logic, depth, and storytelling — not about a particular finish.
- **Photoreal / PBR / "AAA render" language is quarantined to the OPT-IN block at the bottom.** Do NOT pull material-fidelity or "Unreal-quality / commercial-photography" language into a painted or stylized job (GRUESOME, kok-boru, any stylized brief). It fights the look. Switch that block on only for photoreal product viz, realistic 3D, or ArtStation-style game concept/key art — see "🔓 OPT-IN" below.

---

## 1. The one idea under everything: design first, surface second

A premium frame is built in this order, and the order matters:

1. **Design foundation** — composition, value structure, silhouette, focal hierarchy, staging. *Is the underlying picture sound?*
2. **Rendering** — lighting, material, texture, colour. *Is it executed well?*
3. **Presentation** — framing, finish, the choices that sell it.

All three have to work, but foundation is load-bearing. Strong rendering on weak design is the single most common failure in AI work — call it **fake premium**: drama, detail, and contrast piled on a picture that has no real composition underneath. It scrolls past as "wow" and collapses the second anyone actually looks.

The job of a prompt is to specify the *foundation*, not just the surface. A prompt that names lighting and detail but never states where the subject sits or what the eye should hit first has skipped the part that matters most.

---

## 2. The craft dimensions — what to specify, and how to test it

Each one: what strong work does → the move to put in the prompt → the test (where there is a clean one). Ordered by leverage. You will not hit all ten in every prompt; hit the ones the shot lives or dies on.

**1. Composition & focal hierarchy.** Strong work places the subject deliberately — usually off-centre — and builds three reads: the one thing the eye hits first, the supporting detail that rewards a second look, and the ambient texture that justifies full resolution. It is never a centred subject with equal empty space on both sides and no path for the eye.
→ *Prompt move:* state where the subject sits and name the focal point's location — "subject in the left third, primary focal point on the face, lower-contrast supporting detail mid-frame." Specify the compositional logic, not just the subject.
→ *Test:* the eye lands on one clear subject within about half a second, and the frame still reads at thumbnail size. If the eye wanders with nowhere to settle, the hierarchy isn't there.

**2. Silhouette & shape language.** Characters, props, and hero objects read as a distinct shape even small. Strong shapes mix a big primary mass, a secondary break-up, and small tertiary detail — varied rhythm, not uniform busy-ness.
→ *Prompt move:* "distinct silhouette readable at thumbnail, large primary mass with smaller break-up detail, clear shape language for [role/personality]."
→ *Test — black-fill:* imagine the subject filled solid black. Does the shape alone still say what it is and what its role is? If the design only works once texture and colour are added, the form problem was never solved.

**3. Value structure.** Top work holds up in greyscale: a clear lightest light, a clear darkest dark, and a midtone field — a hierarchy you can read with all colour removed. Colour and detail cannot rescue a picture whose values are mush.
→ *Prompt move:* think in value first — "shadow-dominant frame with a single bright zone on the subject," not "dark and gritty" (a mood word with no value information).
→ *Test:* picture it in greyscale. Is there an obvious focal value contrast, or does everything sit at the same middle grey?

**4. Motivated lighting + temperature opposition.** The most reliable quality signal across every category. Light has a clear, identifiable source with logical shadow and fill. Strong setups oppose temperature — warm key against cool fill (or the reverse) — and use a rim/separation light to lift the subject off the background. Atmospheric light (haze, god rays, light through particles) adds depth and mood.
→ *Prompt move:* name the source, direction, and temperature, and oppose key and fill — "warm key from upper right, cool fill from the left, rim separating the subject from the background, soft haze in the midground." One dominant key; don't let multiple light directions fight.
→ *Test:* could you point to where the light comes from? Do the shadows agree with it? Are warm and cool actually doing opposite jobs, or just scattered around?

**5. Colour as a system, not local paint.** Treat colour as one structured scheme — roughly a 60/30/10 split between an ambient tone, a midground hue, and a focal accent — with saturation pushed hardest at the focal point and pulled out toward the edges. Major transitions shift hue, not just value. Random per-object colour reads as cluttered even when each object is fine on its own.
→ *Prompt move:* "dominant cool ambient, warm accent confined to the subject, desaturating toward the background," rather than "colourful" or a pile of unrelated colours.
→ *Test:* is there one clear temperature running the frame with saturation concentrated where the eye should go — or is colour sprinkled everywhere with no zoning?

**6. Atmospheric depth.** Real depth is a gradient, not just "a background." Foreground: highest contrast, highest saturation, sharpest edges. Midground: moderate on all three. Background: lowest contrast, cooler, more desaturated, softest. Strong frames stack at least three readable planes, often with a dark framing element up front (an arch, a branch, an overhang) the eye looks past into a lit midground.
→ *Prompt move:* "three depth planes — sharp high-contrast foreground element, lit midground subject, soft cool desaturated background — atmospheric recession between them."
→ *Test:* can you point to foreground, midground, and background and say what each is doing? Is the background actually receding, or is it as sharp and saturated as the front?

**7. Edge control.** Edges aim attention the way focus does on a camera: sharp where it matters (the face, the hands, the defining feature), soft where falloff is wanted (atmospheric depth, the periphery). The worst single signal is *the same edge quality everywhere* — it means no decision was made about what to emphasise.
→ *Prompt move:* "sharp defined edges on the face and key props, softer atmospheric edges on background elements — edge contrast as the attention guide."
→ *Test:* is sharpness highest at the focal point and softest at depth, or uniform across the whole frame?

**8. Storytelling density.** Premium frames carry several readable layers of story at once — the environment says something about the world, the costume and props about the role, the light about the mood. This is not the same as clutter: a sparse frame can be dense with story if every element earns its place.
→ *Prompt move:* give the world a few specifics that imply more than they show — "[environmental detail] establishing [world], silhouette and costume reading [role], every element earning its place."
→ *Test — one sentence:* could a viewer describe the world of this image in one sentence, with no caption? If not, the density isn't there yet.

**9. Stylization consistency.** In stylized work, every element sits in the *same* register and degree. If the lighting is painterly, the textures are painterly; if the characters are stylized, the environment matches. Mixing a photoreal element into a painted frame reads as uncontrolled, not as a hybrid. (This is the default lane for GRUESOME / kok-boru and most stylized briefs.)
→ *Prompt move:* name the register and hold it across the whole frame — "[Arcane-style painterly / oil-gouache / flat graphic] rendering throughout, secondary elements stylized to match the hero, no photoreal intrusions."
→ *Test:* does any one element look like it came from a different rendering process than the rest?

**10. Consistency across a sequence.** Across the different shots of one film or one project, hold a shared DNA: the same colour-temperature system, the same lighting logic, the same rendering register. This is what makes a set of shots feel like one world rather than a pile of separate images.
→ *Prompt move:* when writing several prompts for one piece, carry the established temperature/light/register forward into each so continuity holds across cuts.
→ *Note — not a contradiction of rule 10 (variation distinctness):* that rule makes multiple *variations of the same beat* look genuinely different in camera and staging. This makes *different shots of the same film* feel unified in colour and finish. Different axes — different camera treatment, same world.

---

## 3. Fake-premium signals — necessary but not sufficient

These traits are easy to generate and frequently mistaken for quality. They are fine to use — they are just not *evidence* of quality, and they must not stand in for design. When one shows up, run the real test.

| Signal | Why it misleads | The real test |
|---|---|---|
| Dramatic lighting | Easy to apply with no composition under it | Does the light reinforce the focal hierarchy, or fight it? |
| Hyper-detail everywhere | Procedural detail mimics craft | Is detail *denser at the focal point* than at the edges? |
| High global contrast | A one-slider post effect | Is contrast structurally placed, or just cranked across the whole frame? |
| Chromatic aberration / film grain | An aesthetic filter, not a quality marker | Is it where real lens physics would put it, or sprayed on? |
| Epic scale | Big environments read as impressive by default | Is there a clear story subject *inside* the scale? |
| Cinematic letterbox (2.39:1) | Bars create a "movie" feel cheaply | Does the framing actually use that width? |

The dominant AI failure pattern this guards against: **maximum surface complexity with no spatial grammar** — full detail at every depth plane, dramatic light on a frame with no composition, the subject dead-centre with no relational staging. Specify the foundation and this doesn't happen.

---

## 4. When something looks off — diagnose and fix

Common failure modes and the prompt fix for each.

| Looks like | Fix in the prompt |
|---|---|
| Everything equally sharp/detailed, no sense of depth | Add an explicit atmospheric gradient — sharp saturated foreground → soft cool background; vary edge sharpness by depth |
| Shadows pointing different ways on the same subject | Name one dominant key light with a single direction |
| Warm and cool scattered with no logic | Define the temperature system — warm key, cool fill, neutral ambient |
| Subject dead-centre, equal empty space both sides, static | Place the subject off-centre and state the compositional logic |
| Generic, unreadable silhouette | Add shape-language descriptors tied to the character/object's role and personality |
| Fabric, metal, stone all look the same | Name each material distinctly (and switch on the opt-in block if it's a realism job) |
| Every part of the frame at maximum drama at once | Reserve the drama — highest contrast and detail for the focal zone, lower it elsewhere |

---

## 5. Pre-ship craft check (runs with the rule 5c second pass)

A checklist, not a score. On the cold read before the deck, confirm the prompt actually carries the foundation:

- [ ] Composition stated — where the subject sits, what the eye hits first (not left to default centre framing)?
- [ ] Light **source + direction + temperature** named, with key/fill opposed?
- [ ] Depth roles assigned — foreground / midground / background each doing a job?
- [ ] Colour as a system — one dominant temperature, saturation concentrated at the focal point?
- [ ] Edges deliberately varied — sharp on focal, soft on ambient?
- [ ] Stylization register named and held consistent across the frame?
- [ ] Does every element earn its place (one-sentence-world test passes)?
- [ ] Dead adjectives avoided — "epic / 8k / masterpiece / hyper-detailed / trending on ArtStation / dramatic / cinematic" as filler (defer to rule 2b; replace each with the concrete thing that causes the look)?

If a box is empty and the shot needs it, fix the prompt before it ships.

---

## 6. Taking this into video (without breaking rule 9)

The craft above is composition logic — it carries straight into motion. The moves that translate:

- **Open on the design proof.** Establish the silhouette or the wide before cutting to detail; don't start on a close-up that hides the composition.
- **Move the camera *through* depth planes** — push past a foreground element into a lit midground — so atmospheric depth reads in motion, not just in a still.
- **Lock light motivation and the colour-temperature system across cuts.** Define it once, hold it, so the sequence feels like one world (dimension 10).
- **Let focus and edge aim the eye in motion** — a focus pull or a sharp-subject/soft-background relationship does the same job a static edge map does.
- **Hold the stylization register across every shot.**

**The hard line:** this governs the *craft* — depth, light, colour, edge, story. It does **not** touch pacing, camera energy, or cut rhythm. Those stay governed by **rule 9 (kinetic by default — restless camera, brisk motion, Arcane/Fortiche-grade animation)** and the active video module. Do **not** import a "slow, single camera move, no shake, hold the frame" default from general cinematic-quality advice — that contradicts rule 9. Take the depth-and-light craft; leave the calm-camera pacing.

For the kok-boru painted-on-twos style, express depth, light, and edge through *that* style's grammar — held poses, smear frames, on-twos snapping, controlled warm/cool light — never through motion blur or smooth gliding, which the style forbids.

---

## 🔓 OPT-IN — photoreal / game concept-art / key-art realism layer

**Off by default. Switch on only when the job is photoreal product visualization, realistic 3D, or ArtStation-style game concept / key art — and never for a painted or stylized brief (GRUESOME, kok-boru, any stylized look) unless the user explicitly asks for photoreal.** Everything in sections 1–6 still runs underneath; this block adds the realism layer on top.

When it's on:

- **Material / PBR fidelity.** Each material has to behave correctly at full resolution, and incorrect behaviour (plastic-looking skin, rubber-looking metal) is the fastest quality failure in realism work. Name each major material with its actual property: metal reflects by angle of incidence with little diffuse; rough surfaces scatter highlights; skin, leaves, and glass respond to backlight with subsurface or translucency; roughness varies within a single surface rather than being uniform. Wear and aging that tell the object's history (dust in crevices, edge damage, moisture in recesses) read as craft; a uniform clean surface reads as procedural.
- **Studio lighting language for product.** A three-point rig — key, fill, rim separation — over a neutral or contextually plain background, with a named aperture for depth of field. Judge it against real commercial photography, not concept-art standards.
- **Material consistency across angles.** In a multi-shot or turntable set, the metal stays metallic from every angle; material identity must not break as the camera moves.
- **The realism quality bar may be named here.** This is the one place "AAA key-art quality / Unreal-quality render / commercial-photography quality" earns its keep — and even here, only *alongside* the concrete light, material, and lens specifics, never instead of them (rule 2b still holds). A bare "Unreal Engine 5, 8k, photorealistic" with no real lighting or material detail underneath is still fake premium.

Keep this block off for stylized work. The style-neutral craft is what runs on every job; this is the realism add-on for the jobs that call for it.
