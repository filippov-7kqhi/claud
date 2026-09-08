import sys, os; sys.path.insert(0, '/home/user/claud/tools')
from build_site import write_site
from products import for_store
import cfg_branchforge, cfg_haulcrest

ROOT = '/home/user/claud/sites'
for mod, prefix in ((cfg_branchforge, 'BF'), (cfg_haulcrest, 'HC')):
    cfg = dict(mod.CFG)
    cfg['products'] = for_store(cfg['brand'], prefix)
    key = cfg['domain'].split('.')[0]
    pages = write_site(cfg, f'{ROOT}/{key}')
    print(f"{cfg['brand']}: {len(pages)} pages, {len(cfg['products'])} products -> {ROOT}/{key}")
