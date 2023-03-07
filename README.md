# Summary
**UD_French-FIB** (French Interrogative Bank) is an extraction of sentences exhibiting an interrogative from French UD corpora.

# Introduction
**UD_French-FIB** (French Interrogative Bank) is an extraction of sentences exhibiting an interrogative from French UD corpora:
 * [UD_French-ParTUT](https://github.com/UniversalDependencies/UD_French-ParTUT) (written)
 * [UD_French-GSD](https://github.com/UniversalDependencies/UD_French-GSD) (written)
 * [UD_French-Sequoia](https://github.com/UniversalDependencies/UD_French-Sequoia) (written)
 * [UD_French-FQB](https://github.com/UniversalDependencies/UD_French-FQB) (written)
 * [UD_French-Rhaposide](https://github.com/UniversalDependencies/UD_French-Rhapsodie) (spoken)
 * [UD_French_ParisSotires](https://github.com/UniversalDependencies/UD_French-ParisStories) (spoken)
 * [UD_French-PUD](https://github.com/UniversalDependencies/UD_French-PUD) (written)

The identification of interrogatives clauses and the extraction were performed using the [FUDIA](https://github.com/Valentin-D-Richard/FUDIA) programme. 20 sentences were removed by hand because they were badly annotated, either due to an original annotation mistake, or due to limitations of FUDIA's heuristics.

## Changes wrt. original UD corpora

Some changes wrt. the original UD corpora have been made during the identification process. For more information about these changes, please check out the FUDIA documentation.

### Added features :
 * some missing `PronType="Rel"`
 * some missing `PronType="Int"`
 * `ClauseType="Int"` on interrogative clause heads
 * `PhraseType="Int"` on interrogative phrase heads

### Changed annotations
 * *tel quel* changed to fixed (with `ExtPos="ADJ"`) when it is not already the case
 * *n'importe + WH* changed to fixed: with `ExtPos="DET"` if `WH[lemma="quel"]`, `ExtPos="PRON"` if `WH[lemma="quoi"|"qui"|"lequel"]` and `ExtPos="ADV"` if `WH[lemma="comment"|"quand"|"où"]`, and with consequent head shift
 * *est-ce que* changed to fixed with `ExtPos="SCONJ"`, the head shifted to the interrogative clause head CL_HEAD, and the main relation changed to `mark(CL_HEAD,est)`
 * *qu'est-ce que* changed to fixed with `ExtPos="PRON"`, the head shifted to the interrogative clause head CL_HEAD, and the relations changed to `obj`, `obl` or `nsubj` from CL_HEAD to *qu'*, depending on the context
 * *WH + que + S'* with *que* attached to WH, changed to govern *que* by the head of S'


## Splitting
The whole corpus contains 38,898 tokens in 2,973 sentences.

In **UD_French-FIB**, data are split into:

 * `fr_fib-ud-test.conllu`: 2,386 tokens in 115 sentences
   * using GSD test, ParisStories test, ParTUT test, Rhaposodie test and Sequoia test
 * `fr_fib-ud-dev.conllu`: 2,365 tokens in 130 sentences
   * using GSD dev, ParisStories dev, ParTUT dev, Rhaposodie dev and Sequoia dev
 * `fr_fib-ud-train.conllu`: 34,147 tokens in 2,728 sentences
   * using FQB test, GSD train, ParisStories train, ParTUT train, PUD test, Rhaposodie train and Sequoia train

## Enriched versions

For each set, an enriched version is provided. The enriched version contains the same sentences but with additional edges and features:
 * edges `cue:wh` from the head of the interrogative clause to the interrogative proform(s) associated
 * edges `cue:wh` from the head of the interrogative phrase to the interrogative proform(s) associated
 * edged `cue:mark` from the head of the interrogative clause to the interrogative marker
 * feature `Quoted="Yes"` for quoted segments

For more information, see the [FUDIA documentation](https://github.com/Valentin-D-Richard/FUDIA/blob/main/FUDIA_README.md).

## Genres
The corpus contains written sentences and trasncriptions of spoken sentences. More about the different genres is to be found in the documentation of the original corpora.

# References


# Changelog



=== Machine-readable metadata (DO NOT REMOVE!) ================================
Data available since: UD v2.0
License: LGPL-LR
Includes text: yes
Genre: wiki medical news nonfiction legal blog reviews spoken
Lemmas: converted from manual
UPOS: converted from manual
XPOS: not available
Features: converted from manual
Relations: converted from manual
Contributing: elsewhere
===============================================================================
