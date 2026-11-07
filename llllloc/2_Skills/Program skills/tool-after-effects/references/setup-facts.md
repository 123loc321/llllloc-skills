# Setup facts

Moved from SKILL.md on 14 Oct 2026, unchanged. Read when the bridge, the license or a permission fails.

## SETUP FACTS (9 Oct 2026, checked live)
- Server: `@synthetic-ai/ae-mcp` through `npx`, version 2.11.0. Panel: Synthetic AE MCP CEP panel v2.10.9, installed at `~/Library/Application Support/Adobe/CEP/extensions/com.synthetic.ae-mcp.bridge`.
- The license key sits in TWO places: `AE_MCP_LICENSE` in `claude_desktop_config.json`, and the panel's Settings. A new key from Synthetic goes into both. Never print the key in a reply.
- The panel's Temp directory always resets to its default, `/var/folders/.../T/ae-mcp-bridge` (his words, 1 Nov 2026). So the server follows the panel: `AE_MCP_TEMP_DIR` in `claude_desktop_config.json` holds that path, read when the app starts. Without it the server writes to `/tmp/ae-mcp-bridge`, which the panel never reads. Commands processed 0 while Running means a folder mismatch. A `cmd_*.jsx` left in the folder means the panel is not reading it.
- macOS runs in panel mode only (Synthetic's own page). Standalone tools that launch After Effects or `aerender` are a fallback, 10 to 30 s each.
- Most tools need After Effects > Settings > Scripting & Expressions > Allow Scripts to Write Files and Access Network. "Permission denied" from a script means this is off.
- Synthetic Setup.app crashes on his Mac. Activation never needed it.
- Which app builds a job is his call per job. Never move a job between apps on your own.
