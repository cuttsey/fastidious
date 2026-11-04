"""fmotion: generate stills and motion from a Fastidious brief through image and video model APIs.

    python3 -m fmotion init                      create ./motion with a brief and shot list to fill in
    python3 -m fmotion validate                  check brief.json and shotlist.json before spending anything
    python3 -m fmotion frames  [--shots S01,S02] [--final] [--dry-run]
    python3 -m fmotion edit    O-004 "warmer key light, lower horizon" [--final]
    python3 -m fmotion pick    O-004 --reason "only option that keeps the horizon quiet"
    python3 -m fmotion animate [--shots ...] [--provider seedance|kling|seedance,kling] [--draft] [--seed 7] [--dry-run]
    python3 -m fmotion status  [--wait]          poll every provider, download finished clips, make review strips
    python3 -m fmotion palette O-011             measure a still or clip against the brand palette
    python3 -m fmotion assemble [--music track.mp3]
    python3 -m fmotion check   A-001             flash, loudness and format checks on a cut
    python3 -m fmotion cost                      calls and seconds spent so far, priced from config rates

Every generated still and clip gets a permanent O- ID; every pick is a D-; every cut is an A-.
"""
import argparse
import json
import os
import shutil
import sys
import time

from . import config, ledger, media, prompts, providers

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(HERE, "..", "templates")


def ws_path(args, *p):
    return os.path.join(args.dir, *p)


def load_json(path):
    if not os.path.exists(path):
        raise SystemExit(f"{path} is missing. Run `fmotion init`, then fill it in from the Fastidious artefacts.")
    with open(path) as f:
        return json.load(f)


def load(args):
    brief = load_json(ws_path(args, "brief.json"))
    shots = load_json(ws_path(args, "shotlist.json"))
    return brief, shots, ledger.Ledger(args.dir), config.load(args.dir)


def select(shots, wanted):
    if not wanted or wanted == "all":
        return shots["shots"]
    keep = set(wanted.split(","))
    return [s for s in shots["shots"] if s["id"] in keep]


def picked(led, shot_id, kind):
    """The current pick for a shot: the latest decision that chose an option of this kind."""
    ds = [d for d in led.find(kind="D", shot=shot_id) if d.get("type") == kind]
    return led.get(ds[-1]["option"]) if ds else None


def ref_paths(brief, ids, led):
    out = []
    refs = {r["id"]: r for r in brief.get("references", [])}
    for rid in ids or []:
        if rid.startswith("O-"):
            out.append(led.get(rid)["file"])
        elif rid in refs:
            out.append(refs[rid]["path"])
        else:
            raise SystemExit(f"Reference {rid} is neither an O- option nor in brief.references.")
    for p in out:
        if not os.path.exists(p):
            raise SystemExit(f"Reference file {p} does not exist.")
    return out


def write_request(args, name, req):
    path = ws_path(args, "requests", f"{name}.json")
    shown = json.loads(json.dumps(req, default=str))
    for item in shown.get("json", {}).get("content", []):  # keep dry-run files readable
        if item.get("type") == "image_url":
            item["image_url"]["url"] = item["image_url"]["url"][:48] + "...(base64)"
    with open(path, "w") as f:
        json.dump(shown, f, indent=2)
    return path


# ---- commands ------------------------------------------------------------------------------------------

def cmd_init(args):
    for sub in ("frames", "clips", "sheets", "requests", "out", "refs"):
        os.makedirs(ws_path(args, sub), exist_ok=True)
    for name in ("brief.json", "shotlist.json"):
        dst = ws_path(args, name)
        if not os.path.exists(dst):
            shutil.copy(os.path.join(TEMPLATES, name), dst)
    print(f"Workspace ready in {args.dir}. Fill brief.json from FRAME.md, POSITIONING.md, SIGN-SYSTEM.md, "
          "BRAND-SYSTEM.md and REFERENCES.md, then write shotlist.json.")


