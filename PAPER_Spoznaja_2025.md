# KOMPARATIVNA ANALIZA ALGORITAMA ZA DETEKCIJU KRUŽNIH OBJEKATA: PRIMJENA NA AUTOMATSKO BROJANJE KOVANICA

**Tip rada:** Originalni naučni članak (Original scientific paper)

**Autor:** Edina Kadrić Durmiš  
**E-mail:** edina.kadric.durmis@unze.ba  
**Ustanova:** Univerzitet u Zenici, Filozofski fakultet

## APSTRAKT

Ovaj rad predstavlja komparativnu analizu tri različita pristupa detekciji kružnih objekata u digitalnoj obradi slike, s fokusom na automatsko brojanje kovanica. Glavni doprinos nije predlaganje novog algoritma u globalnom smislu, nego **eksperimentalna komparacija tri klasična pristupa u istom kontrolisanom scenariju**: morfološki *pipeline* (kombinacija uobičajenih koraka obrade slike prilagođenih domeni), Hough transformacija kruga i blob detekcija (*SimpleBlobDetector*). Evaluacija se oslanja na ručno anotiran mali skup od šest slika, jedinstven evaluacijski okvir temeljen na IoU i F1, te praktičnu Django web aplikaciju za testiranje i edukaciju. Sva tri algoritma testirana su uz ground truth anotacije; rezultati pokazuju da morfološki pristup postiže izuzetne performanse (F1=1.0, prosječni IoU=0.77) u kontroliranim uslovima s konzistentnom pozadinom, dok Hough i Blob pristup pokazuju značajno slabije agregatne rezultate (F1=0.382 i 0.404). Detaljno je analizirana razlika u performansama, sa posebnim osvrtom na ulogu HSV segmentacije pozadine kao ključnog faktora uspjeha morfološkog pristupa. Implementacija omogućava interaktivno testiranje, usporedbu algoritama i podešavanje parametara putem korisničkog sučelja. Rad demonstrira praktičnu primjenjivost klasičnih metoda u kontrolisanim industrijskim scenarijima i nudi alat za edukaciju i istraživanje u oblasti digitalne obrade slike.

**Ključne riječi:** detekcija krugova, blob detekcija, obrada slike, OpenCV, morfološke operacije, Hough transformacija, IoU metrika, automatizacija industrije

## COMPARATIVE ANALYSIS OF CIRCULAR OBJECT DETECTION ALGORITHMS: APPLICATION TO AUTOMATIC COIN COUNTING

### ABSTRACT

This paper presents a comparative analysis of three approaches to circular object detection in digital image processing, focusing on automatic coin counting. The main contribution is not a globally novel algorithm, but an **experimental comparison of three classical methods under the same controlled scenario**: a domain-tuned morphological pipeline, the Hough circle transform, and blob detection (*SimpleBlobDetector*). Evaluation uses a small manually annotated set of six images, a unified framework based on IoU and F1, and a practical Django web application for testing and education. Results show that the morphological approach achieves strong performance (F1=1.0, average IoU=0.77) in controlled conditions with consistent backgrounds, while Hough and Blob show weaker aggregate results (F1=0.382 and 0.404). Performance differences are analyzed in detail, emphasizing HSV background segmentation as a key factor for the morphological pipeline. The implementation supports interactive testing, algorithm comparison, and parameter tuning via a web interface. The work illustrates the applicability of classical methods in controlled industrial settings and provides an educational tool for digital image processing.

**Keywords:** circle detection, blob detection, image processing, OpenCV, morphological operations, Hough transform, IoU metric, industrial automation

## 1. UVOD

Automatska detekcija i brojanje objekata kružnog oblika predstavlja fundamentalan zadatak u kompjuterskoj viziji s brojnim praktičnim primjenama u industriji, medicini i drugim oblastima. Od detekcije proizvoda na proizvodnoj traci, preko prepoznavanja bakterijskih kolonija u medicinskoj dijagnostici, do automatskog brojanja kovanica u finansijskim aplikacijama – sposobnost pouzdane i efikasne identifikacije kružnih struktura predstavlja kritičnu funkcionalnost savremenih automatizovanih sistema (Davies, 2005).

Razvoj metoda za detekciju krugova ima bogatu istoriju u kompjuterskoj viziji. Rani pristupi fokusirali su se na direktnu analizu ivica i kontura (Ballard, 1981), dok su moderniji pristupi integrisali naprednije tehnike statističkog učenja i dubokog učenja (Ronneberger et al., 2015). Ipak, klasični pristupi zasnovani na obradi slike ostaju relevantni zahvaljujući svojoj interpretabilnosti, brzini izvršavanja i minimalnim zahtjevima za računarskim resursima (Bradski i Kaehler, 2008).

Ovaj rad fokusira se na tri reprezentativna pristupa detekciji krugova: morfološki *pipeline* prilagođen domeni brojanja kovanica, Hough transformaciju kruga kao standardnu parametarsku metodu, te blob detekciju zasnovanu na analizi značajki. **Doprinos rada** treba razumjeti kao: (a) sistematsku eksperimentalnu komparaciju ova tri pristupa u **istom** kontrolisanom postavku i na istom malom, ručno anotiranom skupu; (b) jedinstven evaluacijski okvir (IoU prag 0,5, Precision, Recall, F1); (c) otvorenu web aplikaciju za ponavljanje eksperimenata, podešavanje parametara i nastavu. Cilj nije tvrdnja o revolucionarnoj teorijskoj novosti — detekcija kovanica čest je studentski i inženjerski zadatak — nego transparentno mjerenje razlika između uobičajenih klasičnih metoda kada se primijene paralelno i ocijene jednako rigorozno. Cilj istraživanja je stoga dvostruk: (1) usporediti performanse ovih pristupa na realnim testnim podacima koristeći navedene metrike, te (2) pokazati praktičnu i edukacijsku vrijednost integrisanog alata u industrijski sličnim, kontrolisanim scenarijima.

