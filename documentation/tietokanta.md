# Tietokantarakenne

## Tietokantakaavio

![Bet1X2 tietokantakaavio](https://github.com/Jsos17/Vedonlyonti1X2/blob/master/documentation/Bet1X2_tietokantakaavio.jpg)

[Linkki luokkakaavioon](https://github.com/Jsos17/Vedonlyonti1X2/blob/master/documentation/Bet1X2_luokkakaavio.jpg)

## Tietokanta

* Sport_match kuvaa ottelua
* Betting_offer kuvaa vedonlyöntikohdetta
* Bet_coupon kuvaa vedonlyöntikuponkia
* *Betting_offer_of_coupon* on liitostaulu *Bet_couponin* ja *Bettting_offerin* ja se kuvaa kupongin yksittäistä vetokohde-valintaa
* Bettor kuvaa käyttäjää (nimentä olisi voinut olla ehkä neutraalimpi user, koska myös adminia mallinnetaan tämän kautta)
* Role kuvaa rooleja, jotka voivat liittyä käyttäjään/pelaajaan. Oletuksena on olemassa roolit "CUSTOMER" ja "ADMIN" ja nämä entryt luodaan automaattisesti tietokantaan. Kuitenkin erillinen taulu mahdollistaa roolien laajentamisen tulevaisuudessa
* User_role on liitostaulu *Bettorin* ja *Role:n* välillä, eli on mahdollista että käyttäjään liittyy useampi rooli. Käytännössä kun asiakas luo tilin liitetään häneen "CUSTOMER" rooli ja muita rooleja ei sovelluksen kautta voi liittää. "ADMIN"-rooli voidaan asettaa komentorivin kautta, ja tällöin on suositeltavaa, että rooli "CUSTOMER" poistetaan, koska ADMIN ei tee mitään CUSTOMER-roolin oikeuksilla.

Tietokannassa on siis kaksi monesta-moneen suhdetta *Bettorin* ja *Role:n välillä*, sekä *Bet_couponin* ja *Bettting_offerin* välillä.

Täysi CRUD liittyy *Sport_matchiin*, *Betting_offeriin* ja *Bettoriin*, tietyin rajoituksin. Role ja User_role tauluja ei voi muokata sovelluksen kautta. 

*Sport_match* voidaan poistaa, jos siihen ei liity *Betting_offeria*, muokkauksessa tuloksen asetus on kertaalleen tehtävissä, muuten muokkausta ei ole rajoitettu, jos ottelu ei ole vielä ratkennut. 

*Betting_offer* voidaan poistaa, jos siihen ei liity *Betting_offer_of_couponeja* (ja siten myös *Bet_couponeja*) eli, jos vetokohteesta ei ole lyöty vetoa JA jos betting_offer on asetettu ei-aktiiviseksi. Kohdetta voi myös päivittää eli esimerkiksi kertoimia muuttaa. Kerroinmuutokset eivät vaikuta jo asetettuihin vetoihin, sillä jokaisen pelaajan "saama" kerroin on talletettu *Betting_offer_of_coupon* entryyn mallintaen todellisuutta.

*Bettor* vodaan poistaa (eli pelaaja voi poistaa tilinsä), jos kaikki hänen vetonsa ovat ratkenneet. Tällöin myös pelaajaan liittyvä User_role entry poistetaan, mutta sen sijaan kaikki pelaajaan littyvät vetokupongit jäävät olemaan olemassa, siten että niiden vierasavaimeksi tulee null. Päivitystoiminnallisuus liittyy salasanan vaihtoon ja tilin balanssin muuttamiseen rahansiirroilla, panoksien asettamisella ja voittojen saamisella.

## Normalisointi

Tietokannan kaikki taulut ovat **ensimmäisessä normaalimuodossa**, koska:

* Minkään taulun sarake ei sisällä listoja
* Taulujen sarakkeet eivät muodosta toistuvia ryhmiä
* Sarakkeiden arvot ovat samantyyppisiä
* Jokaisessa taulussa sarakkeiden nimet ovat uniikkeja
* Sarakkeiden järjestys ei vaikuta tietokantataulun toimintaan
* Koska pääavaimet ovat kussakin taulussa uniikkeja, niin tauluissa ei voi olla kahta täsmälleen samanlaista riviä
* Rivien järjestys ei vaikuta tietokantataulun toimintaan

Tietokannan kaikki taulut ovat myös **toisessa normaalimuodossa**, koska jokaisen taulun pääavain on määritelty yhden sarakkeen avulla, ja koska taulut ovat ensimmäisessä normaalimuodossa.

Tietokannan **kaikki taulut paitsi Bet_coupon ja Bettor ovat myös kolmannessa normaalimuodossa**, sillä niiden sarakkeet eitvät ole transitiivisesti riippuvaisia taulujen pääavaimesta. 

**Bet_coupon** taulussa *possible_win_eur* ja *possible_win_cent* ovat funktionaalisesti riippuvaisia sarakejoukosta *combined_odds*, *stake_eur* ja *stake_cent* ja näin ollen *possible_win_eur* ja *possible_win_cent* ovat myös transitiivisesti riippuvaisia taulun pääavaimesta. Tarkalleen ottaen voiton määriä ei välttämättä tarvitsisi tallentaa, mutta toisaalta tämä tilanne vähentää usein toistuvaa voiton uudelleen laskemista, tekee maksettavan voiton ja sen miten se pyöristetään yksiselitteiseksi, kun se kerran on laskettu, sekä helpottaa myös ohjelmointia.

**Bettor** taulussa username on uniikki, joten taulun kaikki muut sarakkeet ovat transitiivisesti riippuvaisia pääavaimesta. En kuitenkaan näe mitään hyötyä taulun pilkkomisesta pienempiin osiin, ja toisaalta käyttäjänimen uniikkiuden estäminen taas aiheuttaa tarpeettomia ongelmia. 

## Indeksointi

Erillisiä indeksejä ei ole asetettu, eli käytännössä vain avaimiin liittyy indeksi.

## CREATE TABLE -lauseet




