##### Module which retrieved subordinated interrogatives

from .coveney import p,w, subordinated1, subordinated2, ch
V = "V"

EMBD1 = [
    (p, ch(V) + subordinated1(V))
]
EMBD2 = [
    (p, ch(V) + subordinated2(V))
]

EMBEDDED_REQS = {
    "embd" : [EMBD1, EMBD2]
}