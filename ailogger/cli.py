import argparse, json, pathlib, datetime, uuid
DB = pathlib.Path("data/incidents.jsonl")


def load_all():
    if not DB.exists(): return []
    return [json.loads(x) for x in DB.read_text(encoding="utf-8").splitlines() if x.strip()]


def save_all(items):
    DB.parent.mkdir(parents=True, exist_ok=True)
    DB.write_text("\n".join(json.dumps(i, ensure_ascii=False) for i in items) + ("\n" if items else ""), encoding="utf-8")


def create(title, severity, summary):
    items=load_all()
    it={"id":f"inc-{uuid.uuid4().hex[:10]}","created_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"title":title,"severity":severity,"summary":summary,"status":"open"}
    items.append(it); save_all(items); print(it["id"])


def set_status(iid, st):
    items=load_all(); ok=False
    for it in items:
        if it["id"]==iid: it["status"]=st; ok=True
    save_all(items)
    print("updated" if ok else "not-found")


def ls(sev=None, st=None):
    items=load_all()
    if sev: items=[i for i in items if i["severity"]==sev]
    if st: items=[i for i in items if i["status"]==st]
    for i in items: print(f"{i['id']} | {i['severity']} | {i['status']} | {i['title']}")


def summary(out):
    items=load_all(); by={}
    for i in items: by[i['severity']]=by.get(i['severity'],0)+1
    lines=["# Weekly Incident Summary", "", f"Total: {len(items)}"] + [f"- {k}: {by[k]}" for k in sorted(by)]
    pathlib.Path(out).write_text("\n".join(lines), encoding="utf-8")
    print(out)


def main():
    ap=argparse.ArgumentParser(prog="ailogger")
    sub=ap.add_subparsers(dest="cmd", required=True)
    c=sub.add_parser("create"); c.add_argument("--title",required=True); c.add_argument("--severity",choices=["low","med","high"],default="med"); c.add_argument("--summary",required=True)
    l=sub.add_parser("list"); l.add_argument("--severity",choices=["low","med","high"]); l.add_argument("--status",choices=["open","closed"])
    cl=sub.add_parser("close"); cl.add_argument("--id",required=True)
    ro=sub.add_parser("reopen"); ro.add_argument("--id",required=True)
    s=sub.add_parser("summary"); s.add_argument("--out",default="weekly-summary.md")
    a=ap.parse_args()
    if a.cmd=="create": create(a.title,a.severity,a.summary)
    elif a.cmd=="list": ls(a.severity,a.status)
    elif a.cmd=="close": set_status(a.id,"closed")
    elif a.cmd=="reopen": set_status(a.id,"open")
    elif a.cmd=="summary": summary(a.out)

if __name__ == "__main__":
    main()