def cmd_validate(args):
    brief, shots, led, cfg = load(args)
    problems = []
    for k in ("purpose", "audience", "single_idea", "sign", "tokens"):
        if not brief.get(k):
            problems.append(f"brief.{k} is empty")
    if not brief.get("tokens", {}).get("palette"):
        problems.append("brief.tokens.palette is empty: the palette check and every prompt depend on it")
    for r in brief.get("references", []):
        if not os.path.exists(r.get("path", "")):
            problems.append(f"reference {r.get('id')} file missing: {r.get('path')}")
        if not r.get("borrow"):
            problems.append(f"reference {r.get('id')} says nothing about what to borrow")
    total = 0
    for s in shots.get("shots", []):
        sid = s.get("id", "?")
        for k in ("intent", "seconds", "frame", "motion"):
            if not s.get(k):
                problems.append(f"{sid}: {k} is missing")
        total += float(s.get("seconds", 0))
        if not 4 <= int(s.get("clip_seconds", max(4, round(s.get("seconds", 5))))) <= 15:
            problems.append(f"{sid}: Seedance 2.0 clips run 4 to 15 seconds; set clip_seconds in range")
        prompt = (s.get("frame", {}).get("prompt", "") + " " + s.get("motion", {}).get("prompt", "")).lower()
        for word in ("text that says", "logo", "headline", "caption", "the words"):
            if word in prompt:
                problems.append(f"{sid}: asks the model for '{word}'. Set type in post; models misspell it")
        if len(s.get("frame", {}).get("directions", [])) == 1:
            problems.append(f"{sid}: one direction is not a choice. Give two or more, or none")
    print(f"{len(shots.get('shots', []))} shots, {total:.1f}s planned.")
    if problems:
        print("Fix before generating:\n- " + "\n- ".join(problems))
        sys.exit(1)
    print("Brief and shot list are ready.")


def _variants(shot):
    dirs = shot["frame"].get("directions") or [None] * int(shot["frame"].get("variants", 3))
    return dirs


def cmd_frames(args):
    brief, shots, led, cfg = load(args)
    token = None if args.dry_run else config.key("OPENAI_API_KEY")
    api = providers.OpenAIImages(cfg, token)
    quality = cfg["image_quality_final"] if args.final else cfg["image_quality_draft"]
    for shot in select(shots, args.shots):
        size = shot["frame"].get("size", cfg["image_size_draft"])
        refs = ref_paths(brief, shot["frame"].get("references"), led)
        made = []
        for n, direction in enumerate(_variants(shot), 1):
            text = prompts.frame_prompt(brief, shot)
            if direction:
                text = f"Direction: {direction}. " + text
            req = api.edit_request(text, refs, size, quality) if refs else api.generate_request(text, size, quality)
            if args.dry_run:  # a dry run spends nothing and takes no IDs
                print(f"{shot['id']} v{n}: request written to {write_request(args, shot['id'] + f'-frame-v{n}', req)}")
                continue
            oid = led.new("O", type="still", shot=shot["id"], prompt=text, direction=direction, quality=quality,
                          references=shot["frame"].get("references", []), status="requested")
            img = api.send(req)[0]
            path = ws_path(args, "frames", f"{oid}.png")
            with open(path, "wb") as f:
                f.write(img)
            led.update(oid, status="generated", file=path)
            made.append((path, f"{oid} {direction or ''}".strip()))
            print(f"{oid} {shot['id']}: {path}")
        if made:
            sheet = media.sheet_stills(made, ws_path(args, "sheets", f"{shot['id']}-frames.png"))
            print(f"Review sheet: {sheet}")


def cmd_edit(args):
    brief, shots, led, cfg = load(args)
    src = led.get(args.option)
    shot = next(s for s in shots["shots"] if s["id"] == src["shot"])
    token = None if args.dry_run else config.key("OPENAI_API_KEY")
    api = providers.OpenAIImages(cfg, token)
    refs = [src["file"]] + ref_paths(brief, shot["frame"].get("references"), led)
    text = (f"Edit the first image: {args.instruction}. Change nothing else. " + prompts.style_block(brief) + " " + prompts.NO_TEXT)
    quality = cfg["image_quality_final"] if args.final else cfg["image_quality_draft"]
    req = api.edit_request(text, refs, shot["frame"].get("size", cfg["image_size_draft"]), quality)
    if args.dry_run:
        print(f"Request written to {write_request(args, args.option + '-edit', req)}")
        return
    oid = led.new("O", type="still", shot=shot["id"], prompt=text, parent=args.option, note=args.instruction,
                  status="requested")
    path = ws_path(args, "frames", f"{oid}.png")
    with open(path, "wb") as f:
        f.write(api.send(req)[0])
    led.update(oid, status="generated", file=path)
    media.sheet_stills([(src["file"], f"{args.option} before"), (path, f"{oid} after")],
                       ws_path(args, "sheets", f"{oid}-edit.png"), cols=2)
    print(f"{oid}: {path}")


def cmd_pick(args):
    led = ledger.Ledger(args.dir)
    opt = led.get(args.option)
    if opt.get("status") not in ("generated", "succeeded"):
        raise SystemExit(f"{args.option} has status {opt.get('status')}; only finished options can be picked.")
    did = led.new("D", shot=opt["shot"], option=args.option, type=opt["type"], reason=args.reason or "")
    print(f"{did}: {args.option} chosen for {opt['shot']}.")


