*(english version below)*

# Tagování českých vět pro automatické doplňování čárek
### Richard Klíma - NPRG045 (2021/2022)

Cílem tohoto projektu je vytvořit program pro taggování českých vět pro úlohu doplňování
interpunkčních čárek do těchto vět. Program je rozdělen na několik logických celků podle toho,
jak probíhá zpracování zkušebních dat.

## 1) Přehled

Celý projekt se zkládá z&nbsp;několika částí, které se zabývají jednotlivými kroky od přípravy
a parsování dat, až po vytvoření modelu pro automatické doplňování interpunkčních čárek.

Základním stavebním kamenem jsou zkušební data, podle kterých se bude model učit čárky
doplňovat. Pro tento účel byla vybrána data z&nbsp;Prague Dependency Treebank 3.5 (dále jen PDT)
z&nbsp;repozitáře LINDAT/CLARIAH-CZ. Ze tří vrstev dat dostupných v&nbsp;PDT byly pro účely tohoto
projektu vybrány morfologická a syntaktická, tedy s&nbsp;tektogramatickou vrstvou tento projekt
nepracuje. Tato data byla rozbalena z&nbsp;archivů a následně upravena pomocí parseru do
zvoleného formátu.

Data ve zvoleném formátu následně zpracovává tagger vět, který ke každé větě přiřadí číselné pole
tagů, které slouží k&nbsp;natrénování modelu pro automatické doplňování čárek. Tagger při
značkování vět bere v&nbsp;potaz např.&nbsp;počty některých slovních druhů ve větě, počty oslovení,
počty ustálených frází, apod. Pro nalezení ustálený frází, ve kterých se píše čárka, byl vytvořen
samostatný *hledač* frází.

## 2) Podrobný popis částí projektu
### a) Kód
#### I) Parser
Data z&nbsp;obou použitých vrstev PDT jsou ve formátu XML, k&nbsp;parsování tedy byly použity
třídy Pythonu, které umí pracovat s XML soubory. Každý ze souborů z PDT byl nejprve scanován pro
zjištění ID vět, které se ve všech souborech vyskytují. Podle ID vět, které byly v obou vrstvách
PDT, pak byly tyto věty spárovány a použity. Věty, které se vyskytovaly pouze v jedné vrstvě,
nebyly pro účel tohoto projektu využity.

Parsování jednotlivých typů souborů bylo provedeno v několika krocích. Nejprve byly věty
naparsovány do přechodného formátu, kde na prvním řádku je ID věty a na následujících řádcích
jednotlivá slova a jejich atributy. Prázdný řádek odděluje věty.

Z tohoto přechodného souboru pak byly věty přečteny a rozděleny do dvou souborů, kde v prvním
souboru jsou všechny věty obsahující alespoň jednu čárku a v druhém souboru věty bez čárky.
Tyto soubory jsou takto připravené pro tagger.