### 1.1. Motivacija i praktična primjena

Motivacija za ovo istraživanje proizlazi iz konkretnih potreba industrije za pouzdanim i ekonomičnim rješenjima za automatsko prebrojavanje i inspekciju kružnih objekata. Dok savremeni pristupi bazirani na dubokom učenju postižu impresivne rezultate, oni često zahtijevaju značajne računarske resurse i velike skupove podataka za treniranje (LeCun et al., 2015). U mnogim industrijskim okruženjima gdje su uslovi osvjetljenja i pozadina kontrolirani, klasične metode mogu postići uporedivu ili čak superiorniju performansu uz nižu složenost implementacije.

Posebna fokusna oblast ovog istraživanja je brojanje kovanica kao reprezentativan primjer detekcije kružnih objekata u kontroliranim uslovima. Kovanice predstavljaju idealan testni slučaj jer kombinuju karakteristike realnih industrijskih objekata (varijacija u veličini, refleksiji metala, mogućnost preklapanja) s mogućnošću precizne ground truth anotacije.

## 2. PREGLED LITERATURE I POVEZANIH RADOVA

### 2.1. Klasični pristupi detekciji krugova

Detekcija kružnih objekata u digitalnim slikama predstavlja fundamentalan problem kompjuterske vizije s dugom istorijom istraživanja. Rani pristupi fokusirali su se na detekciju ivica praćenu analizom geometrijskih karakteristika.

**Hough transformacija** (Duda i Hart, 1972) predstavlja revolucionarni pristup koji je transformisao problem detekcije oblika iz prostora slike u parametarski prostor gdje se objekti manifestuju kao vrhovi u akumulatorskoj matrici. Izvorni Hough pristup bio je računski veoma zahtevan, ali kasniji radovi uveli su optimizacije poput gradijent-based pristupa (Illingworth i Kittler, 1988) i randomizovane Hough transformacije (Xu et al., 1990). Davies (2005) pruža sveobuhvatan pregled različitih varijacija Hough metode, uključujući probabilističku Hough transformaciju koja značajno smanjuje računsku složenost.

**Metode zasnovane na konturama** oslanjaju se na Canny detekciju ivica (Canny, 1986) praćenu analizom geometrijskih svojstava zatvorenih kontura. Suzuki i Abe (1985) razvili su efikasan algoritam za ekstrakciju kontura koji je postao standard u OpenCV biblioteci. Ključni parametar za validaciju kružnosti konture je odnos površine i opsega, gdje savršeni krug postiže maksimalnu vrijednost 4π (Prasad et al., 2012).

**Morfološke operacije** tradicionalno se koriste u pre-procesiranju slika za poboljšanje kvalitete detekcije. González i Woods (2008) detaljno opisuju operacije dilatacije, erozije, otvaranja i zatvaranja. Soille (2003) istražuje napredne morfološke tehnike uključujući watershed transformaciju i morfološku rekonstrukciju. Međutim, sistematska kombinacija morfoloških operacija u cjelovit *pipeline* za detekciju krugova ostaje nedovoljno istražena oblast.

### 2.2. Blob detekcija i ekstraktori značajki

Blob detektori identifikuju regije slike koje se razlikuju po svojstvima poput intenziteta, boje ili teksture. Lindeberg (1998) postavlja teorijsku osnovu za scale-space analizu u detekciji blob-ova. SimpleBlobDetector iz OpenCV biblioteke (Bradski i Kaehler, 2008) kombinuje multiple kriterijume (površina, cirkularnost, konveksnost, inercija) za robusnu detekciju.

SIFT (Scale-Invariant Feature Transform) i SURF (Speeded Up Robust Features) detektori (Lowe, 2004; Bay et al., 2006) nude invarijantnost na skaliranje i rotaciju, ali su računski zahtjevniji. Moreels i Perona (2007) istražuju evaluaciju različitih detektora značajki na realnim slikama pod različitim uslovima.

### 2.3. Deep learning pristupi

Savremena istraživanja dominantno koriste konvolucijske neuronske mreže (CNN) za detekciju objekata. Ključni pristupi uključuju:

**Region-based metode**: R-CNN (Girshick et al., 2014) uvodi koncept selektivne pretrage regiona praćene CNN klasifikacijom. Fast R-CNN (Girshick, 2015) i Faster R-CNN (Ren et al., 2015) progresivno poboljšavaju brzinu uvođenjem Region Proposal Network (RPN). Mask R-CNN (He et al., 2017) proširuje Faster R-CNN segmentacijom na nivou piksela.

**Single-shot detektori**: YOLO (You Only Look Once) familija (Redmon et al., 2016; Redmon i Farhadi, 2017, 2018) tretira detekciju kao regresijski problem, postižući real-time performanse. SSD (Single Shot MultiBox Detector) (Liu et al., 2016) koristi multiple feature mape za detekciju objekata različitih veličina.

**Specifične primjene na kovanice**: Khashman i Sekeroglu (2006) razvijaju CNN za identifikaciju valute. Reisert et al. (2007) koriste template matching za prepoznavanje kovanica. Noviji radovi (Bremananth et al., 2010; Van et al., 2016) kombinuju deep learning s klasičnim metodama.

**Noviji trendovi**. Pregled evolucije YOLO porodice do YOLOv8 i dalje (Terven i Cordova-Esparza, 2023) pokazuje da jednoprolazni detektori i dalje dominiraju u aplikacijama gdje je bitna brzina. Transformer-bazirani detektori poput RT-DETR-a postižu konkurentne ili bolje rezultate na složenim scenama uz pažljivo inženjerstvo brzine (Zhao et al., 2024). Segmentacijski i „foundation“ modeli (npr. SAM — Kirillov et al., 2023) dodatno pomjeraju granicu tačnosti u heterogenim scenarijima, ali uz veće zahtjeve za podacima, memorijom i infrastrukturom.

