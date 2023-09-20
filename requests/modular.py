import classes as cl
import coveney as cv

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
    return verb+'[VerbForm="Fin"|"Inf"] ; '+cv.copaux(head,verb)

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
    req = cv.cleft(C,EST,K) + cv.precedes(EST,Q)
    return req + cv.precedes(Q,K) + cv.precedes(K,verb)

def cleft2(verb:str) -> str :
    req = cv.cleft(C,EST,K) + cv.precedes(Q,C)
    return req + cv.precedes(EST,K) + cv.precedes(K,verb)

# Version a: with V as main verb

# ClauseType and anchor
a0_0 = cl.Snippet("0_0.")
a0_0.request = p(cv.ch(V)) + w(cv.copaux(V,W)) + w(cv.is_qu_word(V))

version_a = cl.DisjRule("version_a", a0_0)


# Version b: with V auxiliary or copula

# ClauseType, copula or auxiliary and anchor
b0_0 = cl.Snippet("0_0.")
b0_0.request = p(cv.ch(CH) + fininf_copaux(CH,V)) + \
    w(cv.has_left_fininf_aux(CH)) + w(cv.is_qu_word(CH)) + \
    w(cv.has_right_fininf_aux(CH)) + w(cv.has_right_fininf_cop(CH))

version_b = cl.DisjRule("version_b", b0_0)


# Version c: Q is UD clause head and V as auxiliary or copula

# ClauseType, is qu-word, copula or auxiliary and anchor
c0_0 = cl.Snippet("0_0.")
c0_0.request = p(cv.ch(Q) + fininf_copaux(Q,V) + cv.is_qu_word(Q)) + \
    w(cv.has_left_fininf_aux(Q)) + \
    w(cv.has_right_fininf_aux(Q)) + w(cv.has_right_fininf_cop(Q))

version_c = cl.DisjRule("version_c", c0_0)


# Version d: Q is UD clause head, and no verb
d0_0 = cl.Snippet("0_0")
d0_0.request = p(cv.ch(Q) + cv.is_qu_word(Q)) + w(cv.copaux(Q,W))

version_d = cl.DisjRule("version_d", d0_0)


### Clause-level interrogative marker
def cm(H:str) -> str:
    # ecq
    r1_0 = cl.Snippet("1_0.")
    r1_0.request = p(cv.has_ecq_marker(H)) + w(cv.has_que_marker(H)) + \
        w(has_si_marker(H))

    # que
    r1_1 = cl.Snippet("1_1.")
    r1_1.request = w(cv.has_ecq_marker(H)) + p(cv.has_que_marker(H)) + \
        w(has_si_marker(H))

    #si
    r1_2 = cl.Snippet("1_2.")
    r1_2.request = w(cv.has_ecq_marker(H)) + w(cv.has_que_marker(H)) + \
        p(has_si_marker(H))
    
    r1_3 = cl.Snippet("1_3.")
    r1_3.request = w(cv.has_ecq_marker(H)) + w(cv.has_que_marker(H)) + \
        w(has_si_marker(H))
    
    return [r1_0, r1_1, r1_2, r1_3]


### Verb-level interrogative marker
def vm(H:str) -> str:
    # clitic suffixation
    r2_0 = cl.Snippet("2_0.")
    r2_0.request = p(cv.has_cl_marker(H)) + w(has_titu_marker1(H)) + \
        w(has_titu_marker2(H))
    
    # -ti/-tu (first possibility)
    r2_1 = cl.Snippet("2_1.")
    r2_1.request = p(cv.has_cl_marker(H)) + w(has_titu_marker1(H)) + \
        w(has_titu_marker2(H))
    
    # -ti/-tu (second possibility)
    r2_1_alt = cl.Snippet("2_1.")
    r2_1_alt.request = p(cv.has_cl_marker(H)) + w(has_titu_marker1(H)) + \
        w(has_titu_marker2(H))
    
    r2_2 = cl.Snippet("2_2.")
    r2_2.request = w(cv.has_cl_marker(H)) + w(has_titu_marker1(H)) + \
        w(has_titu_marker2(H))
    
    return [r2_0, r2_1, r2_1_alt, r2_2]


### QU-word
def qu(H:str) -> str:
    # presence of a different qu word
    r3_0 = cl.Snippet("3_0.")
    r3_0.request = p(cv.qu_word(H,Q))

    # no qu-word
    r3_1 = cl.Snippet("3_1.")
    r3_1.request = w(cv.qu_word(H,Q))

    return [r3_0, r3_1]

