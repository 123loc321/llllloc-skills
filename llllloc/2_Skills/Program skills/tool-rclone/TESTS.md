# llllloc:tool-rclone: tests (28 Oct 2026)

Each prompt names what a right run does. Built from the thread "Speed up the Showreel download" (28 Oct 2026).

1. "download this Drive folder into the client 1_VISUAL ASSET: https://drive.google.com/drive/folders/<id>"
   Right: path from the map row, `rclone size` on the ID first, a copy job started through Rclone UI (rc on localhost:5572) with the explicit destination folder, not `rclone sync`. Reply names size, speed after 20 s, where to watch.
2. "Cyberduck is slow, finish this download with rclone"
   Right: asks him to Stop the Cyberduck transfer first, copies into the SAME folder (finished files skipped), measures the line with `networkQuality` before blaming a tool.
3. "mirror my CREATIVE #1 folder X to this Drive folder every hour"
   Right: uses `gd-studio-write`, runs `drive-mirror.sh ... --dry-run` first and shows what would upload or move, waits for his go, then schedules. Never runs a mirror with the read-only remote, never on an unplugged drive.

Must NOT trigger: "the Showreel Premiere timeline needs the new clips" (a Premiere job, llllloc:tool-premiere-pro).
