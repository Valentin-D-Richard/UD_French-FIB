from .classes import Snippet, DisjRule
from .coveney import copaux, ch, precedes, cleft, has_cl_marker, has_que_marker, \
    has_left_fininf_aux, has_right_fininf_aux, has_right_fininf_cop, \
    has_ecq_marker, is_qu_word, qu_word, prec_gn, subordinated1, subordinated2

V = "V" # main verb
Q = "Q" # qu-word
S = "S" # subject
E = "E" # 'est-ce que'
CL = "CL" # clitic subject marker
GN = "GN" # nominal subject
CH = "CH" # UD clause head (if different from V)
K = "K" # 'que'
SI = "SI"
C = "C"
EST = "EST"
A = "A" # other auxiliary or copula
AN = "AN" # anchor
G = "G" # governer
T = "T" # -ti/-tu
W = "*" # wildcard

#### utils 

def p(pattern:str) -> str:
    return 'pattern { '+pattern+' } \n'

def w(pattern:str) -> str:
    return 'without { '+pattern+' } \n'

def subj(head:str) -> str:
    return head+' -[expl:subj|nsubj|nsubj:pass|csubj]-> S ; \n'

def fininf_copaux(head:str,verb:str) -> str:
    return verb+'[VerbForm="Fin"|"Inf"] ; '+copaux(head,verb)

def has_si_marker(head:str) -> str:
    req = head+' -[cue:mark]-> SI ; '
    return req+'SI[lemma="si"] ; \n'

def has_titu_marker1(head:str) -> str:
    req = head+' -[mark]-> T ; '+head+' -[cue:mark]-> T ; '
    return req+'T[form="tu"|"-tu"|"ti"|"-ti"|"TU"|"-TU"|"TI"|"-TI"] ; \n'

def has_titu_marker2(head:str) -> str:
    req = head+' -[cue:mark]-> T ; T[upos="PART"] ; '
    return req+'T[form="tu"|"-tu"|"ti"|"-ti"|"TU"|"-TU"|"TI"|"-TI"] ; \n'

def cleft1(verb:str) -> str :
    req = cleft(C,EST,K) + precedes(EST,Q)
    return req + precedes(Q,K) + precedes(K,verb)

def cleft2(verb:str) -> str :
    req = cleft(C,EST,K) + precedes(Q,C)
    return req + precedes(EST,K) + precedes(K,verb)

# Version a: with V as main verb

# ClauseType and anchor
a0_0 = Snippet("0_0.")
a0_0.request = p(ch(V)) + w(copaux(V,W)) + w(is_qu_word(V))


# Version b: with V auxiliary or copula

# ClauseType, copula or auxiliary and anchor
b0_0 = Snippet("0_0.")
b0_0.request = p(ch(CH) + fininf_copaux(CH,V)) + \
    w(has_left_fininf_aux(CH)) + w(is_qu_word(CH)) + \
    w(has_right_fininf_aux(CH)) + w(has_right_fininf_cop(CH))


# Version c: Q is UD clause head and V as auxiliary or copula

# ClauseType, is qu-word, copula or auxiliary and anchor
c0_0 = Snippet("0_0.")
c0_0.request = p(ch(Q) + fininf_copaux(Q,V) + is_qu_word(Q)) + \
    w(has_left_fininf_aux(Q)) + \
    w(has_right_fininf_aux(Q)) + w(has_right_fininf_cop(Q))


# Version d: Q is UD clause head, and no verb
d0_0 = Snippet("0_0")
d0_0.request = p(ch(Q) + is_qu_word(Q)) + w(copaux(Q,W))



### Clause-level interrogative marker
def cm(H:str) -> str:
    # ecq
    r1_0 = Snippet("1_0.")
    r1_0.request = p(has_ecq_marker(H)) + w(has_que_marker(H)) + \
        w(has_si_marker(H))

    # que
    r1_1 = Snippet("1_1.")
    r1_1.request = w(has_ecq_marker(H)) + p(has_que_marker(H)) + \
        w(has_si_marker(H))

    #si
    r1_2 = Snippet("1_2.")
    r1_2.request = w(has_ecq_marker(H)) + w(has_que_marker(H)) + \
        p(has_si_marker(H))
    
    r1_3 = Snippet("1_3.")
    r1_3.request = w(has_ecq_marker(H)) + w(has_que_marker(H)) + \
        w(has_si_marker(H))
    
    return [r1_0, r1_1, r1_2, r1_3]


### Verb-level interrogative marker
def vm(H:str) -> str:
    # clitic suffixation
    r2_0 = Snippet("2_0.")
    r2_0.request = p(has_cl_marker(H)) + w(has_titu_marker1(H)) + \
        w(has_titu_marker2(H))
    
    # -ti/-tu (first possibility)
    r2_1 = Snippet("2_1.")
    r2_1.request = p(has_cl_marker(H)) + w(has_titu_marker1(H)) + \
        w(has_titu_marker2(H))
    
    # -ti/-tu (second possibility)
    r2_1_alt = Snippet("2_1.")
    r2_1_alt.request = p(has_cl_marker(H)) + w(has_titu_marker1(H)) + \
        w(has_titu_marker2(H))
    
    r2_2 = Snippet("2_2.")
    r2_2.request = w(has_cl_marker(H)) + w(has_titu_marker1(H)) + \
        w(has_titu_marker2(H))
    
    return [r2_0, r2_1, r2_1_alt, r2_2]


