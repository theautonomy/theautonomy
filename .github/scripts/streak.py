"""Rewrite the streak block in README.md from the GitHub contribution calendar."""
import datetime as dt
import json
import os
import re
import urllib.request

USER = os.environ.get("GH_USER", "theautonomy")
TOKEN = os.environ["GITHUB_TOKEN"]


def gql(query, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        body = json.load(r)
    if "errors" in body:
        raise SystemExit(body["errors"])
    return body["data"]


today = dt.datetime.now(dt.timezone.utc).date()

years = gql(
    "query($u:String!){user(login:$u){contributionsCollection{contributionYears}}}", u=USER
)["user"]["contributionsCollection"]["contributionYears"]

days = {}
for year in years:
    cal = gql(
        """query($u:String!,$f:DateTime!,$t:DateTime!){user(login:$u){
             contributionsCollection(from:$f,to:$t){contributionCalendar{
               weeks{contributionDays{date contributionCount}}}}}}""",
        u=USER, f=f"{year}-01-01T00:00:00Z", t=f"{year}-12-31T23:59:59Z",
    )["user"]["contributionsCollection"]["contributionCalendar"]
    for week in cal["weeks"]:
        for d in week["contributionDays"]:
            days[dt.date.fromisoformat(d["date"])] = d["contributionCount"]

dates = sorted(d for d in days if d <= today)
total = sum(days[d] for d in dates)
first = next((d for d in dates if days[d]), today)
year_dates = [d for d in dates if d.year == today.year]
year_total = sum(days[d] for d in year_dates)

# longest run of consecutive active days this year
longest, run_start, best = 0, None, (None, None)
for d in year_dates:
    if days[d]:
        run_start = run_start or d
        if (d - run_start).days + 1 > longest:
            longest, best = (d - run_start).days + 1, (run_start, d)
    else:
        run_start = None

# current streak: today doesn't break it if there's nothing yet
cur_end = today if days.get(today) else today - dt.timedelta(days=1)
cur_start = cur_end
while days.get(cur_start - dt.timedelta(days=1)):
    cur_start -= dt.timedelta(days=1)
current = (cur_end - cur_start).days + 1 if days.get(cur_end) else 0


def fmt(d):
    return f"{d:%b} {d.day}, {d.year}"


def span(a, b):
    return f"{fmt(a)} - {fmt(b)}" if a else "-"


def n_days(n):
    return f"{n} day" + ("" if n == 1 else "s")


block = f"""<!-- streak:start -->
```console
wei@github:~$ ./streak.sh

  contributions        {year_total:<10,}  in {today.year}
  total contributions  {total:<10,}  {fmt(first)} - present
  current streak       {n_days(current):<10}  {span(cur_start, cur_end) if current else "-"}
  longest streak       {n_days(longest):<10}  {span(*best)}

  last updated {today.isoformat()} UTC
```
<!-- streak:end -->"""

with open("README.md", encoding="utf-8") as f:
    readme = f.read()
readme = re.sub(r"<!-- streak:start -->.*?<!-- streak:end -->", lambda _: block, readme, flags=re.S)
with open("README.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(readme)
print(block)