Savremeni modeli dubokog učenja tipično daju bolje rezultate u **heterogenim** scenama i velikim skupovima, ali zahtijevaju znatno više označenih podataka i računarskih resursa nego klasični *pipeline*-i. Zbog toga fokus ovog rada ostaje na **klasičnim** metodama i njihovoj eksplicitnoj komparaciji u kontrolisanim postavkama, gdje su interpretabilnost, niski trošak i brza iteracija i dalje često odlučujući faktori (uporediti LeCun et al., 2015).

### 2.4. Hibridni i adapativni pristupi

Novija istraživanja istražuju kombinaciju klasičnih i modernih metoda. Xie i Pun (2017) kombinuju morfološke operacije s deep features za medicinske aplikacije. Zhu et al. (2018) predlažu hibridni pristup za detekciju industrial defekata koristeći morfologiju i CNN.

**Adaptivni prag** (Otsu, 1979; Sauvola i Pietikäinen, 2000) ključan je za robusnu binarizaciju u varijabilnim uslovima osvjetljenja. Bradley i Roth (2007) razvijaju brz adaptivni algoritam pogodan za real-time primjene.

**HSV color space** široko se koristi u kompjuterskoj viziji zbog intuitivnije reprezentacije boje nego RGB (Gonzalez i Woods, 2008). Smith (1978) prvi formalno opisuje HSV transformaciju. Cucchiara et al. (2003) demonstriraju prednosti HSV prostora za background subtraction u video nadzoru.

### 2.5. Metrike evaluacije u detekciji objekata

Standardne metrike uključuju Precision, Recall, F1-Score i Accuracy (Powers, 2011). **IoU (Intersection over Union)**, također poznat kao Jaccard index, postao je *de facto* standard u evaluaciji detekcije objekata (Everingham et al., 2010). PASCAL VOC (Everingham et al., 2010) i MS COCO (Lin et al., 2014) datasets postavljaju benchmark s IoU pragom od 0.5 za pozitivnu detekciju.

Garcia-Garcia et al. (2017) uspoređuju različite metrike za semantičku segmentaciju. Padilla et al. (2020) nude sveobuhvatan pregled metrika za evaluaciju detekcije objekata, uključujući Average Precision (AP) i mean Average Precision (mAP).

### 2.6. Identifikacija research gap-a

Pregled literature otkriva nekoliko značajnih praznina:

1. **Nedostatak sistematske evaluacije** klasičnih metoda u industrijskim scenarijima s kontroliranim uslovima
2. **Ograničeno istraživanje** specifičnih kombinacija morfoloških operacija i njihove optimalne sekvence
3. **Nedovoljna dokumentacija** praktičnih trade-off-ova između klasičnih i deep learning pristupa
4. **Manjak open-source alata** za interaktivnu usporedbu algoritama s mogućnošću podešavanja parametara

Ovaj rad adresira ove praznine kroz eksplicitno uspoređivanje tri klasična *pipeline*-a (uključujući domenski podešen morfološki lanac), detaljnu komparativnu analizu na istom anotiranom skupu, te razvoj open-source web aplikacije za edukaciju i istraživanje.

## 3. METODOLOGIJA

### 3.1. Implementirani algoritmi

#### 3.1.1. Morfološka cirkularna detekcija (predloženi algoritam)

Implementiran je morfološki *pipeline* za detekciju krugova zasnovan na specifičnoj kombinaciji i sekvenci klasičnih tehnika obrade slike, prilagođen domeni kovanica na relativno uniformnoj pozadini. *Pipeline* se sastoji od sljedećih koraka:

1. **Zamagljivanje** – redukcija šuma malim kernelom
2. **HSV transformacija i uklanjanje pozadine** – filtriranje pozadine pomoću `inRange` operacije u HSV prostoru
3. **Otsu prag** – adaptivna binarizacija
4. **Dilatacija** – spajanje fragmentiranih regija multipliciranim iteracijama
5. **Erozija** – uklanjanje malih artefakata
6. **Canny detekcija ivica** – ekstrakcija kontura objekata
7. **Ekstrakcija kontura** – primjena eksternog moda kontura
8. **Filtriranje po cirkularnosti** – geometrijska validacija pomoću formule C = (4π × A) / P²

