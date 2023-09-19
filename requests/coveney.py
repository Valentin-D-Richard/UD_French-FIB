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
C = "C"
EST = "EST"
W = "*" # wildcard
p = "pattern"
w = "without"


#### Regularly occurring strings
def ecq_marker(head:str, marker:str) -> str:
    req = head+' -[cue:mark]-> '+marker+' ; '
    return req+marker+'[lemma="être"] ; \n'

def has_ecq_marker(head:str) -> str:
    return ecq_marker(head,E)

def cl_marker(head:str, subject:str) -> str:
    req = head+' -[cue:mark]-> '+subject+' ; \n'
    req += head+' -[expl:subj|nsubj|nsubj:pass]-> '+subject+' ; '
    return req+subject+'[upos="PRON"] ; \n'

def has_cl_marker(head:str) -> str:
    return cl_marker(head, CL)

def que_marker(head:str, marker:str) -> str:
    req = head+' -[cue:mark]-> '+marker+' ; '
    return req+marker+'[lemma="que"] ; \n'

def has_que_marker(head:str) -> str:
    return cl_marker(head, K)

def ch(head:str) -> str: # is_clause_head
    return head+'[ClauseType="Int"] ; \n'

def is_qu_word(head:str) -> str:
    return head+'[PronType="Int"] ; \n'

def qu_word(head:str, qu:str) -> str:
    return head+' -[cue:wh]-> '+qu+' ; \n'

def copaux(head:str, verb:str) -> str:
    return head+' -[1=cop|aux]-> '+verb+' ; \n'

def fin_copaux(head:str, verb:str) -> str:
    return verb+'[VerbForm="Fin"] ; '+copaux(head,verb)

def precedes(first:str, second:str) -> str:
    return first+' << '+second+' ; \n'

def prec_subj(head:str, subject:str) -> str:
    req = head+' -[expl:subj|nsubj|nsubj:pass|csubj]-> '+subject
    return req+' ; '+precedes(subject,head)

def suc_subj(head:str, subject:str) -> str:
    req = head+' -[expl:subj|nsubj|nsubj:pass|csubj]-> '+subject
    return req+' ; '+precedes(head,subject)

def prec_gn(head:str, subject:str) -> str:
    req = head+' -[nsubj|nsubj:pass]-> '+subject
    return req+' ; '+precedes(subject,head)

def suc_gn(head:str, subject:str) -> str:
    req = head+' -[nsubj|nsubj:pass]-> '+subject
    return req+' ; '+precedes(head,subject)

def lemma(head:str, lemma:str) -> str:
    return head+'[lemma="'+lemma+'"] ; \n'

def cleft(subj:str, cop:str, sconj:str) -> str:
    req = subj+'[lemma="ce"] ; '+cop+'[lemma="être"] ; '
    req += subj+' < '+cop+' ; \n'
    return req+sconj+'[lemma="que"|"qui"|"dont", upos="SCONJ"] ; \n'

def subordinated1(head:str) -> str:
    return 'A -[1=ccomp|csubj|xcomp]-> '+head+' ; \n'

def subordinated2(head:str) -> str:
    req = 'A -[1=acl|advcl]-> '+head+' ; \n'
    return req+head+' -> P ; P[lemma="ADP"] ; P << '+head


##### Request descriptions

# Version 1 with V as main verb
# Version 2 with V finite auxiliary or copula
# Version 3 Q is UD clause head and V as auxiliary or copula

### yes-no

ESV1 = [
    (p, ch(V) + has_ecq_marker(V) + prec_subj(V,S)),
    (w, qu_word(V,Q)),
    (w, is_qu_word(V)),
    (w, has_cl_marker(V)),
    (w, subordinated1(V)),
]

