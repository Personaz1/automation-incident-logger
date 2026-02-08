#!/usr/bin/env python3
import argparse, json, pathlib, datetime

DB = pathlib.Path("data/incidents.jsonl")


def append_incident(title, severity, summary):
    DB.parent.mkdir(parents=True, exist_ok=True)
    item = {
        "id": f"inc-{int(datetime.datetime.utcnow().timestamp())}",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "title": title,
        "severity": severity,
        "summary": summary,
        "status": "open",
    }
    with DB.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print("Created", item["id"])


def load_all():
    if not DB.exists():
        return []
    out = []
    for line in DB.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def list_incidents():
    items = load_all()
    if not items:
        print("No incidents")
        return
    for it in items:
        print(f"{it['id']} | {it['severity']} | {it['status']} | {it['title']}")


def summary():
    items = load_all()
    by = {}
    for it in items:
        by[it["severity"]] = by.get(it["severity"], 0) + 1
    print("Total:", len(items))
    for k in sorted(by):
        print(f"- {k}: {by[k]}")


def main():
    ap=argparse.ArgumentParser(prog="ailog")
    sub=ap.add_subparsers(dest="cmd", required=True)
    c=sub.add_parser("create")
    c.add_argument("--title", required=True)
    c.add_argument("--severity", choices=["low","med","high"], default="med")
    c.add_argument("--summary", required=True)
    sub.add_parser("list")
    sub.add_parser("summary")
    args=ap.parse_args()

    if args.cmd=="create":
        append_incident(args.title, args.severity, args.summary)
    elif args.cmd=="list":
        list_incidents()
    elif args.cmd=="summary":
        summary()

if __name__ == "__main__":
    main()
