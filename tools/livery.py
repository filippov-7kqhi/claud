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

ROOTVEXX = dict(
    key="rootvexx", brand="ROOTVEXX", site="rootvexx.shop",
    g1="#ef4444", g2="#dc2626", g3="#991b1b",
    edge="#6b1414", mid="#b91c1c", rec="#991b1b", rec2="#7f1d1d", lite="#dc2626",
    ink="#ffffff", sub="#fecaca", acc="#ef4444", hi="#fca5a5", warm="#f97316",
    glow="#ef4444",
)

LAWNSTRIDE = dict(
    key="lawnstride", brand="LAWNSTRIDE", site="lawnstride.shop",
    g1="#2dd4bf", g2="#14b8a6", g3="#0f766e",
    edge="#083c37", mid="#0d9488", rec="#115e59", rec2="#0b3b36", lite="#14b8a6",
    ink="#04211f", sub="#0b3b36", acc="#14b8a6", hi="#5eead4", warm="#f97316",
    glow="#14b8a6",
)

ALL = [BRANCHFORGE, HAULCREST, ROOTVEXX, LAWNSTRIDE]

# The module-level livery the machine drawings read while rendering.
CUR = BRANCHFORGE


def use(l):
    global CUR
    CUR = l
    return l