def _providers_for(args, shot, film, cfg):
    """--provider wins, then the shot's motion.provider, then film.video_provider, then config."""
    names = args.provider or shot["motion"].get("provider") or film.get("video_provider") or cfg["video_provider"]
    return [n.strip() for n in names.split(",") if n.strip()]


def cmd_animate(args):
    brief, shots, led, cfg = load(args)
    film = shots.get("film", {})
    ratio = film.get("ratio", "16:9")
    res = cfg["video_resolution_draft"] if args.draft else film.get("resolution", cfg["video_resolution_final"])
    order = [s["id"] for s in shots["shots"]]
    apis = {}
    for shot in select(shots, args.shots):
        still = picked(led, shot["id"], "still")
        if not still:
            print(f"{shot['id']}: no still picked yet. Run frames, review the sheet, then pick.")
            continue
        # Kling's output follows the input image's shape, and Seedance's first frame should match the film,
        # so every provider gets the approved still cropped to the film ratio.
        first = media.crop_to_ratio(still["file"], ws_path(args, "frames", f"{still['id']}-{ratio.replace(':', 'x')}.png"), ratio) \
            if not args.dry_run else still["file"]
        m = shot["motion"]
        last = None
        if m.get("end_frame") == "next":  # land exactly on the next shot's approved frame
            i = order.index(shot["id"])
            nxt = picked(led, order[i + 1], "still") if i + 1 < len(order) else None
            last = nxt and nxt["file"]
        elif (m.get("end_frame") or "").startswith("O-"):
            last = led.get(m["end_frame"])["file"]
        seconds = int(shot.get("clip_seconds", max(4, round(shot["seconds"]))))
        seed = args.seed if args.seed is not None else int(m.get("seed", film.get("seed", -1)))
        for name in _providers_for(args, shot, film, cfg):
            if name not in apis:
                apis[name] = providers.video(name, cfg, draft=args.draft, dry_run=args.dry_run)
            api = apis[name]
            if name == "seedance":
                refs = ref_paths(brief, m.get("references"), led)
                text = prompts.motion_prompt(brief, shot, n_refs=len(refs))
                req = api.create_request(text, first_frame=first, last_frame=last, references=refs, ratio=ratio,
                                         resolution=res, duration=seconds, seed=seed, camera_fixed=bool(m.get("camera_fixed")))
                detail = {"resolution": res, "seed": seed}
            else:
                text = prompts.motion_prompt(brief, shot, include_avoid=False)
                if m.get("camera_fixed"):
                    text += " The camera does not move."
                if m.get("references"):
                    print(f"{shot['id']}: Kling ignores motion.references; continuity comes from the first and last frames.")
                req = api.create_request(text, first_frame=first, last_frame=last,
                                         negative_prompt=prompts.negative_prompt(brief, shot), duration=seconds)
                detail = {"resolution": req["json"]["mode"], "mode": req["json"]["mode"]}
            if args.dry_run:
                print(f"{shot['id']} {name}: request written to {write_request(args, shot['id'] + '-motion-' + name, req)}")
                continue
            oid = led.new("O", type="clip", shot=shot["id"], provider=name, prompt=text, from_still=still["id"],
                          model=api.model, draft=args.draft, seconds=seconds, status="submitted", **detail)
            task = api.send(req)
            led.update(oid, task=task)
            print(f"{oid} {shot['id']}: {name} task {task} submitted ({detail['resolution']}, {seconds}s).")
    if not args.dry_run:
        print("Run `fmotion status --wait` to collect the clips.")


def cmd_status(args):
    brief, shots, led, cfg = load(args)
    from . import net as http
    apis = {}
    deadline = time.time() + cfg["poll_timeout_seconds"]
    while True:
        for item in led.find(type="clip", status="submitted"):
            name = item.get("provider", "seedance")
            if name not in apis:
                apis[name] = providers.video(name, cfg)
            r = apis[name].result(item["task"])
            if r["status"] == "succeeded":
                path = ws_path(args, "clips", f"{item['id']}.mp4")
                http.download(r["video_url"], path)
                extra = {}
                if r.get("last_frame_url"):
                    lf = ws_path(args, "frames", f"{item['id']}-last.png")
                    http.download(r["last_frame_url"], lf)
                    extra["last_frame"] = lf
                strip = media.strip_clip(path, ws_path(args, "sheets", f"{item['id']}-strip.png"), item["id"])  # label by ID only, so drafts from different providers are judged blind
                led.update(item["id"], status="succeeded", file=path, strip=strip, usage=r.get("usage"), **extra)
                print(f"{item['id']} {item['shot']} ({name}): {path}  review: {strip}")
            elif r["status"] == "failed":
                led.update(item["id"], status="failed", note=json.dumps(r.get("error") or r.get("raw_status"))[:300])
                print(f"{item['id']} {item['shot']} ({name}): failed {r.get('error') or ''}")
        remaining = led.find(type="clip", status="submitted")
        if not args.wait or not remaining or time.time() > deadline:
            print(f"{len(remaining)} clip(s) still running.")
            return
        time.sleep(cfg["poll_seconds"])


