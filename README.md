# Bet1X2App/Tietokantasovellus alkukesä 2018

## Vedonvälittäjä Bet1X2

Vedonvälitystoimisto Bet1X2 tarjoaa pelkästään 1X2-tyyppisiä vetoja rekisteröityneille asiakkailleen internetsivullaan.

Asiakas voi rekisteröityä sivulla, ja sen jälkeen lyödä vetoa yhtiön tarjoamista otteluista. Ottelulla on kolme eri tulosmahdollisuutta: kotivoitto 1, tasapeli X ja vierasvoitto 2. Jokaiseen mahdollisuuteen liittyy kerroin ja tapahtuman todennäköisyys. Lisäksi otteluun liittyy kotijoukkue, vierasjoukkue, ajankohta ja myöhemmin varmistuva tulos. 

Bet1X2:n palautusprosentti on 90 % eli se ottaa laskennallisesti ja odotusarvoisesti 10 % jokaisesta ottelutapahtuman pelivaihdosta itselleen. Loput 90 % maksetaan pelaajille voittoina.

Vedonvälittäjällä työskentelee admin-oikeuksilla varustettuja henkilöitä, jotka voivat lisätä otteluita otteluvalikoimaan ja liittää niihin kotivoiton, tasapelin ja vierasvoiton todennäköisyyden. Otteluihin voidaan sitten liittää vetokohde, joka sisältää muun muassa kertoimet. Admin voi poistaa vetokohteen, jos siitä ei vielä ole lyöty vetoa. Muutoin admin voi vain muuttaa vetokohteen ei-aktiiviseksi tai sulkea sen lopullisesti. Kun kohde on suljettu ei siitä voi lyödä vetoa ja sen aktiiviseksi muuttaminen ei tee mitään. Hiukan ennen ottelun alkua kohde sulkeutuu automaattisesti.

Asiakas voi muuttaa käyttäjätunnustaan, salasanaansa ja lisätä saldoaan. Lisäksi asiakas voi poistaa tilinsä, jos hänellä ei ole avoimia vetoja, muulloin asiakas joutuu odottamaan, että avoimet vedot ratkeavat ja tämän jälkeen asiakas voi poistaa tilinsä. 

Asiakas ei voi perua vetoa sen jälkeen kun se on lyöty. Vedon lyötyään asiakas näkee mahdollisen voiton määrän. Asiakas voi lyödä useita vetoja samasta kohteesta maksimipanostuksen sallimissa rajoissa.

Asiakas voi yhdistellä useita kohteita samaan vetoon. Asiakas voittaa jos kaikki vedon kohteet ovat oikein ja häviää muulloin. Vetoon liitettyjen vetokohteiden määrä on rajattu, ja tämä raja tarkentuu myöhemmin.

Asiakas voi tarkastella vetohistoriaansa ja tarjolla olevia vetokohteita. Admin voi tarkastella kaikkien kohteiden vaihtoja ja maksettuja voittoja sekä käytettävissä olevien otteluiden listoja. Lisäksi admin voi tarkastella asiakkaiden vedonlyönnin menestyksellisyyttä heidän vetohistorian kautta.

### Alustava luokkakaavio

[Bet1X2 luokkakaavio](https://github.com/Jsos17/Vedonlyonti1X2/blob/master/documentation/Bet1X2_luokkakaavio.jpg)

### Alustava tietokantakaavio

[Bet1X2 tietokantakaavio](https://github.com/Jsos17/Vedonlyonti1X2/blob/master/documentation/Bet1X2_tietokantakaavio.jpg)

### User stories

[User stories](https://github.com/Jsos17/Vedonlyonti1X2/blob/master/documentation/user_stories.md)

### Rekisteröity käyttäjä: (Kaikki taulut poistettiin ja asennettiin uudelleen hetkellä ma 18.6.2018 n. klo 21:20, joitain tietoja ei välttämättä näy juuri tällä ajanhetkellä)

username: pelaaja1

password: 12345678

### Linkki herokuun (päivitetty)

[Bet1X2App](https://bet1x2-app.herokuapp.com/)

Huomioita:

Tilin poisto on jäädytetty, jotta kukaan ei poista esimerkkitiliä, samoin päivitys on muokattu koskemaan vain saldoa. Maksimipanosta tai pelaajan varallisuutta ei tällä hetkellä tarkisteta. Jos tapahtuman todennäköisyys on 90 % tai yli niin kertoimet menevät alle 1:n johtuen vielä puutteellisesta laskentamekanismista, ja tällöin kertoimia pitää säätää manuaalisesti jotta lomake validoidaan. Ottelun voi poistaa vain jos siihen ei liity vetokohdetta tällä hetkellä.