### QU-word
def qu(H:str) -> str:
    # presence of a different qu word
    r3_0 = Snippet("3_0.")
    r3_0.request = p(qu_word(H,Q))

    # no qu-word
    r3_1 = Snippet("3_1.")
    r3_1.request = w(qu_word(H,Q))

    return [r3_0, r3_1]

c3_0 = Snippet("3_0.") 
c3_0.request = p('') # In version c, Q is the qu_word

d3_0 = Snippet("3_0.") 
d3_0.request = p('') # In version c, Q is the qu_word


### Global place of the qu-phrase
def ipplace_strd(H:str,MV:str) -> str:
    # MV is the main verb, relative to which the position is computed
    # subject are considered in situ

    # in-situ
    r4_0 = Snippet("4_0.")
    r4_0.request = p(precedes(MV,Q))

    # in-situ: case of subject
    r4_0_alt = Snippet("4_0.")
    r4_0_alt.request = p(prec_gn(H,Q))

    # fronted, not subject
    r_4_1 = Snippet("4_1.")
    r_4_1.request = p(precedes(Q,MV)) + w(prec_gn(H,Q))

    return [r4_0, r4_0_alt, r_4_1]

def ipplace_cleft(H:str,MV:str) -> str:
    # cleft1
    r4_2 = Snippet("4_2.")
    r4_2.request = p(cleft1(MV)) + w(prec_gn(H,Q))

    # cleft2
    r4_3 = Snippet("4_3.")
    r4_3.request = p(cleft2(MV)) + w(prec_gn(H,Q))

    return [r4_2, r4_3]

# alone (elliptic) or nominal
d4_4 = Snippet("4_4.")
d4_4.request = p('')


### Syntactic position of the interrogative word in the interrogative phrase
# Ignored for the moment

### Syntactic position of the interrogative phrase in the clause
# Ignored for the moment

### Dependencies of the qu-word
# Ignored for the moment

### Syntactic position of the interrogative clause
def quspos(H:str) -> str:
    # subordinated 1
    r8_0 = Snippet("8_0.")
    r8_0.request = p(subordinated1(H))

    # subordinated 2
    r8_0_alt = Snippet("8_0.")
    r8_0_alt.request = p(subordinated2(H))

    # root
    r8_1 = Snippet("8_1.")
    r8_1.request = w(subordinated1(H)) + w(subordinated2(H))

    return [r8_0, r8_0_alt, r8_1]


### Verbal form
# Ignored for the moment

### Place of the subject
def subjplace(H:str,MV:str) -> str:
    # canonical (before the main verb)
    r10_0 = Snippet("10_0.")
    r10_0.request = p(subj(H) + precedes(S,MV))

    # stylistic inversion
    r10_1 = Snippet("10_1.")
    r10_1.request = p(subj(H) + precedes(MV,S))

    # no (other) subject
    r10_2 = Snippet("10_2.")
    r10_2.request = w(subj(H))

    return [r10_0, r10_1, r10_2]

root = Snippet("root.")

modular = DisjRule("modular", root)
modular.add_snippets([a0_0, b0_0, c0_0, d0_0], root)

# Version a
modular.add_snippets(cm(V), a0_0)
modular.add_snippets(vm(V), a0_0)
qu_a = qu(V)
modular.add_snippets(qu_a, a0_0)
qu_a_snippet = qu_a[0]
modular.add_snippets(ipplace_strd(V,V) + ipplace_cleft(V,V), qu_a_snippet)
modular.add_snippets(quspos(V), a0_0)
modular.add_snippets(subjplace(V,V), a0_0)

# Version b
modular.add_snippets(cm(CH), b0_0)
modular.add_snippets(vm(CH), b0_0)
qu_b = qu(CH)
modular.add_snippets(qu_b, b0_0)
qu_b_snippet = qu_b[0]
modular.add_snippets(ipplace_strd(CH,V) + ipplace_cleft(CH,V), qu_b_snippet)
modular.add_snippets(quspos(CH), b0_0)
modular.add_snippets(subjplace(CH,V), b0_0)

# Version c
modular.add_snippets(cm(Q), c0_0)
modular.add_snippets(vm(Q), c0_0)
modular.add_snippets([c3_0], c0_0)
modular.add_snippets(ipplace_strd(Q,V), c3_0)
modular.add_snippets(quspos(Q), c0_0)
modular.add_snippets(subjplace(Q,V), c0_0)

# Version d
modular.add_snippets(cm(Q), d0_0)
modular.add_snippets(vm(Q)[-1:], d0_0)
modular.add_snippets([d3_0], d0_0)
modular.add_snippets([d4_4], d3_0)
modular.add_snippets(quspos(Q), d0_0)
modular.add_snippets(subjplace(Q,W)[-1:], d0_0)


branches = modular.gen_branches(output="request", group_by_trace=True,
                                keep_trace=True)
MODULAR_REQ = {
    cat: req_list for (cat,req_list) in branches
}