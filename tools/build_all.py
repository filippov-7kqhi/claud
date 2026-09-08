import sys, os; sys.path.insert(0, '/home/user/claud/tools')
from build_site import write_site
from products import for_store
import cfg_branchforge, cfg_haulcrest
import hashlib


def digest(path):
    """Short content hash so a changed asset gets a new URL and can never be served stale."""
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:10]

ROOT = '/home/user/claud/sites'
for mod, prefix in ((cfg_branchforge, 'BF'), (cfg_haulcrest, 'HC')):
    cfg = dict(mod.CFG)
    cfg['products'] = for_store(cfg['brand'], prefix)
    key = cfg['domain'].split('.')[0]
    cfg['ver_css'] = digest(f'{ROOT}/{key}/assets/css/style.css')
    cfg['ver_js'] = digest(f'{ROOT}/{key}/assets/js/script.js')
    pages = write_site(cfg, f'{ROOT}/{key}')
    print(f"{cfg['brand']}: {len(pages)} pages, {len(cfg['products'])} products "
          f"| css v{cfg['ver_css']} js v{cfg['ver_js']}")
