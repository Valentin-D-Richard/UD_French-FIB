#!/usr/bin/env python3
#### Python script used to extract sentences
# and compile statitics about the syntactic structures
# of French interrogatives

import pandas as pd
import argparse as arg
import os
import matplotlib.pyplot as plt
import grewpy as gp
gp.set_config("ud")

##### Global constant variables

FORMATS = ["txt", "csv", "json", "plot", "sents", "html", "svg", "png"]
SENT_FORMATS = ["sents", "html", "svg", "png"]

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

from requests.modular import MODULAR_REQ
MODULAR = {}

from requests.no import NO_REQS
NO = {
    "all": "no grouping by annotation scheme category"
}

SCHEMES = {
    "coveney":COVENEY_REQS,
    "modular":MODULAR_REQ, "no":NO_REQS}

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
    return SCHEMES[scheme][cat]

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
        res += corpus.search(elt_subcorpus_req(elt_list, subcorpus), deco=True)
    return res

def add_totals(df:pd.DataFrame) -> ():
    """"Adds a column with total on row and a line with totals on columns"""
    df['Total'] = df.sum(axis=1,numeric_only=True) # column
    nb = len(frame.index)
    df.loc[nb]= df.sum() # row
    df.loc[nb,"subcorpus"] = "Total"


#### Main function
dict = {"subcorpus": subcorpora}
dict.update({cat:0 for cat in SCHEMES[scheme].keys()})
frame = pd.DataFrame(dict)

corpus = gp.Corpus(args.filenames)

# Computing occurence number par category and subcorpus
if o_format not in SENT_FORMATS:
    for cat in SCHEMES[scheme].keys():
        for i, subcorpus in enumerate(subcorpora):
            frame.at[i,cat] = 0

            # Adding the counts of the different requests
            # defined in requests/<scheme>.py
            for elt_list in cat_req(scheme, cat):
                request = elt_subcorpus_req(elt_list, subcorpus)
                try:
                    frame.at[i,cat] += corpus.count(request)
                    
                # Anticipating errors in module requests
                except (gp.grew.GrewError,UnicodeDecodeError) as err:
                    print("##### Some error occured at "+cat+" while parsing the request:")
                    print(request)
                    print("#####")
                    raise gp.grew.GrewError(err)

    add_totals(frame)

else:
    # Concatenating the list of results of search requests
    for cat in SCHEMES[scheme].keys():
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
    for cat in SCHEMES[scheme].keys():
        print("########## Category:", cat)
        for i, subcorpus in enumerate(subcorpora):
            print("##### Corpus:", subcorpus)
            sents = set([corpus[sent['sent_id']].json_data()
                        ['meta']['text'] for sent in frame.at[i,cat]])
            print('\n'.join(sents))

elif o_format == "html":

    # Printing the list of sentences
    for cat in SCHEMES[scheme].keys():
        print("<h2>Category: "+cat+"</h2>")
        for i, subcorpus in enumerate(subcorpora):
            print("<h3>Corpus: "+subcorpus+"</h3>")
            for match in frame.at[i,cat]:
                sent_id = match['sent_id']
                deco = match['deco']
                print(corpus[sent_id].to_sentence(deco=deco))

elif o_format == "svg" or o_format == "png":
    dir = "results/svg/"
    prev_sent_id = ""
    i = 2

    # Creating a dot file for every sentences
    for cat in SCHEMES[scheme].keys():
        subdir = cat+"/"
        # creates the directory if it does not exist
        if not os.path.exists(dir + subdir):
            os.makedirs(dir + subdir)

        # Creates a svg/png out of every match
        for i, subcorpus in enumerate(subcorpora):
            for match in frame.at[i,cat]:
                sent_id = match['sent_id']
                deco = match['deco']
                filename = dir + subdir + sent_id

                # Checking filename to avoid collisions
                if prev_sent_id == sent_id:
                    filename += "___" + str(i)
                    i += 1
                else:
                    prev_sent_id = sent_id
                    i = 2

                if o_format == "svg":
                    filename += ".svg"
                    with open(filename, "w") as f:
                        f.write(corpus[sent_id].to_svg(deco=deco))

                if o_format == "png":
                    filename += ".png"
                    with open(filename, "w") as f:
                        f.write(corpus[sent_id].to_svg(deco=deco))
                        # Transformaing transparent by white background
                        cmd = "convert "+filename+"  -background white "
                        cmd += "-alpha remove -flatten -alpha off "+filename
                        os.system(cmd)

else:
    print(frame)






