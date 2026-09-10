# -*- coding: utf-8 -*-
"""Copy a built store into its GitHub Pages repository working tree.

Two things this does that a plain `cp -r` does not:

  * It leaves alone anything the repository holds that the generator does not
    own -- the README, and the Cloudflare Worker source under stripe/. A
    wholesale replace would silently delete them.
  * It ships only the image galleries a product actually references. Both
    original stores sell photographed machines, so the generated catalogue art
    sitting in their build directory is several megabytes of dead weight.

It does not commit or push; run git yourself once you have read the diff.
"""
import argparse, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from products import for_store
import cfg_branchforge, cfg_haulcrest, cfg_rootvexx, cfg_lawnstride

SITES = os.path.join(REPO, "sites")
STORES = {"branchforge": (cfg_branchforge, "BF"), "haulcrest": (cfg_haulcrest, "HC"),
          "rootvexx": (cfg_rootvexx, "RV"), "lawnstride": (cfg_lawnstride, "LS")}

# top-level names in the repo that are not ours to replace or remove
KEEP = {".git", ".github", "README.md", "LICENSE", "stripe"}


def wanted_galleries(key):
    mod, prefix = STORES[key]
    return {p["dir"].split("/")[-1]
            for p in for_store(mod.CFG["brand"], prefix, key, f"{SITES}/{key}")}


def deploy(key, dest):
    src, keep = f"{SITES}/{key}", wanted_galleries(key)
    for name in os.listdir(dest):
        if name not in KEEP:
            path = f"{dest}/{name}"
            shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)

    copied = 0
    for root, dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        parts = rel.split(os.sep)
        # assets/img/<gallery>: skip a gallery no product on this store references
        if len(parts) >= 3 and parts[0] == "assets" and parts[1] == "img" and parts[2] not in keep:
            dirs[:] = []
            continue
        out = dest if rel == "." else f"{dest}/{rel}"
        os.makedirs(out, exist_ok=True)
        for f in files:
            shutil.copy2(f"{root}/{f}", f"{out}/{f}")
            copied += 1

    open(f"{dest}/.nojekyll", "w").close()      # the site is already built
    return copied, sorted(keep)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("store", nargs="*", choices=sorted(STORES) + [[]],
                    help="stores to deploy; default all four")
    ap.add_argument("--repos", default=os.path.dirname(REPO), metavar="DIR",
                    help="directory holding the four store clones "
                         "(default: the directory this repo sits in)")
    args = ap.parse_args()

    for key in (args.store or sorted(STORES)):
        dest = os.path.join(args.repos, key)
        if not os.path.isdir(os.path.join(dest, ".git")):
            raise SystemExit(f"{dest} is not a git clone. Clone filippov-7kqhi/{key} "
                             f"there, or pass --repos.")
        n, gal = deploy(key, dest)
        print(f"{key}: {n} files -> {dest}, galleries {', '.join(gal)}")