VCL1 = [
    (p,ch(V) + cl_marker(V,CL) + precedes(V,CL)),
    (w, copaux(V,W)),
    (w, qu_word(V,Q)),
    (w, is_qu_word(V)),
    (w, prec_subj(V,S)),
    (w, has_ecq_marker(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
VCL2 = [
    (p,ch(CH) + fin_copaux(CH,V) + cl_marker(CH,CL) + precedes(V,CL)),
    (w, qu_word(CH,Q)),
    (w, is_qu_word(CH)),
    (w, prec_subj(CH,S)),
    (w, has_ecq_marker(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]

GNVCL1 = [
    (p,ch(V) + cl_marker(V,CL) + prec_gn(V,GN) + precedes(V,CL)),
    (w, copaux(V,W)),
    (w, qu_word(V,Q)),
    (w, is_qu_word(V)),
    (w, has_ecq_marker(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
GNVCL2 = [
    (p,ch(CH) + fin_copaux(CH,V) + cl_marker(CH,CL) + precedes(V,CL) +
     prec_gn(CH,GN) + precedes(GN,V)),
    (w, qu_word(CH,Q)),
    (w, is_qu_word(CH)),
    (w, has_ecq_marker(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]


### Constituent

SVQ1 = [
    (p, ch(V) + qu_word(V,Q) + precedes(V,Q) + prec_subj(V,S)),
    (w, copaux(V,W)),
    (w, has_ecq_marker(V)),
    (w, has_cl_marker(V)),
    (w, has_que_marker(V)),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
SVQ2 = [
    (p, ch(CH) + fin_copaux(CH,V) + qu_word(CH,Q) + precedes(V,Q) +
     prec_subj(CH,S) + precedes(S,V)),
    (w, has_ecq_marker(CH)),
    (w, has_cl_marker(CH)),
    (w, has_que_marker(CH)),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
SVQ3 = [
    (p, ch(Q) + is_qu_word(Q) + fin_copaux(Q,V) + prec_subj(V,S)),
    (w, has_ecq_marker(Q)),
    (w, has_cl_marker(Q)),
    (w, has_que_marker(Q)),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

QSV1 = [
    (p, ch(V) + qu_word(V,Q) + prec_subj(V,S) + precedes(Q,S)),
    (w, copaux(V,W)),
    (w, has_ecq_marker(V)),
    (w, has_cl_marker(V)),
    (w, has_que_marker(V)),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
QSV2 = [
    (p, ch(CH) + fin_copaux(CH,V) + qu_word(CH,Q) + prec_subj(CH,S) +
     precedes(S,V) + precedes(Q,S)),
    (w, has_ecq_marker(CH)),
    (w, has_cl_marker(CH)),
    (w, has_que_marker(CH)),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
QSV3 = [
    (p, ch(Q) + is_qu_word(Q) + fin_copaux(Q,V) + prec_subj(Q,S) +
     precedes(Q,S)),
    (w, has_ecq_marker(Q)),
    (w, has_cl_marker(Q)),
    (w, has_que_marker(Q)),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

QVCL1 = [
    (p, ch(V) + precedes(Q,V) + qu_word(V,Q) + cl_marker(V,CL) +
     precedes(V,CL)),
    (w, copaux(V,W)),
    (w, has_ecq_marker(V)),
    (w, prec_subj(V,S)),
    (w, has_que_marker(V)),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
QVCL2 = [
    (p, ch(CH) + fin_copaux(CH,V) + precedes(Q,V) + qu_word(V,Q) +
     cl_marker(CH,CL) + precedes(V,CL)),
    (w, has_ecq_marker(CH)),
    (w, prec_subj(CH,S)),
    (w, has_que_marker(CH)),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
QVCL3 = [
    (p, ch(Q) + is_qu_word(Q) + fin_copaux(Q,V) + precedes(Q,V) + 
     cl_marker(Q,CL) + precedes(V,CL)),
    (w, has_ecq_marker(Q)),
    (w, suc_subj(Q,S)),
    (w, has_que_marker(Q)),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

QGNVCL1 = [
    (p, ch(V) + prec_gn(V,GN) + qu_word(V,Q) + precedes(Q,GN) +
     cl_marker(V,CL) + precedes(V,CL)),
    (w, copaux(V,W)),
    (w, has_ecq_marker(V)),
    (w, has_que_marker(V)),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
QGNVCL2 = [
    (p, ch(CH) + fin_copaux(CH,V) + prec_gn(CH,GN) + precedes(GN,V) +
     qu_word(CH,Q) + precedes(Q,GN) +
     cl_marker(CH,CL) + precedes(V,CL)),
    (w, has_ecq_marker(CH)),
    (w, has_que_marker(CH)),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
QGNVCL3 = [
    (p, ch(Q) + suc_gn(Q,GN) + is_qu_word(Q) + fin_copaux(Q,V) + precedes(GN,V) +
     cl_marker(Q, CL) + precedes(V, CL)),
    (w, has_ecq_marker(Q)),
    (w, has_que_marker(Q)),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

QVGN1 = [
    (p, ch(V) + suc_gn(V,GN) + qu_word(V,Q) + precedes(Q,V)),
    (w, copaux(V,W)),
    (w, has_ecq_marker(V)),
    (w, has_cl_marker(V)),
    (w, cl_marker(V,GN)),
    (w, has_que_marker(V)),
    (w, prec_subj(V,S)),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
QVGN2 = [
    (p, ch(CH) + fin_copaux(CH,V) + precedes(V,CH) + suc_gn(CH,GN) +
     qu_word(CH,Q) + precedes(Q,V)),
    (w, has_ecq_marker(CH)),
    (w, has_cl_marker(CH)),
    (w, cl_marker(CH,GN)),
    (w, has_que_marker(CH)),
    (w, prec_subj(CH,S)),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
QVGN3 = [
    (p, ch(Q) + is_qu_word(Q) + suc_gn(Q,GN) + fin_copaux(Q,V) + precedes(V,GN)),
    (w, has_ecq_marker(Q)),
    (w, has_cl_marker(Q)),
    (w, cl_marker(Q,GN)),
    (w, suc_subj(Q,S)),
    (w, has_que_marker(Q)),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

SEQKSV1 = [
    (p,ch(V) + qu_word(V,Q) + prec_subj(V,S) + cleft(C,EST,K) + 
     precedes(C,EST) + precedes(Q,K) + precedes(K,S)),
    (w, copaux(V,W)),
    (w, has_cl_marker(V)),
    (w, has_ecq_marker(V)),
    (w, que_marker(V, "K2")),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
SEQKSV2 = [
    (p,ch(CH) + fin_copaux(CH,V) + qu_word(CH,Q) + prec_subj(CH,S) +
     precedes(S,V) + cleft(C,EST,K) + 
     precedes(C,EST) + precedes(Q,K) + precedes(K,S)),
    (w, has_cl_marker(CH)),
    (w, has_ecq_marker(CH)),
    (w, que_marker(CH, "K2")),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
SEQKSV3 = [
    (p,ch(Q) + is_qu_word(Q) + fin_copaux(Q,V) + suc_subj(Q,S) + cleft(C,EST,K) + 
     precedes(C,EST) + precedes(Q,K) + precedes(K,S) + precedes(S,V)),
    (w, has_cl_marker(Q)),
    (w, has_ecq_marker(Q)),
    (w, que_marker(Q, "K2")),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

QESV1 = [
    (p,ch(V) + ecq_marker(V,E) + qu_word(V,Q) + precedes(Q,E)
     + prec_subj(V,S) + precedes(E,S)),
    (w, copaux(V,W)),
    (w, has_cl_marker(V)),
    (w, has_que_marker(V)),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
QESV2 = [
    (p,ch(CH) + fin_copaux(CH,V) + ecq_marker(CH,E) + qu_word(CH,Q) +
     precedes(Q,E) + prec_subj(CH,S) + precedes(S,V) + precedes(E,S)),
    (w, has_cl_marker(CH)),
    (w, has_que_marker(CH)),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
QESV3 = [
    (p,ch(Q) + is_qu_word(Q) + ecq_marker(Q,E) + fin_copaux(Q,V) + precedes(Q,E)
     + suc_subj(Q,S) + precedes(E,S) + precedes(S,V)),
    (w, has_cl_marker(Q)),
    (w, has_que_marker(Q)),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

QSEKSV1 = [
    (p, ch(V) + qu_word(V,Q) + prec_subj(V,S) + cleft(C,EST,K) + 
     precedes(Q,C) + precedes(EST,K) + precedes(K,S)),
    (w, copaux(V,W)),
    (w, has_cl_marker(V)),
    (w, has_ecq_marker(V)),
    (w, que_marker(V, "K2")),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
QSEKSV2 = [
    (p, ch(CH) + fin_copaux(CH,V) + qu_word(CH,Q) + prec_subj(CH,S) +
     precedes(S,V) + cleft(C,EST,K) + 
     precedes(Q,C) + precedes(EST,K) + precedes(K,S)),
    (w, has_cl_marker(CH)),
    (w, has_ecq_marker(CH)),
    (w, que_marker(CH, "K2")),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
QSEKSV3 = [
    (p, ch(Q) + is_qu_word(Q) + fin_copaux(Q,V) + suc_subj(S,S) + cleft(C,EST,K) + 
     precedes(Q,C) + precedes(EST,K) + precedes(K,S) + precedes(S,V)),
    (w, has_cl_marker(Q)),
    (w, has_ecq_marker(Q)),
    (w, que_marker(Q, "K2")),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

QKSV1 = [
    (p, ch(V) + que_marker(V,K) + qu_word(V,Q) + precedes(Q,K)
     + prec_subj(V,S) + precedes(K,S)),
    (w, copaux(V,W)),
    (w, has_cl_marker(V)),
    (w, is_qu_word(V)),
    (w, has_ecq_marker(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
QKSV2 = [
    (p, ch(CH) + fin_copaux(CH,V) + que_marker(CH,K) + qu_word(CH,Q) +
     precedes(Q,K) + prec_subj(CH,S) + precedes(S,V) + precedes(K,S)),
    (w, has_cl_marker(CH)),
    (w, is_qu_word(CH)),
    (w, has_ecq_marker(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
QKSV3 = [
    (p, ch(Q) + is_qu_word(Q) + que_marker(V,K) + fin_copaux(Q, V) +
     precedes(Q,K) + suc_subj(Q,S) + precedes(K,S) + precedes(S,V)),
    (w, has_cl_marker(Q)),
    (w, has_ecq_marker(Q)),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

QeqSV1 = [
    (p, ch(V) + prec_subj(V,Q) + qu_word(V,Q)),
    (w, copaux(V,W)),
    (w, has_cl_marker(V)),
    (w, has_ecq_marker(V)),
    (w, has_que_marker(V)),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
QeqSV2 = [
    (p, ch(CH) + fin_copaux(CH,V) + prec_subj(CH,Q) + precedes(Q,V) +
     qu_word(CH,Q)),
    (w, has_cl_marker(CH)),
    (w, has_ecq_marker(CH)),
    (w, has_que_marker(CH)),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
QeqSV3 = [
    (p, ch(Q) + is_qu_word(Q) + fin_copaux(Q,V) + precedes(Q,V)),
    (w, has_cl_marker(V)),
    (w, has_ecq_marker(V)),
    (w, has_que_marker(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]

QEVGN1 = [
    (p, ch(V) + qu_word(V,Q) + ecq_marker(V,E) + suc_gn(V,GN) + 
     precedes(Q,E) + precedes(E,V)),
    (w, copaux(V, W)),
    (w, has_cl_marker(V)),
    (w, cl_marker(V,GN)),
    (w, has_que_marker(V)),
    (w, prec_subj(V,S)),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
QEVGN2 = [
    (p, ch(CH) + fin_copaux(CH,V) + qu_word(CH,Q) + ecq_marker(CH,E) +
     suc_gn(CH,GN) + precedes(Q,E) + precedes(E,V) + precedes(V,GN)),
    (w, has_cl_marker(CH)),
    (w, cl_marker(CH,GN)),
    (w, has_que_marker(CH)),
    (w, prec_subj(CH,S)),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
QEVGN3 = [
    (p, ch(Q) + is_qu_word(Q) + fin_copaux(Q,V) + ecq_marker(Q,E) + suc_gn(Q,GN) + 
     precedes(Q,E) + precedes(E,V) + precedes(V,GN)),
    (w, has_cl_marker(Q)),
    (w, cl_marker(Q,GN)),
    (w, suc_subj(Q,S)),
    (w, has_que_marker(Q)),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

QeqSVCL1 = [
    (p, ch(V) + qu_word(V,Q) + cl_marker(V,CL) + prec_subj(V,Q) +
     precedes(V,CL)),
    (w, copaux(V, W)),
    (w, has_ecq_marker(V)),
    (w, has_que_marker(V)),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
QeqSVCL2 = [
    (p, ch(CH) + fin_copaux(CH, V) + qu_word(CH,Q) + cl_marker(CH,CL) +
     prec_subj(CH,Q) + precedes(Q,V) + precedes(V,CL)),
    (w, has_ecq_marker(CH)),
    (w, has_que_marker(CH)),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
QeqSVCL3 = [
    (p, ch(Q) + is_qu_word(Q) + fin_copaux(Q,V) + cl_marker(Q,CL) +
     precedes(V,CL)),
    (w, copaux(Q, W)),
    (w, has_ecq_marker(Q)),
    (w, has_que_marker(Q)),
    (w, suc_subj(Q,S)),
    (w, is_qu_word(Q)),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

EGNVCL1 = [
    (p, ch(V) + prec_gn(V,GN) + ecq_marker(V,E) + precedes(E,GN) + 
     cl_marker(V,CL) + precedes(V,CL)),
    (w, copaux(V, W)),
    (w, has_que_marker(V)),
    (w, qu_word(V,Q)),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
EGNVCL2 = [
    (p, ch(CH) + fin_copaux(CH,V) + prec_gn(CH,GN) + precedes(GN,V) +
     ecq_marker(CH,E) + precedes(E,GN) + 
     cl_marker(CH,CL) + precedes(V,CL)),
    (w, has_que_marker(CH)),
    (w, qu_word(CH,Q)),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]

QEGNVCL1 = [
    (p, ch(V) + prec_gn(V,GN) + ecq_marker(V,E) + precedes(E,GN) + 
     cl_marker(V,CL) + precedes(V,CL) + 
     qu_word(V,Q) + precedes(Q,E)),
    (w, copaux(V, W)),
    (w, has_que_marker(V)),
    (w, is_qu_word(V)),
    (w, subordinated1(V)), (w, subordinated2(V))
]
QEGNVCL2 = [
    (p, ch(CH) + fin_copaux(CH,V) + prec_gn(CH,GN) + precedes(GN,V) +
     ecq_marker(CH,E) + precedes(E,GN) + 
     cl_marker(CH,CL) + precedes(V,CL) + qu_word(CH,Q) + precedes(Q,E)),
    (w, has_que_marker(CH)),
    (w, is_qu_word(CH)),
    (w, subordinated1(CH)), (w, subordinated2(CH))
]
QEGNVCL3 = [
    (p, ch(Q) + fin_copaux(Q,V) + suc_gn(Q,GN) + precedes(GN,V) +
     ecq_marker(CH,E) + precedes(E,GN) + 
     cl_marker(Q,CL) + precedes(V,CL) + is_qu_word(Q) + precedes(Q,E)),
    (w, has_que_marker(Q)),
    (w, subordinated1(Q)), (w, subordinated2(Q))
]

COVENEY_REQS = { # From [Coveney 2011]
    # yes-no (fr. totale):
    "ESV": [ESV1], # Est-ce que les autres / ils sont partis ?
    "V-CL": [VCL1, VCL2], # Sont-ils partis ?
    "GN_V-CL": [GNVCL1, GNVCL2], # Les autres sont-ils partis ?
    # constituent (fr. partielle):
    "SVQ": [SVQ1, SVQ2, SVQ3], # Ils sont partis où ?
    "QSV": [QSV1, QSV2, QSV3], # Où ils sont partis ?
    "QV-CL": [QVCL1, QVCL2, QVCL3], # Où sont-ils partis ?
    "Q_GN_V-CL": [QGNVCL1, QGNVCL2, QGNVCL3], # Où les autres sont-ils partis ?
    "QV_GN": [QVGN1, QVGN2, QVGN3], # Où sont partis les autres ?
    "seQkSV": [SEQKSV1, SEQKSV2, SEQKSV3], # C’est où qu’ils sont partis ?
    "QESV": [QESV1, QESV2, QESV3], # Où est-ce qu’ils sont partis ?
    "QsekSV": [QSEKSV1, QSEKSV2, QSEKSV3], # Où c’est qu’ils sont partis ?
    "QkSV": [QKSV1, QKSV2, QKSV3], # Où qu’ils sont partis ?
    "Q=S_V": [QeqSV1, QeqSV2, QeqSV3], # Lesquels sont partis ?
    # hybrid
    "QEV_GN": [QEVGN1, QEVGN2, QEVGN3], # Avec qui est-ce que travaille nicole Dupont ?
    "Q=S_V-CL": [QeqSVCL1, QeqSVCL2, QeqSVCL3], # De ces fillettes, lesquelles sont-elles les tiennes ?
    "E_GN_V-CL": [EGNVCL1, EGNVCL2], # Est-ce que demain les sauveteurs pourront-ils s’approcher des alpinistes en détresse ?
    "QE_GN_V-CL": [QEGNVCL1, QEGNVCL2, QEGNVCL3] # Qu’est-ce que le rédacteur de la rubrique des chats écrasés entend-il par un pachyderme ?
}