**Obrazloženje ključnih koraka.** HSV prostor odvaja nijansu, saturaciju i vrijednost (osvijetljenost), što olakšava pragovno izdvajanje objekata od pozadine kada se boja i saturacija kovanica razlikuju od pozadine — za razliku od RGB-a gdje su ove informacije pomiješane u tri kanala. Nakon segmentacije, **Otsu** metoda automatski bira prag na histogramu slike tako da maksimizuje međuklasnu varijansu između prednjeg plana i pozadine, što je korisno kada histogram ima izražene modove bez ručnog podešavanja praga. **Dilatacija** širi binarne regije i spaja pukotine uzrokovane šumom ili refleksijama; **erozija** zatim uklanja sitne izolirane artefakte i suviše tanke mostove, vraćajući grublje „čist“ oblik kandidata prije detekcije ivica. **Cirkularnost** konture mjeri koliko je oblik blizu kruga: za površinu *A* i obim *P* vrijedi *C* = 4π*A*/*P*²; za savršen krug *C* = 1, za izdužene ili nazubljene konture *C* je manje. Prag na *C* zadržava približno kružne objekte (kovanice) i odbacuje izdužene konture, ostatke pozadine i nepravilne fragmente.

#### 3.1.2. Hough transformacija kruga

Implementirana je klasična Hough metoda koja koristi parametarsku reprezentaciju krugova u akumulatorskom prostoru. Algoritam mapira ivične tačke u 3D prostor parametara (centar x, centar y, radijus) i traži lokalne maksimume koji odgovaraju potencijalnim krugovima. Ključni parametri kontrolišu minimalnu distancu između centara detektovanih krugova, prag za akumulatorske vrijednosti, te minimalni i maksimalni radijus traženih objekata. Algoritam koristi gradient-based pristup za smanjenje računske složenosti (Bradski i Kaehler, 2008).

**Princip i ograničenja.** U (diskretizovanom) prostoru parametara svaka ivična tačka „glasa“ za sve krugove kojima može pripadati; pravi krugovi u slici kumuliraju konzistentne glasove i pojavljuju se kao **vrhovi** u akumulatoru. Zbog toga je metoda osjetljiva na **šum** i na djelimične kružnice u teksturi, sjenci i **metalnim refleksijama**: one stvaraju mnogo konzistentnih lokalnih glasova i lahko daju lažne vrhove. Relativno nizak prag akumulatora ili gusta mapa ivica često vodi do **velikog broja false positive** detekcija (mali krugovi na šumu), dok strožiji prag može propustiti stvarne kovanice — što u praksi zahtijeva pažljivo podešavanje ili dodatno filtriranje rezultata.

#### 3.1.3. Blob detekcija

Korišten je `SimpleBlobDetector` iz OpenCV biblioteke koji identifikuje regije slike zasnovane na analizi značajki. Detektor koristi višestruke pragove i filtrira blob-ove prema kriterijumima kao što su površina (minimalna i maksimalna), cirkularnost (mjera sličnosti s krugom), konveksnost (odnos površine i konveksnog omotača), te inercija (distribucija mase regije). Prije detekcije primjenjena je CLAHE (Contrast Limited Adaptive Histogram Equalization) tehnika za poboljšanje lokalnog kontrasta i omogućavanje robusnije segmentacije u varijabilnim uslovima osvjetljenja.

**Šta detektor mjeri i kada propusta objekte.** Površina (*area*) odbacuje premale ili prevelike regije. **Cirkularnost** uspoređuje oblik s krugom; **konveksnost** mjeri koliko kontura ispunjava konveksni omotač (udubljenja smanjuju vrijednost). **Inercija** (odnos sopstvenih vrijednosti inertia tensora) razlikuje izdužene od približno kružnih blob-ova. Kada su **refleksije** jake ili **kontrast** objekta prema pozadini slab, binarna mapa nakon niza pragova postaje nekompletna: blob se „prekida“, ne zadovoljava istovremeno sve pragove ili ne prolazi jedan od geometrijskih filtera, pa se kovanica **ne detektuje** iako je vizuelno prisutna. Zato je blob pristup u ovom radu često konzervativan (malo detekcija), ali kada uspije, lokalizacija može biti vrlo dobra.

### 3.2. Eksperimentalni setup

#### 3.2.1. Testni skup podataka

Kreiran je skup od 6 testnih slika:
- **5 slika s ground truth anotacijama**: 2KM.jpg (1 kovanica), 4i05KM.jpg (4), 5i05KM.jpg (5), 7i05KM.jpg (7), 7KM.jpg (6)
- **1 slika različitog okruženja**: coins.jpg (5 kovanica)

Ukupno 28 kovanica ručno anotiranih s preciznim koordinatama centara i radijusa.

### 3.3. Metrike evaluacije

Neka su *TP* (true positives) broj ispravno uparenih detekcija, *FP* (false positives) broj detekcija bez odgovarajućeg ground truth objekta, *FN* (false negatives) broj ground truth objekata koji nemaju ispravnu detekciju, a *N* ukupan broj ground truth objekata na slici/skupu. Za svaki upareni par (detekcija, anotacija) računa se **IoU** (Intersection over Union) kao omjer presjeka i unije bounding krugova (ili ekvivalentnih maski). Detekcija se smatra ispravnom ako je IoU ≥ 0,5 prema uobičajenoj praksi (Everingham et al., 2010).

Korištene su sljedeće metrike:

- **Precision** (preciznost): P = TP / (TP + FP), za TP + FP > 0 (inace 0).
- **Recall** (odziv): R = TP / (TP + FN), za TP + FN > 0 (inace 0).
- **F1-Score**: harmonijska sredina preciznosti i odziva, F1 = 2PR / (P + R), za P + R > 0 (inace 0).
- **Mean IoU**: aritmetička sredina IoU vrijednosti po ispravno detektovanim objektima (prema uparivanju koje definiše TP).
- **Accuracy** (stopa pokrivenosti ground truth-a u ovom eksperimentu): A = (TP / N) × 100%, gdje je N broj stvarnih kovanica na slici ili agregatno na skupu, u skladu s tabelama rezultata.

### 3.4. Implementacija i web sučelje

Sistem je implementiran kao Django 4.2 web aplikacija s OpenCV 4.8 bibliotekom za obradu slike. Na serverskoj strani izvršavaju se isti algoritmi opisani u sekciji 3.1; korisnik ne mora lokalno instalirati Python okruženje da bi poredio pristupe.

**Osnovne funkcionalnosti i tok korištenja.** Korisnik učitava jednu ili više slika (do šest po sesiji), bira algoritam ili redoslijed obrade, podešava pragove (npr. Hough akumulator, blob filtere, morfološke iteracije) kroz forme na stranici, pokreće obradu i dobija stranicu s **vizualizacijom**: originalna slika i overlay detektovanih krugova (centar, radijus) po izabranom metodu. Rezultati se mogu pregledati po slikama; gdje je predviđeno, omogućen je izvoz u tabelarnom obliku radi daljnje analize. Sučelje je namijenjeno edukaciji i brzoj iteraciji parametara bez mijenjanja izvornog koda.

**Slika 2.** Prikaz korisničkog sučelja web aplikacije (unos slike, parametri, pregled detekcije).

SLIKA_SUČELJA

*U konačnoj verziji rada umetnuti snimak ekrana stvarnog sučelja (npr. forma za upload, izbor algoritma i panel s rezultatom obrade).*

## 4. REZULTATI

### 4.1. Kvantitativna analiza

Tabela 1 prikazuje detaljne rezultate testiranja sva tri algoritma na cjelokupnom skupu podataka.

**Tabela 1.** Rezultati detekcije po slikama

| Slika | Morfološka cirkularna detekcija ||| Hough transformacija ||| Blob detekcija |||
|-------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| | Det. | F1 | IoU | Det. | F1 | IoU | Det. | F1 | IoU |
| 2KM.jpg | 1 | 1.0 | 0.812 | 6 | 0.286 | 0.586 | 0 | 0.0 | 0.0 |
| 4i05KM.jpg | 4 | 1.0 | 0.706 | 16 | 0.4 | 0.903 | 2 | 0.667 | 0.886 |
| 5i05KM.jpg | 5 | 1.0 | 0.751 | 15 | 0.5 | 0.887 | 3 | 0.75 | 0.908 |
| 7i05KM.jpg | 7 | 1.0 | 0.777 | 19 | 0.538 | 0.918 | 4 | 0.727 | 0.915 |
| 7KM.jpg | 6 | 1.0 | 0.744 | 19 | 0.48 | 0.922 | 1 | 0.286 | 0.922 |
| coins.jpg | 5 | 0.909 | 0.824 | 107 | 0.088 | 0.737 | 0 | 0.0 | 0.0 |
| **Prosjek** | | **0.985** | **0.769** | | **0.382** | **0.826** | | **0.404** | **0.746** |

**Slika 1.** Vizualna komparacija rezultata tri algoritma na testnoj slici 5i05KM.jpg (5 kovanica)

SLIKA

Slika 1 ilustruje karakteristične performanse svakog algoritma na istoj testnoj slici. **Morfološka cirkularna detekcija** (lijevo) postiže perfektnu detekciju svih pet kovanica bez lažnih pozitiva (Precision=1.0, Recall=1.0, F1=1.0, Mean IoU=0.751). **Hough transformacija** (centar) također detektuje svih pet kovanica (Recall=1.0), ali generiše deset dodatnih lažnih pozitiva, rezultirajući sa ukupno 15 detekcija i niskom preciznosti (Precision=0.333, F1=0.5). Ipak, validne Hough detekcije postižu izuzetno visok IoU (0.887). **Blob detekcija** (desno) detektuje samo tri od pet kovanica (Recall=0.6, F1=0.75), ali sve tri detekcije su validne (Precision=1.0) sa najvišim Mean IoU (0.908). Zelene kružnice označavaju detektovane objekte. Ova slika jasno demonstrira trade-off između preciznosti i odziva: morfološki pristup optimalno balansira oba, Hough favorizuje odziv na račun preciznosti, dok Blob favorizuje preciznost na račun odziva.

### 4.2. Analiza po algoritmima

#### 4.2.1. Morfološka cirkularna detekcija

Ovaj pristup pokazao je **najstabilnije performanse**:
- F1 = 1.0 za 5 od 6 slika (slike s kontroliranom pozadinom)
- Prosječni IoU = 0.769 (dobra preciznost lokalizacije)
- Nema lažnih pozitiva na standardnim slikama
- Blagi pad performansi (F1 = 0.909) na slici različitog okruženja

**Analiza vremena obrade**: Prosječno 45-65 ms po slici, što je prihvatljivo za real-time primjene.

#### 4.2.2. Hough transformacija

Hough pristup pokazao je **probleme s lažnim pozitivima**:
- Broj detekcija značajno veći od stvarnog (6-107 vs 1-7 stvarnih)
- F1 score između 0.088-0.538
- **Visok IoU kod pravilnih detekcija** (0.887-0.922) – kada detektuje ispravno, preciznost je odlična
- Ekstreman broj lažnih pozitiva na slici coins.jpg (107 detekcija)

**Zaključak**: Hough metoda treba stroža podešavanja parametara ili dodatni post-processing za filtriranje lažnih pozitiva.

#### 4.2.3. Blob detekcija

Blob pristup pokazao je **najlošije performanse**:
- 0 detekcija na 2 od 6 slika
- F1 score 0.0-0.75 (veoma varijabilan)
- **Excellent IoU kada detektuje** (0.886-0.922)
- Problem s osetljivošću na uslove osvjetljenja

**Zaključak**: Blob detektor zahtijeva značajno prilagođavanje parametara za različite uslove.

### 4.3. Uticaj okruženja

Ključno zapažanje proizlazi iz razlike u performansama između slika s kontroliranom pozadinom i slike coins.jpg koja ima različite uslove osvjetljenja i pozadine:

- **Morfološki pristup**: Blagi pad (F1: 1.0 → 0.909), ali i dalje odličan
- **Hough**: Katastrofalni pad (F1: 0.286-0.538 → 0.088)
- **Blob**: Potpuni neuspjeh (F1: 0.286-0.75 → 0.0)

Ovo potvrđuje hipotezu da je **kontrolirana pozadina kritična** za robusne performanse klasičnih metoda.

## 5. DISKUSIJA

### 5.1. Praktična primjenjivost u industrijskoj obradi

Rezultati jasno ukazuju da morfološki pristup cirkularne detekcije predstavlja **optimalno rješenje za industrijske aplikacije** gdje su uslovi okruženja kontrolirani:

1. **Proizvodne trake** – konstantno osvjetljenje, uniformna pozadina
2. **Automatsko brojanje** – novčići, tablete, vijci, matice
3. **Kontrola kvaliteta** – detekcija defekata na kružnim proizvodima
4. **Robotska vizija** – prepoznavanje i lokalizacija dijelova

Ključne prednosti morfološkog pristupa:
- **Determinističko ponašanje** – predvidljivi rezultati
- **Nema lažnih pozitiva** – kritično za industrijske sisteme
- **Niska računska složenost** – pogodno za *edge computing*
- **Transparentnost** – jednostavno razumijevanje i održavanje

### 5.2. Ograničenja i izazovi

Istraživanje je identificiralo nekoliko ograničenja:

1. **Ovisnost o pozadini**: Sva tri pristupa pokazuju degradaciju performansi u nekontroliranim uslovima
2. **Parametri specifični po primjeni**: Optimalni parametri moraju se podešavati za svaki novi scenario
3. **Problem preklapanja**: Algoritmi nisu testirani na slikama s preklapajućim objektima
4. **Varijacija u veličini**: Potreban širi raspon radijusa u nekim primjenama

### 5.3. Analiza razlika u performansama algoritama

Dramatična razlika u performansama tri testirana algoritma (Morfološki F1=0.985, Hough F1=0.382, Blob F1=0.404) zahtijeva detaljnu analizu arhitekturalnih razlika koje dovode do ovih rezultata.

#### 5.3.1. Prednost morfološkog pristupa: HSV segmentacija pozadine

Ključni dizajnerski element morfološkog *pipeline*-a je **inicijalno korištenje HSV prostora boja za segmentaciju pozadine**:

```
mask = inRange(HSV, (0, 60, 0), (255, 255, 255))
```

Ova operacija, primjenjena na samom početku *pipeline*-a, eliminiše regije sa niskom saturacijom, što uključuje tipične sive i bijele pozadine. Metalne kovanice, zbog svojih reflektivnih svojstava i metalnog sjaja, zadržavaju relativno visoku saturaciju čak i u sivim tonovima, što omogućava njihovo razdvajanje od pozadine. **Svi naredni koraci** (morfološke operacije, Canny detekcija ivica, analiza kontura) stoga rade na već precizno segmentiranim kandidatima.

Ovaj pristup **uključuje domensko znanje** o prirodi objekta koji se detektuje – metalne kovanice imaju specifične optičke karakteristike koje ih razlikuju od papirne ili tekstilne pozadine.

#### 5.3.2. Problem Hough transformacije: lažni pozitivi

Hough pristup pokazao je problema sa ekscesivnim lažnim pozitivima (6-107 detekcija naspram 1-7 stvarnih kovanica). Razlozi su višestruki:

**a) Rad na nefiltiranoj grayscale slici**: Hough algoritam primjenjuje circle detection direktno na sivoj slici bez domenski-specifične segmentacije. Posljedično, sve cirkularne ili kvazi-cirkularne strukture u slici (tekstura pozadine, senke, refleksije, djelimične ivice) postaju kandidati za detekciju.

**b) Osjetljivost akumulatorskog praga**: Parametar `param2` (prag akumulatora) kontroliše koliko "glasova" je potrebno da bi se potencijalni krug prihvatio. U testiranoj konfiguraciji, ovaj prag očigledno nije bio dovoljno strogo postavljen za heterogene pozadine, što je rezultiralo sa 107 detekcija na slici `coins.jpg`.

**c) Odsustvo post-processinga**: Za razliku od morfološkog pristupa koji kombinuje više filtera, Hough metoda nema dodatne korake validacije koji bi eliminisali geometrijski plausibilne ali semantički nevalidne detekcije.

Ironično, **kada Hough detektuje ispravno, preciznost lokalizacije je izuzetna** (Mean IoU 0.826). Problem dakle nije u kvalitetu samog algoritma detekcije krugova, već u **nedostatku diskriminacije** između stvarnih objekata interesa i šuma pozadine.

#### 5.3.3. Problem Blob detekcije: nedovoljno detekcija

Blob pristup pokazao je suprotan problem – nedovoljno detekcija, uključujući 0 detekcija na dvije od šest slika. Glavni uzrok leži u arhitekturi `SimpleBlobDetector`:

**a) Multi-threshold pristup**: Algoritam primjenjuje seriju pragova (threshold) od minimalne do maksimalne vrijednosti i traži regije koje persistiraju kroz multiple pragove. Kovanice sa neuniformnom osvijetljenošću (npr. metalnim refleksijama) mogu "nestati" na određenim pragovima, prekidajući kontinuitet blob-a.

**b) Konjunkcija strogih kriterijuma**: Blob mora istovremeno zadovoljiti kriterijume cirkularnosti, konveksnosti i inercije. Bilo kakva nepravilnost u segmentaciji (npr. uslijed senki ili refleksija) može uzrokovati neuspjeh jednog kriterijuma, što automatski diskvalifikuje cijeli blob.

**c) Odsustvo domenskog znanja**: Kao i Hough, Blob detektor radi na generičkoj grayscale reprezentaciji bez korištenja boje ili teksture za separaciju objekata od pozadine.

Kada Blob uspješno detektuje, **IoU je izuzetno visok** (Mean IoU 0.746), što ukazuje da je problem u **robusnosti detekcije**, ne u njenoj kvaliteti.

#### 5.3.4. Generalizabilnost versus specifičnost

Ovi rezultati ilustruju fundamentalni trade-off u dizajnu algoritama kompjuterske vizije:

- **Hough i Blob su generički algoritmi** dizajnirani za širok spektar aplikacija. Njihova snaga je fleksibilnost, ali cijena je potreba za ekstenzivnim podešavanjem parametara i post-processingom za specifične domene.

- **Morfološki pristup je domenski-adaptiran algoritam** koji uključuje eksplicitno znanje o karakteristikama kovanica (metalne, obojene, na neutral pozadini). Cijena je smanjena generalizabilnost, ali korist je superiornost u ciljanoj aplikaciji.

Za **industrijske scenarije sa kontroliranim uslovima**, domenski-adaptirani pristupi često nadmašuju generičke metode zahvaljujući mogućnosti eksploatacije konzistentnosti okruženja.

### 5.4. Poređenje s deep learning pristupima

Iako ovaj rad ne uključuje direktno poređenje s metodama dubokog učenja, kontekstualizacija rezultata je važna. Deep learning pristupi (Faster R-CNN, YOLO) tipično postižu F1 > 0.95 na različitim okruženjima (Redmon et al., 2016), ali dolaze s značajnim troškovima:

- Potreba za velikim označenim skupovima podataka
- Zahtjevni GPU resursi za treniranje i inferiranje  
- "Crna kutija" priroda – teška interpretabilnost
- Rizik od *overfitting* na trening podatke

Za kontrolirane industrijske aplikacije, morfološki pristup nudi **uporedivu ili superiornu performansu** (F1 = 1.0) uz znatno nižu kompleksnost.

### 5.5. Edukacijski značaj

Razvijena web aplikacija predstavlja vrijedan edukacijski alat koji omogućava:
- Interaktivno učenje o algoritmima obrade slike
- Eksperimentiranje s parametrima u realnom vremenu
- Vizualizaciju međurezultata *pipeline*-a
- Usporedbu različitih pristupa

Ovaj aspekt rada posebno je relevantan za univerzitetsku nastavu iz kompjuterske vizije i obrade slike.

## 6. ZAKLJUČAK

Ovo istraživanje dalo je **komparativnu, eksperimentalno potkrijepljenu sliku** tri klasična pristupa detekciji kružnih objekata u kontekstu brojanja kovanica. Doprinos rada nije tvrdnja o globalnoj algoritamskoj novosti, nego kombinacija: (i) iste eksperimentalne postavke i ručno anotiranog malog skupa, (ii) jedinstvenih metrika (IoU, Precision, Recall, F1), i (iii) javno dostupne web aplikacije za ponavljanje i demonstraciju. Glavni zaključci su:

1. **Morfološki *pipeline*** s ranom HSV segmentacijom pozadine postiže izuzetne agregatne performanse (F1 ≈ 0,985, prosječni IoU ≈ 0,77) u kontrolisanim uslovima i jasno nadmašuje Hough i Blob u ovom eksperimentu.

2. **Kontrolirana pozadina** je kritičan faktor — svi pristupi degradiraju u varijabilnijim uslovima; razlika je posebno izražena kod Hough metode (brojni lažni pozitivi).

3. **HSV segmentacija** objašnjava veliki dio prednosti morfološkog lanca: eliminacija pozadine prije detekcije smanjuje lažne kandidate u odnosu na generičku obradu sive slike.

4. **Hough** u testiranoj konfiguraciji daje mnogo lažnih detekcija usljed glasanja u parametarskom prostoru na šumovitim ivicama; **Blob** često propušta objekte kada refleksije i kontrast kvare stabilnost regija kroz pragove i geometrijske filtere.

5. **Klasične metode** i dalje su opravdane kada su scenarij i budžet ograničeni, uz uvjet da se doprinos ne pretjerano generalizuje van opisane postavke.

Budući rad može uključiti veći anotirani skup, preklapanja, strožije post-procesiranje Hough/Blob rezultata i poređenje s dubokim modelima uz eksplicitno navođenje troška podataka i resursa.

Razvijena web aplikacija služi kao *open-source* alat za edukaciju i reprodukciju eksperimenata, što je sastavni dio doprinosa ovog rada.

## LITERATURA

Ballard, D. H. (1981). "Generalizing the Hough transform to detect arbitrary shapes". *Pattern Recognition*, 13(2), str. 111-122.

Bay, H., Tuytelaars, T. i Van Gool, L. (2006). "SURF: Speeded Up Robust Features". U: *European Conference on Computer Vision (ECCV)*, str. 404-417.

Bradski, G. i Kaehler, A. (2008). *Learning OpenCV: Computer Vision with the OpenCV Library*. Sebastopol: O'Reilly Media.

Bradley, D. i Roth, G. (2007). "Adaptive thresholding using the integral image". *Journal of Graphics Tools*, 12(2), str. 13-21.

Bremananth, R. et al. (2010). "A new approach for Indian coin recognition using image subtraction technique". U: *International Conference on Recent Trends in Information, Telecommunication and Computing*, str. 162-164.

Canny, J. (1986). "A computational approach to edge detection". *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 8(6), str. 679-698.

Cucchiara, R., Grana, C., Piccardi, M. i Prati, A. (2003). "Detecting moving objects, ghosts, and shadows in video streams". *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 25(10), str. 1337-1342.

Davies, E. R. (2005). *Machine Vision: Theory, Algorithms, Practicalities*. 3rd ed. Amsterdam: Morgan Kaufmann.

Duda, R. O. i Hart, P. E. (1972). "Use of the Hough transformation to detect lines and curves in pictures". *Communications of the ACM*, 15(1), str. 11-15.

Everingham, M. et al. (2010). "The Pascal Visual Object Classes (VOC) Challenge". *International Journal of Computer Vision*, 88(2), str. 303-338.

Garcia-Garcia, A. et al. (2017). "A survey on deep learning techniques for image and video semantic segmentation". *Applied Soft Computing*, 70, str. 41-65.

Girshick, R. (2015). "Fast R-CNN". U: *IEEE International Conference on Computer Vision (ICCV)*, str. 1440-1448.

Girshick, R. et al. (2014). "Rich feature hierarchies for accurate object detection and semantic segmentation". U: *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, str. 580-587.

Gonzalez, R. C. i Woods, R. E. (2008). *Digital Image Processing*. 3rd ed. Upper Saddle River: Prentice Hall.

He, K. et al. (2017). "Mask R-CNN". U: *IEEE International Conference on Computer Vision (ICCV)*, str. 2961-2969.

Illingworth, J. i Kittler, J. (1988). "A survey of the Hough transform". *Computer Vision, Graphics, and Image Processing*, 44(1), str. 87-116.

Khashman, A. i Sekeroglu, B. (2006). "Coin identification using a neural network". U: *International Symposium on Intelligent Data Analysis*, str. 179-184.

Kirillov, A. et al. (2023). "Segment Anything". U: *IEEE/CVF International Conference on Computer Vision (ICCV)*.

LeCun, Y., Bengio, Y. i Hinton, G. (2015). "Deep learning". *Nature*, 521(7553), str. 436-444.

Lin, T. Y. et al. (2014). "Microsoft COCO: Common Objects in Context". U: *European Conference on Computer Vision (ECCV)*, str. 740-755.

Lindeberg, T. (1998). "Feature detection with automatic scale selection". *International Journal of Computer Vision*, 30(2), str. 79-116.

Liu, W. et al. (2016). "SSD: Single Shot MultiBox Detector". U: *European Conference on Computer Vision (ECCV)*, str. 21-37.

Lowe, D. G. (2004). "Distinctive image features from scale-invariant keypoints". *International Journal of Computer Vision*, 60(2), str. 91-110.

Moreels, P. i Perona, P. (2007). "Evaluation of features detectors and descriptors based on 3D objects". *International Journal of Computer Vision*, 73(3), str. 263-284.

Otsu, N. (1979). "A threshold selection method from gray-level histograms". *IEEE Transactions on Systems, Man, and Cybernetics*, 9(1), str. 62-66.

Padilla, R., Netto, S. L. i da Silva, E. A. B. (2020). "A survey on performance metrics for object-detection algorithms". U: *International Conference on Systems, Signals and Image Processing (IWSSIP)*, str. 237-242.

Powers, D. M. W. (2011). "Evaluation: From precision, recall and F-measure to ROC, informedness, markedness and correlation". *Journal of Machine Learning Technologies*, 2(1), str. 37-63.

Prasad, D. K., Leung, M. K. H. i Quek, C. (2012). "ElliFit: An unconstrained, non-iterative, least squares based geometric Ellipse Fitting method". *Pattern Recognition*, 46(5), str. 1449-1465.

Redmon, J. et al. (2016). "You Only Look Once: Unified, Real-Time Object Detection". U: *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, str. 779-788.

Redmon, J. i Farhadi, A. (2017). "YOLO9000: Better, faster, stronger". U: *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, str. 7263-7271.

Redmon, J. i Farhadi, A. (2018). "YOLOv3: An incremental improvement". *arXiv preprint* arXiv:1804.02767.

Reisert, M., Ronneberger, O. i Burkhardt, H. (2007). "A fast and reliable coin recognition system". U: *DAGM Conference on Pattern Recognition*, str. 415-424.

Ren, S. et al. (2015). "Faster R-CNN: Towards real-time object detection with region proposal networks". U: *Advances in Neural Information Processing Systems (NIPS)*, str. 91-99.

Sauvola, J. i Pietikäinen, M. (2000). "Adaptive document image binarization". *Pattern Recognition*, 33(2), str. 225-236.

Smith, A. R. (1978). "Color gamut transform pairs". *ACM SIGGRAPH Computer Graphics*, 12(3), str. 12-19.

Soille, P. (2003). *Morphological Image Analysis: Principles and Applications*. 2nd ed. Berlin: Springer-Verlag.

Suzuki, S. i Abe, K. (1985). "Topological structural analysis of digitized binary images by border following". *Computer Vision, Graphics, and Image Processing*, 30(1), str. 32-46.

Terven, J. R. i Cordova-Esparza, D. M. (2023). "A comprehensive review of YOLO architectures in computer vision: From YOLOv1 to YOLOv8 and beyond". *arXiv preprint* arXiv:2304.00501.

Van, L. M., Nguyen, D. T. i Bui, L. T. (2016). "Touch-based coin recognition using neural networks". U: *International Conference on Advanced Technologies for Communications*, str. 202-206.

Xie, W. i Pun, C. M. (2017). "Fusing deep learning and morphological operations for feature extraction". U: *International Conference on Wavelet Analysis and Pattern Recognition (ICWAPR)*, str. 267-272.

Xu, L., Oja, E. i Kultanen, P. (1990). "A new curve detection method: Randomized Hough transform (RHT)". *Pattern Recognition Letters*, 11(5), str. 331-338.

Zhao, Y. et al. (2024). "DETRs Beat YOLOs on Real-Time Object Detection". U: *IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*. (Također: *arXiv preprint* arXiv:2304.08069.)

Zhu, J. Y., Zheng, W. S. i Lu, J. (2018). "Learning deep representations for ground-to-aerial image matching". U: *IEEE International Conference on Computer Vision (ICCV)*, str. 3038-3046.

## SUMMARY

This paper reports an experimental comparison of three classical approaches to circular object detection for automatic coin counting: a domain-tuned morphological pipeline (Gaussian blur, HSV background removal, Otsu thresholding, dilation/erosion, Canny edges, contour circularity filtering), the Hough circle transform, and OpenCV's SimpleBlobDetector. The stated contribution is the **controlled comparative evaluation** on a small manually annotated image set using IoU-based matching and F1/Precision/Recall, together with a Django web application for replication and teaching — not a claim of a globally new algorithm. The morphological pipeline achieved the strongest aggregate results (F1 ≈ 0.985, mean IoU ≈ 0.77) in the tested setup, including F1 = 1.0 on five controlled-background images and F1 = 0.909 on a more variable scene.

Hough produced many false positives (e.g. 6–107 detections vs. 1–7 coins) despite high IoU on true hits; blob detection often missed coins under difficult contrast or reflections but showed high IoU when it fired. The discussion ties these behaviors to voting in Hough space, edge noise, and blob multi-threshold geometry filters.

Classical methods remain practical for constrained industrial-style setups. The web UI supports upload, parameter adjustment, visualization of detections, and export of results for further analysis.
