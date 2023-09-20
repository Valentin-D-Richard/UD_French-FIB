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

# Version a: with V as main verb

# ClauseType and anchor
a0_0 = cl.Snippet("0_0.")
a0_0.request = p(ch_anchor(V)) + w(cv.copaux(V,W)) + w(cv.is_qu_word(V))

richard_a = cl.DisjRule("richard_a", a0_0)


# Version b: with V auxiliary or copula

# ClauseType, copula or auxiliary and anchor
b0_0 = cl.Snippet("0_0.")
b0_0.request = p(ch_anchor(CH) + fininf_copaux(CH,V)) + \
    w(cv.has_left_fininf_aux(CH)) + w(cv.is_qu_word(CH)) + \
    w(cv.has_right_fininf_aux(CH)) + w(cv.has_right_fininf_cop(CH))

richard_b = cl.DisjRule("richard_b", b0_0)


# Version c: Q is UD clause head and V as auxiliary or copula

# ClauseType, is qu-word, copula or auxiliary and anchor
c0_0 = cl.Snippet("0_0.")
c0_0.request = p(ch_anchor(Q) + fininf_copaux(Q,V) + cv.is_qu_word(Q)) + \
    w(cv.has_left_fininf_aux(Q)) + \
    w(cv.has_right_fininf_aux(Q)) + w(cv.has_right_fininf_cop(Q))

richard_c = cl.DisjRule("richard_c", c0_0)



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
    
    return [r1_0, r1_1, r1_2]


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
    
    return [r2_0, r2_1, r2_1_alt]


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
def ipplace(H:str,MV:str) -> str:
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

    # cleft1
    



# Version a
richard_a.add_snippets(cm(V), a0_0)
richard_a.add_snippets(vm(V), a0_0)
qu_a = qu(V)
richard_a.add_snippets(qu_a, a0_0)
qu_a_snippet = qu_a[0]

# Version b
richard_b.add_snippets(cm(CH), b0_0)
richard_b.add_snippets(vm(CH), b0_0)
qu_b = qu(CH)
richard_b.add_snippets(qu_b, b0_0)
qu_b_snippet = qu_b[0]

# Version c
richard_c.add_snippets(cm(Q), c0_0)
richard_c.add_snippets(vm(Q), c0_0)
richard_c.add_snippets(c3_0, c0_0)
