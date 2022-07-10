*(english version below)*

# Tagování českých vět pro automatické doplňování čárek
### Richard Klíma - NPRG045 (2021/2022)

Cílem tohoto projektu je vytvořit program pro tagování českých vět pro úlohu doplňování
interpunkčních čárek do těchto vět. Program je rozdělen na několik logických celků podle toho,
jak probíhá zpracování zkušebních dat.

## 1) Přehled

Celý projekt se skládá z&nbsp;několika částí, které se zabývají jednotlivými kroky od přípravy
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
třídy Pythonu, které umí pracovat s&nbsp;XML soubory. Každý ze souborů z&nbsp;PDT byl nejprve
scanován  pro zjištění ID vět, které se ve všech souborech vyskytují. Podle ID vět, které byly
v&nbsp;obou vrstvách PDT, pak byly tyto věty spárovány a použity. Věty, které se vyskytovaly
pouze v&nbsp;jedné vrstvě, nebyly pro účel tohoto projektu využity.

Parsování jednotlivých typů souborů bylo provedeno v&nbsp;několika krocích. Nejprve byly věty
naparsovány do přechodného formátu, kde na prvním řádku je ID věty a na následujících řádcích
jednotlivá slova a jejich atributy. Prázdný řádek odděluje věty.

Z&nbsp;tohoto přechodného souboru pak byly věty přečteny a rozděleny do dvou souborů, kde
v&nbsp;prvním souboru jsou všechny věty obsahující alespoň jednu čárku a v&nbsp;druhém souboru
věty bez čárky. Tyto soubory jsou takto připravené pro tagger.

#### II) Tagger
Tagger pracuje s&nbsp;daty předpřipravenými parserem. Načte jednotlivé věty a prochází jejich
slova, ze kterých postupně určuje hodnoty jednotlivých tagů. Pro srovnání dvou různých přístupů
vytvoříme dvě verze tagů - první verze obsahuje pouze informace z&nbsp;morfologické vrstvy, druhá
obsahuje navíc informace, které lze nalézt v&nbsp;syntaktické vrstvě. Každou větu máme tedy
otagovanou dvěma způsoby a takto otagované věty jsou uložené ve čtyřech souborech
(s&nbsp;čárkou/bez&nbsp;čárky, se&nbsp;syntaktickou&nbsp;vrstvou/bez&nbsp;syntaktické&nbsp;vrstvy)

**i. Tagy pouze z&nbsp;morfologické vrstvy**

<code>words</code> - počet slov ve větě<br>
<code>verbs</code> - počet sloves v&nbsp;určitém tvaru<br>
<code>genitive</code> - počet podstatných jmen ve 2. pádě<br>
<code>vocative</code> - počet podstatných jmen v&nbsp;5. pádě<br>
<code>common_phrases</code> - počet ustálených frází, ve kterých se píše čárka<br>
<code>subordinate</code> - počet podřadicích spojek ve větě<br>
<code>non_subordinate</code> - počet souřadicích spojek ve větě<br>
<code>conj_that</code> - počet ***že*** ve větě<br>
<code>conj_sothat</code> - počet ***aby*** a jeho tvarů (***abys***, ***abychom***, ...)
ve větě<br>
<code>conj_if</code> - počet ***kdyby*** a jeho tvarů (***kdybys***, ***kdybychom***, ...)
ve větě

**ii. Tagy ze syntaktické vrstvy**

V&nbsp;případě tagování podle obou použitých vrstev PDT k&nbsp;výše popsaným tagům přibudou
ještě tagy určující větné členy. Z&nbsp;dostupných informací v&nbsp;syntaktické vrstvě byly
některé vynechány, protože buď popisují složitější syntaktické závislosti a není tedy
pravděpodobné, že přispějí k&nbsp;lepšímu natrénování modelu na psaní čárek, nebo by byly
zdvojené s&nbsp;již existujícími tagy z&nbsp;morfologické vrstvy (např. větný člen
<code>AuxC</code> určující podřadicí spojku), nebo nejsou pro úlohu doplňování čárek
relevantní (např. větný člen <code>AuxK</code> určující koncovou interpunkci věty). Pokud
ovšem význam tagu pro úlohu doplňování čárek nebyl zřejmý, byl tag ponechán (např. větný člen
<code>AuxO</code> určující nadbytečný element).

<code>adv</code> - příslovečné určení bez dalšího rozlišení<br>
<code>apos</code> - apozice v&nbsp;hlavním uzlu<br>
<code>atr</code> - přívlastek<br>
<code>atv</code> - doplněk (zavěšený na neslovesném členu)<br>
<code>atvv</code> - doplněk (zavěšený na slovese, protože druhý řídící člen chybí)<br>
<code>auxg</code> - jiné grafické symboly, které neukončují větu<br>
<code>auxo</code> - nadbytečný (odkazovací, emotivní) element<br>
<code>auxp</code> - primární předložka, nebo části sekundární předložky<br>
<code>auxr</code> - zvratné ***se***, které není předmětem, ani typu <code>AuxT</code><br>
<code>auxt</code> - neoddělitelné zvratné ***se***<br>
<code>auxv</code> - pomocné sloveso<br>
<code>auxy</code> - příslovce a částice, které nelze zařadit jinam<br>
<code>auxz</code> - zdůrazňovací sloveso<br>
<code>coord</code> - koordinační uzel pro souřadné spojení<br>
<code>obj</code> - předmět<br>
<code>pnom</code> - jmenná část přísudku se sponou být<br>
<code>pred</code> - přísudek<br>
<code>sb</code> - podmět

#### III) Model
Když jsou věty otagované taggerem, můžeme na nich natrénovat model. Pro natrénování byly použity
funkce modulu TensorFlow pro Python. Vstupem pro trénování modelu je pole polí tagů vět a pole
výsledných hodnot (počtů čárek v&nbsp;jednotlivých větách). Výsledný model by měl zvládnout
ze vstupní otaggované věty určit, kolik v&nbsp;ní má být čárek.

#### IV) Doplňování čárek do testovacích vět
Potom, co model určí počet čárek ve větě, ještě potřebujeme doplnit příslušný počet čárek
do věty. K&nbsp;tomu slouží doplňovací modul programu, který opět projde větu a určí slova,
před kterými by čárky měly být (pro každé slovo určí pravděpodobnost, že před ním má být čárka,
a doplní čárky před nejvíce pravděpodobných <code>k</code> slov pro <code>k</code> čárek
k&nbsp;doplnění do věty.
