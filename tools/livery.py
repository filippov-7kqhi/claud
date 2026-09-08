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

ALL = [BRANCHFORGE, HAULCREST]

# The module-level livery the machine drawings read while rendering.
CUR = BRANCHFORGE


def use(l):
    global CUR
    CUR = l
    return l
