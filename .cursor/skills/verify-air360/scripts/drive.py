"""Drive Air360 in headless Chromium, one step per argument, and write evidence.

Run through drive.sh so the venv's Python (with Playwright) is used:

  drive.sh --run RUN_ID --name NAME [--viewport 1280x800] [--profile NAME] STEP [STEP ...]

Each STEP is one shell-quoted string, for example "click button 'Import Photos'".
Evidence lands in .verify-evidence/air360/RUN_ID/NAME/. The run stops at the first
failing step, saves failure.png and failure.aria.yml, and exits 1.

Steps:
  goto PATH                      open URL + PATH (PATH starts with /)
  reload                         reload the page (IndexedDB survives)
  import FILE [FILE ...]         choose the "Import Photos" button and pick FILEs in the
                                 file chooser. Bare names resolve to the run's fixtures dir.
  click ROLE NAME                click by ARIA role and exact accessible name
  click-text TEXT                click the first visible element containing TEXT
  click-css SELECTOR             last resort, for controls with no accessible name
  card FILENAME ROLE NAME        click a control inside the photo card that shows FILENAME
  click-at X Y                   mouse click at viewport coordinates, e.g. a backdrop corner
  drag SELECTOR DX DY            mouse-drag from the element's center by DX,DY pixels
  fill ROLE NAME VALUE           type VALUE into the field with that role and name
  press KEY                      keyboard press on the page, e.g. Escape
  dialogs accept|dismiss         answer later confirm() dialogs (default: dismiss)
  expect ROLE NAME               that control is visible
  expect-text TEXT               some visible element contains TEXT
  expect-no-text TEXT            no visible element contains TEXT
  expect-count-text TEXT N       exactly N visible elements contain TEXT
  expect-css SELECTOR            the element is visible and has a non-zero size
  expect-redraw SELECTOR MS      the element's pixels differ between now and MS later
  expect-url TEXT                the page URL contains TEXT
  idb                            dump the air360-db-v3 "photos" store to idb-<n>.json (read-only)
  idb-count N                    the store holds exactly N records
  screenshot NAME                viewport screenshot to NAME.png, CSS transitions finished first
  aria NAME                      ARIA snapshot of <body> to NAME.aria.yml
  sleep MS                       fixed wait; only for animations with no observable end state
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

SKILL_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_DIR.parent.parent.parent
STATE_ROOT = Path(os.environ.get("VERIFY_AIR360_STATE", os.path.join(os.environ.get("TMPDIR", "/tmp"), "verify-air360")))
EVIDENCE_ROOT = REPO_ROOT / ".verify-evidence" / "air360"

IDB_DUMP_JS = """
async () => {
  // Never open a database that does not exist yet: indexedDB.open would create it
  // without the 'photos' store and break the app's own upgrade path.
  const dbs = await indexedDB.databases();
  if (!dbs.some(d => d.name === 'air360-db-v3')) return {exists: false, records: []};
  const db = await new Promise((res, rej) => {
    const r = indexedDB.open('air360-db-v3');
    r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error);
  });
  if (!db.objectStoreNames.contains('photos')) { db.close(); return {exists: true, records: []}; }
  const rows = await new Promise((res, rej) => {
    const r = db.transaction('photos', 'readonly').objectStore('photos').getAll();
    r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error);
  });
  db.close();
  return {exists: true, records: rows.map(p => ({
    name: p.name, width: p.width, height: p.height, aspectRatio: p.aspectRatio,
    is360: p.is360, captureDate: p.captureDate, cameraMake: p.cameraMake,
    imageBlobBytes: p.imageBlob ? p.imageBlob.size : 0,
  }))};
}
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", default=os.environ.get("VERIFY_AIR360_RUN"), help="run id printed by start.sh")
    ap.add_argument("--name", required=True, help="evidence subdirectory, e.g. import-photos")
    ap.add_argument("--viewport", default="1280x800", help="WxH; below 640 wide the header hides 'Waypoint Aerial' and the storage pill")
    ap.add_argument("--profile", help="reuse a browser profile (IndexedDB) across drive.sh calls in this run")
    ap.add_argument("steps", nargs="+")
    args = ap.parse_args()
    if not args.run:
        sys.exit("error: pass --run or set VERIFY_AIR360_RUN")

    state = STATE_ROOT / args.run
    if not (state / "url").exists():
        sys.exit(f"error: {state}/url missing. Did start.sh run for {args.run}?")
    base_url = (state / "url").read_text().strip()
    fixtures = state / "fixtures"
    out = EVIDENCE_ROOT / args.run / args.name
    out.mkdir(parents=True, exist_ok=True)
    width, height = (int(v) for v in args.viewport.split("x"))

    log = open(out / "steps.log", "a")
    console = open(out / "console.log", "a")
    network = open(out / "network.log", "a")

    def note(line):
        print(line)
        log.write(line + "\n")
        log.flush()

    rev = subprocess.run(["git", "-C", str(REPO_ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", str(REPO_ROOT), "status", "--porcelain", "--", "index.html", "manifest.json"], capture_output=True, text=True).stdout.strip()
    note(f"# run={args.run} name={args.name} url={base_url} rev={rev}{' (site files modified)' if dirty else ''} viewport={args.viewport} profile={args.profile or '-'}")

    dialog_mode = {"value": "dismiss"}
    idb_counter = {"n": 0}

    with sync_playwright() as pw:
        launch_args = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"]  # WebGL for Pannellum
        ctx_opts = dict(viewport={"width": width, "height": height}, locale="en-US", timezone_id="America/New_York")
        if args.profile:
            ctx = pw.chromium.launch_persistent_context(str(state / "profiles" / args.profile), headless=True, args=launch_args, **ctx_opts)
            browser = None
        else:
            browser = pw.chromium.launch(headless=True, args=launch_args)
            ctx = browser.new_context(**ctx_opts)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        expect.set_options(timeout=10_000)

        page.on("console", lambda m: console.write(f"[{m.type}] {m.text}\n") or console.flush())
        page.on("pageerror", lambda e: console.write(f"[pageerror] {e}\n") or console.flush())
        page.on("requestfailed", lambda r: network.write(f"FAILED {r.method} {r.url} {r.failure}\n") or network.flush())
        page.on("response", lambda r: r.status >= 400 and (network.write(f"HTTP {r.status} {r.url}\n") or network.flush()))

        def on_dialog(d):
            note(f"  dialog {d.type} {d.message!r} -> {dialog_mode['value']}")
            d.accept() if dialog_mode["value"] == "accept" else d.dismiss()

        page.on("dialog", on_dialog)

        def fixture(p):
            path = Path(p)
            return str(path if path.is_absolute() or "/" in p else fixtures / p)

        def visible_text(t):
            return page.get_by_text(t).filter(visible=True)

        def run_step(words):
            cmd, rest = words[0], words[1:]
            if cmd == "goto":
                page.goto(base_url + rest[0], wait_until="load")
            elif cmd == "reload":
                page.reload(wait_until="load")
            elif cmd == "import":
                with page.expect_file_chooser() as fc:
                    page.get_by_role("button", name="Import Photos", exact=True).click()
                fc.value.set_files([fixture(p) for p in rest])
            elif cmd == "click":
                page.get_by_role(rest[0], name=rest[1], exact=True).click()
            elif cmd == "click-text":
                visible_text(rest[0]).first.click()
            elif cmd == "click-css":
                page.locator(rest[0]).click()
            elif cmd == "card":
                page.locator(".photo-card").filter(has_text=rest[0]).get_by_role(rest[1], name=rest[2], exact=True).click()
            elif cmd == "click-at":
                page.mouse.click(int(rest[0]), int(rest[1]))
            elif cmd == "drag":
                box = page.locator(rest[0]).bounding_box()
                x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
                page.mouse.move(x, y)
                page.mouse.down()
                page.mouse.move(x + int(rest[1]), y + int(rest[2]), steps=15)
                page.mouse.up()
            elif cmd == "fill":
                page.get_by_role(rest[0], name=rest[1], exact=True).fill(rest[2])
            elif cmd == "press":
                page.keyboard.press(rest[0])
            elif cmd == "dialogs":
                dialog_mode["value"] = rest[0]
            elif cmd == "expect":
                expect(page.get_by_role(rest[0], name=rest[1], exact=True)).to_be_visible()
            elif cmd == "expect-text":
                expect(visible_text(rest[0]).first).to_be_visible()
            elif cmd == "expect-no-text":
                expect(visible_text(rest[0])).to_have_count(0)
            elif cmd == "expect-count-text":
                expect(visible_text(rest[0])).to_have_count(int(rest[1]))
            elif cmd == "expect-css":
                loc = page.locator(rest[0]).first
                expect(loc).to_be_visible()
                box = loc.bounding_box()
                if not box or box["width"] < 1 or box["height"] < 1:
                    raise AssertionError(f"{rest[0]} is visible but sized {box}")
            elif cmd == "expect-redraw":
                loc = page.locator(rest[0]).first
                before = loc.screenshot()
                page.wait_for_timeout(int(rest[1]))
                if loc.screenshot() == before:
                    raise AssertionError(f"{rest[0]} did not change in {rest[1]} ms")
            elif cmd == "expect-url":
                expect(page).to_have_url(re.compile(re.escape(rest[0])))
            elif cmd in ("idb", "idb-count"):
                data = page.evaluate(IDB_DUMP_JS)
                idb_counter["n"] += 1
                path = out / f"idb-{idb_counter['n']}.json"
                path.write_text(json.dumps(data, indent=2))
                note(f"  idb: {len(data['records'])} record(s) -> {path.name}")
                if cmd == "idb-count" and len(data["records"]) != int(rest[0]):
                    raise AssertionError(f"expected {rest[0]} IndexedDB records, found {len(data['records'])}")
            elif cmd == "screenshot":
                # animations="disabled" finishes CSS transitions (the toggle fades for 150 ms) before capture.
                page.screenshot(path=str(out / f"{rest[0]}.png"), animations="disabled")
            elif cmd == "aria":
                (out / f"{rest[0]}.aria.yml").write_text(page.locator("body").aria_snapshot() + "\n")
            elif cmd == "sleep":
                page.wait_for_timeout(int(rest[0]))
            else:
                raise ValueError(f"unknown step {cmd!r}; see drive.sh --help")

        status = 0
        for raw in args.steps:
            words = shlex.split(raw)
            t0 = time.monotonic()
            try:
                run_step(words)
                note(f"ok   {raw}  ({int((time.monotonic() - t0) * 1000)} ms)")
            except Exception as e:  # report the step, keep the evidence, stop the run
                note(f"FAIL {raw}  ({int((time.monotonic() - t0) * 1000)} ms)\n  {type(e).__name__}: {str(e).splitlines()[0] if str(e) else ''}")
                try:
                    page.screenshot(path=str(out / "failure.png"))
                    (out / "failure.aria.yml").write_text(page.locator("body").aria_snapshot() + "\n")
                except Exception:
                    pass
                status = 1
                break
        ctx.close()
        if browser:
            browser.close()
    note(f"# result={'PASS' if status == 0 else 'FAIL'} evidence={out}")
    sys.exit(status)


if __name__ == "__main__":
    main()
