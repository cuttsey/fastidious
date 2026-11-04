"""Compiles brief.json and a shot from shotlist.json into provider prompts.

The model sees one consistent visual language on every call: the brand's palette, light, lens, texture and
composition rules come from the brief, and only the subject, action and camera change per shot. That is
most of what separates a coherent film from a pile of good-looking clips.
"""

NO_TEXT = ("No text, letters, numbers, logos, captions, watermarks or interface writing anywhere in the frame; "
           "type is set separately in post.")


def style_block(brief):
    t = brief.get("tokens", {})
    lines = []
    if t.get("palette"):
        named = ", ".join(f"{k} {v}" for k, v in t["palette"].items())
        lines.append(f"Palette, held strictly: {named}. Nothing outside it except neutral shadow and highlight.")
    for key, label in (("light", "Light"), ("lens", "Lens and camera"), ("texture", "Texture and finish"),
                       ("composition", "Composition"), ("mood", "Mood")):
        if t.get(key):
            lines.append(f"{label}: {t[key]}.")
    if brief.get("sign"):
        lines.append(f"It should signify: {brief['sign']}.")
    return " ".join(lines)


def avoid_block(brief, shot):
    avoid = list(brief.get("avoid", [])) + list(shot.get("avoid", []))
    return ("Avoid: " + "; ".join(avoid) + ".") if avoid else ""


def frame_prompt(brief, shot):
    f = shot["frame"]
    parts = [f["prompt"].rstrip(".") + "."]
    if shot.get("type_space"):
        parts.append(f"Leave clean, quiet space {shot['type_space']} for a line of type added later.")
    parts += [style_block(brief), avoid_block(brief, shot), NO_TEXT]
    return " ".join(p for p in parts if p)


def negative_prompt(brief, shot):
    """For providers with a dedicated negative field (Kling): the avoid list plus the no-text rule."""
    avoid = list(brief.get("avoid", [])) + list(shot.get("avoid", []))
    return ", ".join(avoid + ["text", "letters", "logos", "watermark", "captions", "morphing", "flicker", "extra objects"])


def motion_prompt(brief, shot, n_refs=0, include_avoid=True):
    m = shot["motion"]
    parts = [m["prompt"].rstrip(".") + "."]
    if m.get("camera"):
        parts.append(f"Camera: {m['camera']}. One move only, eased in and out.")
    if n_refs:
        tags = ", ".join(f"@Image{i + 1}" for i in range(n_refs))
        parts.append(f"Keep the look, palette and materials of {tags} exactly.")
    parts.append("Physically plausible motion, no morphing, no flicker, no extra objects appearing.")
    parts += [avoid_block(brief, shot) if include_avoid else "", NO_TEXT]
    return " ".join(p for p in parts if p)
