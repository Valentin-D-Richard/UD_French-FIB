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
T = "T" # -ti/-tu
W = "*" # wildcard

#### utils 

def p(pattern:str) -> str:
    return 'pattern { '+pattern+' } \n'

def w(pattern:str) -> str:
    return 'without { '+pattern+' } \n'

def ch_anchor(head:str) -> str:
    return head+'[ClauseType="Int"] ; a: A -> V'

def has_si_marker(head:str) -> str:
    req = head+' -[cue:mark]-> SI ; '
    return req+'SI[lemma="si"] ; \n'

def has_titu_marker1(head:str) -> str:
    req = head+' -[mark]-> T ; '+head+' -[cue:mark]-> T ; '
    return req+'T[form="tu"|"-tu"|"ti"|"-ti"|"TU"|"-TU"|"TI"|"-TI"] ; \n'

def has_titu_marker2(head:str) -> str:
    req = head+' -[cue:mark]-> T ; T[upos="PART"] ; '
    return req+'T[form="tu"|"-tu"|"ti"|"-ti"|"TU"|"-TU"|"TI"|"-TI"] ; \n'

# Version a: with V as main verb
# Version b: with V auxiliary or copula
# Version c: Q is UD clause head and V as auxiliary or copula

# ClauseType and anchor
a0_0 = cl.Snippet("0_0.")
a0_0.request = p(ch_anchor(V))

richard_a = cl.DisjRule("richard_a", a0_0)

### Clause-level interrogative marker
def cm(H:str) -> str:
    # ecq
    r1_0 = cl.Snippet("1_0")
    r1_0.request = p(cv.has_ecq_marker(H)) + w(cv.has_que_marker(H)) + \
        w(has_si_marker(H))

    # que
    r1_1 = cl.Snippet("1_1")
    r1_1.request = w(cv.has_ecq_marker(H)) + p(cv.has_que_marker(H)) + \
        w(has_si_marker(H))

    #si
    r1_2 = cl.Snippet("1_2")
    r1_2.request = w(cv.has_ecq_marker(H)) + w(cv.has_que_marker(H)) + \
        p(has_si_marker(H))
    
    return [r1_0, r1_1, r1_2]


### Verb-level interrogative marker
def vm(H:str) -> str:
    # clitic suffixation
    r2_0 = cl.Snippet("2_0")
    r2_0.request = p(cv.has_cl_marker(H)) + w(has_titu_marker1(H)) + \
        w(has_titu_marker2(H))
    
    # -ti/-tu (first possibility)
    r2_1 = cl.Snippet("2_1")
    r2_1.request = p(cv.has_cl_marker(H)) + w(has_titu_marker1(H)) + \
        w(has_titu_marker2(H))
    
    # -ti/-tu (second possibility)
    r2_1p = cl.Snippet("2_1")
    r2_1p.request = p(cv.has_cl_marker(H)) + w(has_titu_marker1(H)) + \
        w(has_titu_marker2(H))
    
    return [r2_0, r2_1, r2_1p]



