*(english version below)*

# Tagování českých vět pro automatické doplňování čárek
### Richard Klíma - NPRG045 (2021/2022)

## Specifikace
Tento ročníkový projekt zahrnuje parser datových souborů Prague Dependency Tree (PDT) verze 3.5 a značkovač českých
vět pro automatické doplňování interpunkčních čárek.

Parser z XML souborů získaných z PDT 3.5 udělá soubory, které jsou jednodušší pro použití ve značkovači (nepotřebujeme
tak podrobné informace o jednotlivých slovech, jak nabízí PDT 3.5).

Značkovač z uvedených upravených dat umí každou jednu větu označkovat pomocí tagů, následně je možné pomocí těchto tagů
natrénovat model strojového učení na doplňování interpunkčních čárek do českých vět.

Pokud chceme označkovat větu, která není součástí PDT 3.5, využijeme nástroje MorphoDiTa z repozitáře LINDAT/CLARIAH
k označkování jednotlivých slov morfologickými značkami. Z těchto značek pak opět můžeme označkovat větu tagy
pro strojové učení.

## Operační systém, jazyk, knihovny, vývojové prostředí
Projekt je psán pod operačním systémem Windows 10 v jazyce Python v IDE PyCharm od firmy JetBrains. Použité jsou
standardní knihovny pro Python a některé externí rozšíření (strojové učení, MorphoDiTa, ...).

---

# Tagging of Czech sentences for AI comma completion
### Richard Klíma - NPRG045 (2021/2022)

## Specification
This individual software project contains a parser of Prague Dependency Tree (PDT) data files for version 3.5 and 
a tagger of Czech sentences for AI comma completion.

The parser will create simpler files from PDT 3.5 XML files for the tagger (we don't need so many details for single
words, as presented in PDT 3.5).

The tagger will tag each and every sentence from modified data, using these tags we can then train a machine learning
model for comma completion to Czech sentences.

If we want to tag a sentence which is not a part of PDT 3.5, we use the MorphoDiTa tool from LINDAT/CLARIAH repository
to tag single words with morphological tags. We can tag the whole sentence from these word tags to form the tags
required for the machine learning model.

## OS, language, libraries, IDE
The project is written under Windows 10 OS in Python language with the PyCharm IDE from the company JetBrains. We use
standard Python libraries with several external modules (machine learning, MorphoDiTa, ...).