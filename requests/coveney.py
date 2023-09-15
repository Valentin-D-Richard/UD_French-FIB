##### Category requests for coveney annotation scheme



##### String variables
V = "V" # main verb
Q = "Q" # qu-word
S = "S" # subject
E = "E" # 'est-ce que'
CL = "CL" # clitic subject marker
GN = "GN" # nominal subject
CH = "CH" # UD clause head (if different from V)
K = "K" # 'que'
SI = 'si'
W = "*" # wildcard
p = "pattern"
w = "without"


#### Regularly occurring strings
def ecq_marker(head:str, marker:str) -> str:
    req = head+' -[cue:mark]-> '+marker+' ; '
    return req+marker+'[lemma="être"] ;\n'

def has_ecq_marker(head:str) -> str:
    return ecq_marker(head,E)

def cl_marker(head:str, subject:str) -> str:
    req = head+' -[cue:mark]-> '+subject+' ;\n'
    req += head+' -[expl:nsubj|nsubj|nsubj:pass]-> '+subject+' ; '
    return req+subject+'[upos="PRON"] ;\n'

def has_cl_marker(head:str) -> str:
    return cl_marker(head, CL)

def que_marker(head:str, marker:str) -> str:
    req = head+' -[cue:mark]-> '+marker+' ; '
    return req+marker+'[lemma="que"] ;\n'

def ch(head:str) -> str: # is_clause_head
    return head+'[ClauseType="Int"] ;\n'

def is_qu_word(head:str) -> str:
    return head+'[PronType="Int"] ;\n'

def qu_word(head:str, qu:str) -> str:
    return head+' -[cue:wh]-> '+qu+' ;\n'

def copaux(head:str, copaux:str) -> str:
    return head+' -[1=cop|aux]-> '+copaux+' ;\n'

def precedes(first:str, second:str) -> str:
    return first+' << '+second+' ;\n'

def prec_subj(head:str, subject:str) -> str:
    req = head+' -[expl:nsubj|nsubj|nsubj:pass|csubj]-> '+subject
    return req+precedes(subject,head)

def prec_gn(head:str, subject:str) -> str:
    req = head+' -[nsubj|nsubj:pass]-> '+subject
    return req+precedes(subject,head)

def suc_gn(head:str, subject:str) -> str:
    req = head+' -[nsubj|nsubj:pass]-> '+subject
    return req+precedes(head,subject)




##### Request descriptions

# Version 1 with V as main verb
# Version 2 with V auxiliary or copula
# Version 3 Q is UD clause head and V as auxiliary or copula

### yes-no

ESV1 = [
    (p, ch(V) + has_ecq_marker(V) + prec_subj(V,S)),
    (w, copaux(V,W)),
    (w, qu_word(V,Q)),
    (w, is_qu_word(V)),
    (w, has_cl_marker(V))
]

VCL1 = [
    (p,ch(V) + has_cl_marker(V)),
    (w, copaux(V,W)),
    (w, qu_word(V,Q)),
    (w, is_qu_word(V)),
    (w, prec_subj(V,S)),
    (w, has_ecq_marker(V))
]

GNVCL1 = [
    (p,ch(V) + has_cl_marker(V) + prec_gn(V,GN)),
    (w, copaux(V,W)),
    (w, qu_word(V,Q)),
    (w, is_qu_word(V)),
    (w, has_ecq_marker(V))
]


### Constituent

SVQ1 = [
    (p, ch(V) + qu_word(V,Q) + precedes(V,Q) + prec_subj(V,S)),
    (w, copaux(V,W)),
    (w, has_ecq_marker(V)),
    (w, has_cl_marker(V))
]
SVQ2 = [
]
SVQ3 = [
    (p, ch(Q) + is_qu_word(Q) + copaux(Q,V) + prec_subj(V,S)),
    (w, has_ecq_marker(Q)),
    (w, has_cl_marker(Q))
]

