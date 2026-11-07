# BUILD FOR HIS HANDS

Part of `llllloc:task-motion`.

## BUILD FOR HIS HANDS [R33] [R36] (30 Sep, 2 Oct 2026)
He edits every film after Claude in the MOTION app. He needs three things in his hands: the text, the animation and the easing. Keyframes are a bonus.
- CODE OR LAYERS, WHICHEVER IS EASIER [R36]. One code layer may draw a whole scene when that is the easier and more efficient build. Then every text sits in a Content slot, and every move's timing, distance and easing is a named prop. Separate layers when he will move or restyle an element by hand.
- EVERY CLIP IS A PLACEHOLDER [R33]. Every clip or picture inside a frame (card, window, screen) is one he can swap in Content: its own layer masked by the frame's window, or a `src` slot on the code layer. A swapped file keeps the box, the crop and the motion.
- EVERY MOVE IS A NUMBER HE CAN SEE. Speed, delay, distance, stagger, blur, glow, opacity, the easing: each sits in a named layer property or a Content slot, never as a literal inside code. One number in the panel changes the whole thing. Name it in his words ("Rise", "Delay", "Glow"), and give it a unit.
- ONE EASING LANGUAGE PER FILM. Three named curves for the whole film: Appear in, Appear out, Move. Every layer takes them by name, so one change moves the film. A layer that needs its own curve says why in its name.
- GROUPS KEEP IT SMALL. Group layers by scene part (Title block, Country cards, Background), the group named in the film's words. A scene reads in ten rows or fewer when folded. Until MOTION ships groups, the group is a name prefix: `Title block / Headline`.
- ONE COLOR PER KIND. Label colors: text blue, pictures and clips green, shapes and cards yellow, effects and fields purple, background grey. The same on every film, so he reads a timeline at a glance.
- THE LAYER MAP. The V1 reply lists the groups, their layers or slots, and the one number that drives each move, in five to ten lines. The map is the handoff.

