"""Per-store livery. Every machine can be painted in either brand's colours."""

BRANCHFORGE = dict(
    key="branchforge", brand="BRANCHFORGE", site="branchforge.shop",
    g1="#2f7d4f", g2="#1f5c39", g3="#123726",
    edge="#0c2418", mid="#164a2f", rec="#0f3325", rec2="#0b2a1a", lite="#1a5537",
    ink="#ffffff", sub="#a3e635", acc="#a3e635", hi="#7fe043", warm="#f97316",
    glow="#a3e635",
)

HAULCREST = dict(
    key="haulcrest", brand="HAULCREST", site="haulcrest.shop",
    g1="#fbbf24", g2="#f59e0b", g3="#b45309",
    edge="#7c4a09", mid="#d97706", rec="#b45309", rec2="#92400e", lite="#f59e0b",
    ink="#1a1206", sub="#4a3410", acc="#f59e0b", hi="#fcd34d", warm="#f97316",
    glow="#f59e0b",
)

ROOTVEXX = dict(key="rootvexx", brand="ROOTVEXX", site="rootvexx.shop", studio="light",
    g1="#fb923c", g2="#ea580c", g3="#9a3412", edge="#7c2d12", mid="#c2410c",
    rec="#9a3412", rec2="#7c2d12", lite="#ea580c",
    ink="#ffffff", sub="#fed7aa", acc="#f97316", hi="#fdba74", warm="#f97316", glow="#f97316")

LAWNSTRIDE = dict(key="lawnstride", brand="LAWNSTRIDE", site="lawnstride.shop", studio="light",
    g1="#84cc16", g2="#65a30d", g3="#3f6212", edge="#274e13", mid="#4d7c0f",
    rec="#3f6212", rec2="#274e13", lite="#65a30d",
    ink="#ffffff", sub="#e4f7bd", acc="#65a30d", hi="#a3e635", warm="#f97316", glow="#65a30d")

ALL = [BRANCHFORGE, HAULCREST, ROOTVEXX, LAWNSTRIDE]

# The module-level livery the machine drawings read while rendering.
CUR = BRANCHFORGE


def use(l):
    global CUR
    CUR = l
    return l