def cmd_palette(args):
    brief, shots, led, cfg = load(args)
    path = led.get(args.target)["file"] if args.target.startswith(("O-", "A-")) else args.target
    report = media.palette_report(path, brief["tokens"]["palette"], tolerance=args.tolerance)
    if args.target.startswith(("O-", "A-")):
        led.update(args.target, palette=report)
    print(json.dumps(report, indent=2))


def cmd_assemble(args):
    brief, shots, led, cfg = load(args)
    film = shots.get("film", {})
    clips, used = [], []
    for s in shots["shots"]:
        c = picked(led, s["id"], "clip")
        if not c:
            raise SystemExit(f"{s['id']} has no picked clip. Review the strips and `fmotion pick` one.")
        clips.append((c["file"], float(s["seconds"])))
        used.append(c["id"])
    w, h = (int(x) for x in film.get("size", "1920x1080").split("x"))
    aid = led.new("A", type="cut", shot="film", options=used, status="rendering")
    out = ws_path(args, "out", f"{aid}.mp4")
    media.assemble(clips, out, w, h, int(film.get("fps", 24)), music=args.music)
    led.update(aid, status="rendered", file=out)
    print(f"{aid}: {out}. Run `fmotion check {aid}` before anyone sees it.")


def cmd_check(args):
    led = ledger.Ledger(args.dir)
    path = led.get(args.target)["file"] if args.target.startswith("A-") else args.target
    result = {"flash": media.flash_check(path), "loudness": media.loudness(path), "format": media.probe(path)}
    if args.target.startswith("A-"):
        led.update(args.target, checks=result)
    print(json.dumps(result, indent=2))
    if not result["flash"]["passes"]:
        sys.exit(1)


def cmd_cost(args):
    led = ledger.Ledger(args.dir)
    cfg = config.load(args.dir)
    rates = cfg.get("rates", {})
    stills = [i for i in led.find(type="still") if i.get("status") == "generated"]
    clips = [i for i in led.find(type="clip") if i.get("status") in ("succeeded", "submitted")]
    by_q = {}
    for s in stills:
        by_q[s.get("quality")] = by_q.get(s.get("quality"), 0) + 1
    by_r = {}
    for c in clips:
        key_ = f"{c.get('provider', 'seedance')}_{c.get('resolution')}"
        by_r[key_] = by_r.get(key_, 0) + float(c.get("seconds", 0))
    est = sum(n * rates.get(f"image_{q}", 0) for q, n in by_q.items()) + \
        sum(sec * rates.get(f"{r}_per_second", 0) for r, sec in by_r.items())
    print(json.dumps({"stills_by_quality": by_q, "video_seconds_by_provider_and_tier": by_r,
                      "estimate": round(est, 2) if rates else "set rates in motion/config.json to price this"}, indent=2))


def main(argv=None):
    p = argparse.ArgumentParser(prog="fmotion", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--dir", default="motion", help="workspace folder (default: ./motion)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("validate")
    f = sub.add_parser("frames"); f.add_argument("--shots"); f.add_argument("--final", action="store_true"); f.add_argument("--dry-run", action="store_true")
    e = sub.add_parser("edit"); e.add_argument("option"); e.add_argument("instruction"); e.add_argument("--final", action="store_true"); e.add_argument("--dry-run", action="store_true")
    k = sub.add_parser("pick"); k.add_argument("option"); k.add_argument("--reason")
    a = sub.add_parser("animate"); a.add_argument("--shots"); a.add_argument("--provider", help="seedance, kling, or both: seedance,kling"); a.add_argument("--draft", action="store_true"); a.add_argument("--seed", type=int); a.add_argument("--dry-run", action="store_true")
    s = sub.add_parser("status"); s.add_argument("--wait", action="store_true")
    pl = sub.add_parser("palette"); pl.add_argument("target"); pl.add_argument("--tolerance", type=float, default=14.0)
    asm = sub.add_parser("assemble"); asm.add_argument("--music")
    c = sub.add_parser("check"); c.add_argument("target")
    sub.add_parser("cost")
    args = p.parse_args(argv)
    if args.cmd != "init" and not os.path.isdir(args.dir):
        raise SystemExit(f"No workspace at {args.dir}. Run `fmotion init` first.")
    globals()[f"cmd_{args.cmd}"](args)


if __name__ == "__main__":
    main()
