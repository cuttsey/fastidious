# Formats

Build artwork at the format's true ratio. Sizes are for artwork files. Print production adds bleed and resolution: check the media owner's specification before going to print.

## Devices (capture viewports)
| Device | CSS viewport | Capture dsf | Notes |
|---|---|---|---|
| Phone | 390 × 844 | 2–3 | iPhone-class; a scroll of 6–8 s reads well |
| Tablet | 834 × 1194 | 2 | portrait; landscape 1194 × 834 |
| Laptop | 1440 × 900 | 1–2 | the most common desktop presentation size |
| Desktop / TV | 1920 × 1080 | 1 | for in-store screens and DOOH content |

## UK out-of-home (paper)
| Format | Size | Ratio | Artwork px (screen presentation) |
|---|---|---|---|
| 48-sheet billboard | 6096 × 3048 mm | 2:1 | 2400 × 1200 |
| 96-sheet | 12192 × 3048 mm | 4:1 | 3200 × 800 |
| 6-sheet (bus shelter, street panel) | 1200 × 1800 mm | 2:3 | 1200 × 1800 |
| 4-sheet (Tube, rail platforms) | 1016 × 1524 mm | 2:3 | 1016 × 1524 |
| Double crown (Tube cross-track, small venues) | 508 × 762 mm | 2:3 | 1016 × 1524 |
| 16-sheet (Tube cross-track) | 3048 × 2032 mm | 3:2 | 1800 × 1200 |
| A-board / shop window | A1 594 × 841 mm | 1:√2 | 1190 × 1684 |

## Digital out-of-home (DOOH)
| Format | Pixels | Motion |
|---|---|---|
| Digital 6-sheet (portrait) | 1080 × 1920 | 5–10 s loops; often no sound, sometimes stills only |
| Large-format digital (landscape) | 1920 × 1080 (or the screen's own size) | slow, legible motion |
| Rail and station portrait screens | 1080 × 1920 | similar to D6 |

## Display advertising (IAB)
| Name | Size |
|---|---|
| Medium rectangle (MPU) | 300 × 250 |
| Leaderboard | 728 × 90 |
| Half page | 300 × 600 |
| Billboard | 970 × 250 |
| Mobile banner | 320 × 50 |
| Skyscraper | 160 × 600 |
Keep animation to 15 s or less and three loops at most. End on the logo and call to action.

## Social
| Placement | Size |
|---|---|
| Post (4:5) | 1080 × 1350 |
| Square | 1080 × 1080 |
| Story / Reel | 1080 × 1920 |
| X header | 1500 × 500 |
| LinkedIn page cover | 1128 × 191 |
| Facebook cover | 1640 × 624 |
| YouTube banner | 2560 × 1440 (safe area 1546 × 423) |

## Camera and timing defaults
- Clips run 6–10 s at 30fps, 1920 × 1080. Hold the first and last half-second.
- Devices: orbit 20–30° of yaw across the clip and 5–15° of pitch; the laptop is seen from above (negative `rx`).
- Photos: push in from zoom 1.0–1.15 to 1.2–1.35, centred on the surface.
- Paper paste: a 1.5–2 s wipe starting at 0.5 s. Digital slides: change every 2.5–3 s.