QSV1 = [
    (p, ch(V) + qu_word(V,Q) + prec_subj(V,S) + precedes(Q,S)),
    (w, copaux(V,W)),
    (w, has_ecq_marker(V)),
    (w, has_cl_marker(V))
]
QSV2 = [
]
QSV3 = [
    (p, ch(Q) + is_qu_word(Q) + copaux(Q,V) + prec_subj(S,V) + precedes(Q,S)),
    (w, has_ecq_marker(Q)),
    (w, has_cl_marker(Q))
]

QVCL1 = [
    (p, ch(V) + precedes(Q,V) + has_cl_marker(V)),
    (w, copaux(V,W)),
    (w, has_ecq_marker(V)),
    (w, prec_subj(V,S))
]

QGNVCL1 = [
    (p, ch(V) + prec_gn(V,GN) + precedes(Q,GN) + has_cl_marker(V)),
    (w, copaux(V,W)),
    (w, has_ecq_marker(V))
]

QVGN1 = [
    (p, ch(V) + suc_gn(V,GN) + precedes(Q,V)),
    (w, copaux(V,W)),
    (w, has_ecq_marker(V)),
    (w, has_cl_marker(V)),
    (w, cl_marker(GN))
]

SEQKSV1 = [
    (p,'''V[ClauseType="Int"] ; V -[cue:wh]-> Q ;
     ''')
]

QESV1 = [
    (p,ch(V) + ecq_marker(V,E) + qu_word(V,Q) + precedes(Q,E)
     + prec_subj(V,S) + precedes(E,S)),
    (w, copaux(V,W)),
    (w, has_cl_marker(V))
]

QSEKSV1 = [
    (p,'''V[ClauseType="Int"] ; V -[cue:wh]-> Q ;
     ''')
]

QKSV1 = [
    (p,ch(V) + que_marker(V,K) + qu_word(V,Q) + precedes(Q,K)
     + prec_subj(V,S) + precedes(K,S)),
    (w, copaux(V,W)),
    (w, has_cl_marker(V))
]

QeqSV1 = [
    (p,'''V[ClauseType="Int"] ; V -[cue:wh]-> Q ;
     ''')
]

COVENEY_REQS = { # From [Coveney 2011]
    # yes-no (fr. totale):
    "ESV": ESV1, # Est-ce que les autres / ils sont partis ?
    "V-CL": VCL1, # Sont-ils partis ?
    "GN_V-CL": GNVCL1, # Les autres sont-ils partis ?
    # constituent (fr. partielle):
    "SVQ": SVQ1, # Ils sont partis où ?
    "QSV": QSV1, # Où ils sont partis ?
    "QV-CL": QVCL1, # Où sont-ils partis ?
    "Q_GN_V-CL": QGNVCL1, # Où les autres sont-ils partis ?
    "QV_GN": QVGN1, # Où sont partis les autres ?
    "seQkSV": SEQKSV1, # C’est où qu’ils sont partis ?
    "QESV": QESV1, # Où est-ce qu’ils sont partis ?
    "QsekSV": QSEKSV1, # Où c’est qu’ils sont partis ?
    "QkSV": QKSV1, # Où qu’ils sont partis ?
    "Q=S_V": QeqSV1, # Lesquels sont partis ?
    # hybrid
    "QEV_GN": "qu+ 'est-ce que' + stylistic inversion", # Avec qui est-ce que travaille nicole Dupont ?
    "Q=S_V-CL": "subject qu + clitic inversion", # De ces fillettes, lesquelles sont-elles les tiennes ?
    "E_GN_V-CL": "'est-ce que' + complex inversion", # Est-ce que demain les sauveteurs pourront-ils s’approcher des alpinistes en détresse ?
    "QE_GN_V-CL": "qu + 'est-ce que' + complex inversion" # Qu’est-ce que le rédacteur de la rubrique des chats écrasés entend-il par un pachyderme ?
}