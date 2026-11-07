# Tests for llllloc:task-design-system (17 Oct 2026)

### New UI with no system
Prompt: "Design the settings screen for the MOTION app" in a job folder with no DesignSystem file
Should trigger: yes, before llllloc:task-design builds anything
First file Claude should open: references/system-sheets.md
Done looks like: three or four rendered sheets, one trade-off line each, the reply ends on the question, nothing built

### A film with no look yet
Prompt: "Animate part 1 of the Lotus film in Cavalry" in a job with ART-DIRECTION.md but no DesignSystem file
Should trigger: yes, with llllloc:task-motion and llllloc:tool-cavalry waiting
First file Claude should open: references/system-sheets.md
Done looks like: sheets with one style frame each and a motion rule, the four showreel lines on the picked one, V1 written the turn he picks, ART-DIRECTION.md read into it and moved to Old/

### A live site to write down
Prompt: "Write the design system of <your-domain> so we can build the new page on it"
Should trigger: yes
First file Claude should open: references/design-system-from-product.md
Done looks like: DesignSystem_the studioCollective_V1.md with every value traced to the page, labeled a reconstructed draft

### He changes the look in words
Prompt: "Make the accent the lime from sheet 2, keep the rest" on a job with DesignSystem_Honda_V1.md
Should trigger: yes, NEW VERSION
First file Claude should open: references/file-template.md
Done looks like: DesignSystem_Honda_V2.md the same turn, one line on top saying what changed, V1 kept beside it

### Must not trigger
Prompt: "Move the title 20 px up on slide 3" on a job that has DesignSystem_Honda_V2.md
Should trigger: no. llllloc:task-design reads the file and nudges the slide. No sheets, no new version.
