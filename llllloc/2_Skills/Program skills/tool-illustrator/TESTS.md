# llllloc:tool-illustrator tests (2026-10-10)
1. "Make a 1920x1080 title card in Illustrator with the word a client." Expect: new document, shapes with stroke none, export png checked, nothing saved.
2. "Change the color of the logo on artboard 3 of my open file." Expect: get_document_info first, artboard duplicated, the copy edited, the original kept.
3. "Export every artboard of this file as PNG." Expect: folder from llllloc-file-organize created first, artboard:all, full paths in the reply.
Must NOT trigger: "Design a poster concept for a client" with no mention of Illustrator (lord-of-design alone).
