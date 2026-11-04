"""Option ledger for generated work, compatible with Fastidious's option-ledger IDs.

Every generated still or clip is an option (O-), every pick is a decision (D-), every delivered cut is an
output (A-). IDs are permanent and never reused, so "animate O-014" or "rebuild A-302" always means the same
thing. The ledger is written as JSON (for the CLI) and as LEDGER.md (for people).
"""
import json
import os
import time


class Ledger:
    def __init__(self, workspace):
        self.path = os.path.join(workspace, "ledger.json")
        self.md = os.path.join(workspace, "LEDGER.md")
        if os.path.exists(self.path):
            with open(self.path) as f:
                self.data = json.load(f)
        else:
            self.data = {"next": {"O": 1, "D": 1, "A": 1}, "items": {}}

    def new(self, kind, **fields):
        n = self.data["next"][kind]
        self.data["next"][kind] = n + 1
        iid = f"{kind}-{n:03d}"
        fields.update(id=iid, kind=kind, created=time.strftime("%Y-%m-%d %H:%M"))
        self.data["items"][iid] = fields
        self.save()
        return iid

    def get(self, iid):
        if iid not in self.data["items"]:
            raise SystemExit(f"{iid} is not in the ledger.")
        return self.data["items"][iid]

    def update(self, iid, **fields):
        self.get(iid).update(fields)
        self.save()

    def find(self, **match):
        return [v for v in self.data["items"].values() if all(v.get(k) == m for k, m in match.items())]

    def save(self):
        tmp = self.path + ".part"
        with open(tmp, "w") as f:
            json.dump(self.data, f, indent=2)
        os.replace(tmp, self.path)
        rows = ["# Motion ledger", "", "| ID | Shot | Type | Status | File | Note |", "|---|---|---|---|---|---|"]
        for v in self.data["items"].values():
            note = (v.get("note") or v.get("reason") or "").replace("|", "/")
            rows.append(f"| {v['id']} | {v.get('shot', '')} | {v.get('type', v['kind'])} | {v.get('status', '')} | "
                        f"{v.get('file', '')} | {note} |")
        with open(self.md, "w") as f:
            f.write("\n".join(rows) + "\n")