c3_0 = cl.Snippet("3_0.") 
c3_0.request = p('') # In version c, Q is the qu_word


### Global place of the qu-phrase
def ipplace_strd(H:str,MV:str) -> str:
    # MV is the main verb, relative to which the position is computed
    # subject are considered in situ

    # in-situ
    r4_0 = cl.Snippet("4_0.")
    r4_0.request = p(cv.precedes(MV,Q))

    # in-situ: case of subject
    r4_0_alt = cl.Snippet("4_0.")
    r4_0_alt.request = p(cv.prec_gn(H,Q))

    # fronted, not subject
    r_4_1 = cl.Snippet("4_1.")
    r_4_1.request = p(cv.precedes(Q,MV)) + w(cv.prec_gn(H,Q))

    return [r4_0, r4_0_alt, r_4_1]

def ipplace_cleft(H:str,MV:str) -> str:
    # cleft1
    r4_2 = cl.Snippet("4_2.")
    r4_2.request = p(cleft1(MV)) + w(cv.prec_gn(H,Q))

    # cleft2
    r4_3 = cl.Snippet("4_3.")
    r4_3.request = p(cleft2(MV)) + w(cv.prec_gn(H,Q))

    return [r4_2, r4_3]

# alone (elliptic) or nominal
d4_4 = cl.Snippet("4_4.")
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
    r8_0 = cl.Snippet("8_0.")
    r8_0.request = p(cv.subordinated1(H))

    # subordinated 2
    r8_0_alt = cl.Snippet("8_0.")
    r8_0_alt.request = p(cv.subordinated2(H))

    # root
    r8_1 = cl.Snippet("8_1.")
    r8_1.request = w(cv.subordinated1(H)) + cv.subordinated2(H)

    return [r8_0, r8_0_alt, r8_1]


### Verbal form
# Ignored for the moment

### Place of the subject
def subjplace(H:str,MV:str) -> str:
    # canonical (before the main verb)
    r10_0 = cl.Snippet("10_0.")
    r10_0.request = p(subj(H) + cv.precedes(S,MV))

    # stylistic inversion
    r10_1 = cl.Snippet("10_1.")
    r10_1.request = p(subj(H) + cv.precedes(MV,S))

    # no (other) subject
    r10_2 = cl.Snippet("10_2.")
    r10_2.request = w(subj(H))

    return [r10_0, r10_1, r10_2]




# Version a
version_a.add_snippets(cm(V), a0_0)
version_a.add_snippets(vm(V), a0_0)
qu_a = qu(V)
version_a.add_snippets(qu_a, a0_0)
qu_a_snippet = qu_a[0]
version_a.add_snippets(ipplace_strd(V,V) + ipplace_cleft(V,V), qu_a_snippet)
version_a.add_snippets(quspos(V), a0_0)
version_a.add_snippets(subjplace(V,V), a0_0)

# Version b
version_b.add_snippets(cm(CH), b0_0)
version_b.add_snippets(vm(CH), b0_0)
qu_b = qu(CH)
version_b.add_snippets(qu_b, b0_0)
qu_b_snippet = qu_b[0]
version_b.add_snippets(ipplace_strd(CH,V) + ipplace_cleft(CH,V), qu_b_snippet)
version_b.add_snippets(quspos(CH), b0_0)
version_b.add_snippets(subjplace(CH,V), b0_0)

# Version c
version_c.add_snippets(cm(Q), c0_0)
version_c.add_snippets(vm(Q), c0_0)
version_c.add_snippets([c3_0], c0_0)
version_c.add_snippets(ipplace_strd(Q,V), c3_0)
version_c.add_snippets(quspos(Q), c0_0)
version_c.add_snippets(subjplace(Q,V), c0_0)

# Version d
version_d.add_snippets(cm(Q), d0_0)
version_d.add_snippets(vm(Q)[-1:], d0_0)
version_d.add_snippets([c3_0], d0_0)
version_d.add_snippets([d4_4], c3_0)
version_d.add_snippets(quspos(Q), d0_0)
version_d.add_snippets(subjplace(Q,W)[-1:], d0_0)

version_a.draw()
version_b.draw()
version_c.draw()
version_d.draw()