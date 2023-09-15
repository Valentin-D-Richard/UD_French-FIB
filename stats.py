#!/usr/bin/env python3
#### Python script used to extract sentences
# and compile statitics about the syntactic structures
# of French interrogatives

import pandas as pd
import argparse as arg
import matplotlib.pyplot as plt
from grewpy import Request, Corpus, set_config
set_config("ud")

##### Global constant variables

# List of corpora (sentence id prefix)
SUBCORPORA = ["GSD", "ParisStories", "ParTUT", "Rhap",
           "Sequoia", "FQB"]
# List of interrogative word lemmas
QUS = ["combien", "comment", "lequel", "où", "pourquoi",
       "quand", "quel", "qecq", "qui", "quoi", "que"]

# Annotation scheme description
from requests.coveney import COVENEY_REQS
COVENEY = { # From [Coveney 2011]
    # yes-no (fr. totale):
    "ESV": "'est-ce que'", # Est-ce que les autres / ils sont partis ?
    "V-CL": "clitic inversion", # Sont-ils partis ?
    "GN_V-CL": "complex inversion", # Les autres sont-ils partis ?
    # constituent (fr. partielle):
    "SVQ": "in situ", # Ils sont partis où ?
    "QSV": "fronting (fr. antéposition)", # Où ils sont partis ?
    "QV-CL": "qu + clitic inversion", # Où sont-ils partis ?
    "Q_GN_V-CL": "qu + complex inversion", # Où les autres sont-ils partis ?
    "QV_GN": "qu + stylistic inversion", # Où sont partis les autres ?
    "seQkSV": "cleft", # C’est où qu’ils sont partis ?
    "QESV": "qu + 'est-ce que'", # Où est-ce qu’ils sont partis ?
    "QsekSV": "qu + 'est-ce que' variant", # Où c’est qu’ils sont partis ?
    "QkSV": "qu + complementizer", # Où qu’ils sont partis ?
    "Q=S_V": "subject qu", # Lesquels sont partis ?
    # hybrid
    "QEV_GN": "qu+ 'est-ce que' + stylistic inversion", # Avec qui est-ce que travaille nicole Dupont ?
    "Q=S_V-CL": "subject qu + clitic inversion", # De ces fillettes, lesquelles sont-elles les tiennes ?
    "E_GN_V-CL": "'est-ce que' + complex inversion", # Est-ce que demain les sauveteurs pourront-ils s’approcher des alpinistes en détresse ?
    "QE_GN_V-CL": "qu + 'est-ce que' + complex inversion" # Qu’est-ce que le rédacteur de la rubrique des chats écrasés entend-il par un pachyderme ?
}

RICHARD = {}

NO = {
    "all": "no grouping by annotation scheme category"
}

SCHEMES = {
    "coveney":(COVENEY, COVENEY_REQS),
    "richard":RICHARD, "no":NO}

##### Argument parser
description = "Extract sentences and compile statitics"
parser = arg.ArgumentParser(description=description,
                            prog="stats.py",
                            epilog="Credits: Valentin D. Richard 2023")
parser.add_argument("filenames", metavar="FILE",
                    nargs="+", help="a conll(u) enriched file")
message = '''Annotation scheme among:
coveney [Coveney 2011],
richard [Richard 2023],
no (doesn't aggregate on syntactic pattern)'''
parser.add_argument("-s", "--scheme", action="store",
                        choices=SCHEMES.keys(), dest="scheme",
                        default="coveney", nargs=1,
                        metavar="SCHEME", help=message)

args = parser.parse_args()
                          
##### Utils

def cat_req(scheme:str, cat:str) -> list:
    """Returns the request extracting pattern expressed by cat in scheme"""
    return SCHEMES[scheme][1][cat]


def subcorpus_req(subcorpus_name:str) -> tuple:
    """"Returns a request that the sentence comes from subcorpus_name"""
    return ("global",'sent_id = re"^'+ subcorpus_name +'_.*$"')

def qu_req(qu_lemma:str) -> tuple:
    """"Returns a request that the occurence has qu_lemma as
    interrogative word lemma"""
    return ("pattern",'Q[lemma = "'+ qu_lemma +'"]')

#### Main function
dict = {"subcorpus": SUBCORPORA}
dict.update({cat:0 for cat in SCHEMES[args.scheme][0].keys()})
frame = pd.DataFrame(dict)

corpus = Corpus(args.filenames)

# Computing occurence number par category and subcorpus
for cat in SCHEMES[args.scheme][0].keys():
    for i, subcorpus in enumerate(SUBCORPORA):
        request = Request()
        for elt in cat_req(args.scheme, cat):
            request.append(*elt)
        request.append(*subcorpus_req(subcorpus))
        frame[cat][i] = corpus.count(request)

print(frame)






