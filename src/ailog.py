#!/usr/bin/env python3
import argparse, json, pathlib, datetime

DB = pathlib.Path("data/incidents.jsonl")


def append_line(item):
    DB.parent.mkdir(parents=True, exist_ok=True)
    with DB.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def load_all():
    if not DB.exists():
        return []
    out = []
    for line in DB.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def save_all(items):
    DB.parent.mkdir(parents=True, exist_ok=True)
    DB.write_text("\n".join(json.dumps(i, ensure_ascii=False) for i in items) + ("\n" if items else ""), encoding="utf-8")


def create_incident(title, severity, summary):
    item = {
        "id": f"inc-{int(datetime.datetime.utcnow().timestamp())}",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "title": title,
        "severity": severity,
        "summary": summary,
        "status": "open",
    }
    append_line(item)
    print("Created", item["id"])


def set_status(incident_id, status):
    items = load_all()
    changed = False
    for it in items:
        if it["id"] == incident_id:
            it["status"] = status
            it["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
            changed = True
            break
    if changed:
        save_all(items)
        print(f"Updated {incident_id} -> {status}")
    else:
        print("Incident not found")


def list_incidents(severity=None, status=None):
    items = load_all()
    if severity:
        items = [i for i in items if i.get("severity") == severity]
    if status:
        items = [i for i in items if i.get("status") == status]
    if not items:
        print("No incidents")
        return
    for it in items:
        print(f"{it['id']} | {it['severity']} | {it['status']} | {it['title']}")


def summary_md(out='weekly-summary.md'):
    items = load_all()
    by_sev = {}
    by_status = {}
    for it in items:
        by_sev[it['severity']] = by_sev.get(it['severity'], 0) + 1
        by_status[it['status']] = by_status.get(it['status'], 0) + 1

    lines = [
        '# Weekly Incident Summary',
        '',
        f"Generated: {datetime.datetime.utcnow().isoformat()}Z",
        '',
        f"Total incidents: **{len(items)}**",
        '',
        '## By severity'
    ]
    for k in sorted(by_sev):
        lines.append(f"- {k}: {by_sev[k]}")
    lines += ['', '## By status']
    for k in sorted(by_status):
        lines.append(f"- {k}: {by_status[k]}")

    pathlib.Path(out).write_text('\n'.join(lines), encoding='utf-8')
    print('Saved', out)


def main():
    ap=argparse.ArgumentParser(prog="ailog")
    sub=ap.add_subparsers(dest="cmd", required=True)

    c=sub.add_parser("create")
    c.add_argument("--title", required=True)
    c.add_argument("--severity", choices=["low","med","high"], default="med")
    c.add_argument("--summary", required=True)

    l=sub.add_parser("list")
    l.add_argument("--severity", choices=["low","med","high"])
    l.add_argument("--status", choices=["open","closed"])

    cl=sub.add_parser("close")
    cl.add_argument("--id", required=True)

    ro=sub.add_parser("reopen")
    ro.add_argument("--id", required=True)

    s=sub.add_parser("summary")
    s.add_argument("--out", default="weekly-summary.md")

    args=ap.parse_args()

    if args.cmd=="create":
        create_incident(args.title, args.severity, args.summary)
    elif args.cmd=="list":
        list_incidents(args.severity, args.status)
    elif args.cmd=="close":
        set_status(args.id, "closed")
    elif args.cmd=="reopen":
        set_status(args.id, "open")
    elif args.cmd=="summary":
        summary_md(args.out)

if __name__ == "__main__":
    main()
