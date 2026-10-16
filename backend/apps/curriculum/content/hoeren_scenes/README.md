# Hören background sounds

`manage.py make_hoeren_audio` mixes these under the voices: the scene plays alone
for about 1.5 s, then fades to a quiet bed (about 12 %) for the rest of the
recording. A recording that asks for a file that isn't here is skipped, never
made without it.

| File          | What                                     | Search for                                   |
|---------------|------------------------------------------|----------------------------------------------|
| `bahnhof.mp3` | train station: trains, footsteps, echo   | "train station ambience", "railway platform" |
| `strasse.mp3` | city street: traffic, people walking     | "city street ambience", "traffic pedestrians"|
| `cafe.mp3`    | café or restaurant: cups, soft chatter   | "cafe ambience", "restaurant background"     |
| `laden.mp3`   | shop or supermarket                      | "supermarket ambience", "store background"   |
| `buero.mp3`   | office or waiting room: typing, printer  | "office ambience", "waiting room"            |
| `park.mp3`    | park: birds, a little wind               | "park birds ambience"                        |
| `gong.mp3`    | the chime before an announcement (1-2 s) | "announcement chime", "airport ding dong"    |

- Scenes: 20-60 s that loop without a jump, no clear speech in them.
- Any format ffmpeg reads works if renamed to `.mp3`; stereo is mixed to mono.
- Use only **CC0** files (Freesound: filter "Creative Commons 0") or the
  **Pixabay** content licence. Note each file's source here:

| File | Source URL | Licence |
|------|------------|---------|
|      |            |         |
