#!/usr/bin/env python3
#### Python script used to extract sentences
# and compile statitics about the syntactic structures
# of French interrogatives

import pandas as pd
import argparse as arg
import matplotlib.pyplot as plt
import grewpy as gp
gp.set_config("ud")

##### Global constant variables

FORMATS = ["txt", "csv", "json", "plot", "sents", "graphs"]

# List of corpora (sentence id prefix)
SUBCORPORA = ["FQB", "Sequoia", "GSD", "ParTUT", "PUD", "Rhap",
              "ParisStories"]
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

MODULAR = {}

from requests.no import NO_REQS
NO = {
    "all": "no grouping by annotation scheme category"
}

SCHEMES = {
    "coveney":(COVENEY, COVENEY_REQS),
    "modular":MODULAR, "no":(NO, NO_REQS)}

##### Argument parser
description = "Extract sentences and compile statitics"
parser = arg.ArgumentParser(description=description,
                            prog="stats.py",
                            epilog="Credits: XXX") # to change
parser.add_argument("filenames", metavar="FILE",
                    nargs="+", help="a conll(u) enriched file")
message = '''Annotation scheme, among:
coveney [Coveney 2011],
modular ,
no (doesn't aggregate on syntactic pattern)'''
parser.add_argument("-s", "--scheme", action="store",
                        choices=SCHEMES.keys(), dest="scheme",
                        default=["coveney"], nargs=1,
                        metavar="SCHEME", help=message)
message = 'Output format, among: txt (default), csv, json, plot'
parser.add_argument("-f", "--format", action="store",
                        choices=FORMATS, dest="format",
                        default=["txt"], nargs=1,
                        metavar="FORMAT", help=message)
message = 'Subcorpora included, among: '+', '.join(SUBCORPORA)
parser.add_argument("-i", "--include", action="store",
                        choices=SUBCORPORA, dest="include",
                        default=SUBCORPORA, nargs="+",
                        metavar="SUBCORPUS", help=message)
message = 'Subcorpora to exclude, among: '+', '.join(SUBCORPORA)
parser.add_argument("-e", "--exclude", action="store",
                        choices=SUBCORPORA, dest="exclude",
                        default=[], nargs="+",
                        metavar="SUBCORPUS", help=message)

#### Retrieving arguments

args = parser.parse_args()
subcorpora = [sc for sc in args.include if sc not in args.exclude]
scheme = args.scheme[0]
o_format = args.format[0]
                          
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

def elt_subcorpus_req(elt_list:list, subcorpus:str) -> gp.Request:
    """Returns a grew Request from a given request list elt_list
     (of a given category) and a subcorpus"""
    request = gp.Request()
    for elt in elt_list:
        request.append(*elt)
    request.append(*subcorpus_req(subcorpus))
    return request

def search_res(corpus: gp.Corpus, cat:str, subcorpus:str) -> list:
    """Returns the result of the search request on category cat
    and subcorpus"""
    res = []
    for elt_list in cat_req(scheme, cat):
        res += corpus.search(elt_subcorpus_req(elt_list, subcorpus))
    return res

def add_totals(df:pd.DataFrame) -> ():
    """"Adds a column with total on row and a line with totals on columns"""
    df['Total'] = df.sum(axis=1,numeric_only=True) # column
    nb = len(frame.index)
    df.loc[nb]= df.sum() # row
    df.loc[nb,"subcorpus"] = "Total"


#### Main function
dict = {"subcorpus": subcorpora}
dict.update({cat:0 for cat in SCHEMES[scheme][0].keys()})
frame = pd.DataFrame(dict)

corpus = gp.Corpus(args.filenames)

# Computing occurence number par category and subcorpus
if o_format != "sents" and o_format != "graphs":
    for cat in SCHEMES[scheme][0].keys():
        for i, subcorpus in enumerate(subcorpora):
            frame.at[i,cat] = 0

            # Adding the counts of the different requests
            # defined in requests/<scheme>.py
            for elt_list in cat_req(scheme, cat):
                request = elt_subcorpus_req(elt_list, i)
                try:
                    frame.at[i,cat] += corpus.count(request)
                    
                # Anticipating errors in module requests
                except (gp.grew.GrewError,UnicodeDecodeError) as err:
                    print("##### Some error occured at "+cat+" while parsing the request:")
                    print(request)
                    print("#####")
                    raise gp.grew.GrewError(err)

    add_totals(frame)

if o_format == "sents" or o_format == "graphs":
    # Concatenating the list of results of search requests
    for cat in SCHEMES[scheme][0].keys():
        frame[cat] = frame.apply(
            lambda idx: search_res(corpus, cat, idx[0]), axis=1
        )


##### Rendering output

if o_format == "csv":
    print(frame.to_csv())

elif o_format == "json":
    print(frame.to_json())

elif o_format == "plot":
    
    # ploting all corpora on the same plot
    title = "Distribution of French interrogatives "
    title += " ("+args.scheme[0]+" scheme)"
    frame.index = frame["subcorpus"]
    frame = frame[:-1].T[1:-1] # removing totals
    frame.plot(kind='bar', title=title)
    plt.xticks(rotation = 45)
    plt.show()

elif o_format == "sents":

    # Printing the list of sentences
    for cat in SCHEMES[scheme][0].keys():
        print("########## Category:", cat)
        for i, subcorpus in enumerate(subcorpora):
            print("##### Corpus:", subcorpus)
            sents = set([corpus.get(sent['sent_id']).json_data()
                        ['meta']['text'] for sent in frame.at[i,cat]])
            print('\n'.join(sents))

elif o_format == "graphs":

    # Creating a dot file for every sentences
    for cat in SCHEMES[scheme][0].keys():
        for i, subcorpus in enumerate(subcorpora):
            for sent in frame.at[i,cat]:
                dot = corpus.get(sent['sent_id']).to_dot()
                print(dot)


else:
    print(frame)






