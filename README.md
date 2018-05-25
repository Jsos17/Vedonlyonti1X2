# Bet1X2App/Tietokantasovellus alkukesä 2018

## Vedonvälittäjä Bet1X2

Vedonvälitystoimisto Bet1X2 tarjoaa pelkästään 1X2-tyyppisiä vetoja rekisteröityneille asiakkailleen internetsivullaan.

Asiakas voi rekisteröityä sivulla, ja sen jälkeen lyödä vetoa yhtiön tarjoamista otteluista. Ottelulla on kolme eri tulosmahdollisuutta: kotivoitto 1, tasapeli X ja vierasvoitto 2. Jokaiseen mahdollisuuteen liittyy kerroin ja tapahtuman todennäköisyys. Lisäksi otteluun liittyy kotijoukkue, vierasjoukkue, ajankohta ja myöhemmin varmistuva tulos. 

Bet1X2:n palautusprosentti on 85 % eli se ottaa laskennallisesti ja odotusarvoisesti 15 % jokaisesta ottelutapahtuman pelivaihdosta itselleen. Loput 85 % maksetaan pelaajille voittoina.

Vedonvälittäjällä työskentelee admin-oikeuksilla varustettuja henkilöitä, jotka voivat valita otteluvalikoimasta otteluita ja liittää niihin vetokohteen. Admin voi poistaa vetokohteen, jos siitä ei vielä ole lyöty vetoa. Muutoin admin voi vain muuttaa vetokohteen ei-aktiiviseksi tai sulkea sen lopullisesti. Kun kohde on suljettu ei siitä voi lyödä vetoa ja sen aktiiviseksi muuttaminen ei tee mitään. Hiukan ennen ottelun alkua kohde sulkeutuu automaattisesti.

Tarjottuun vetoon liittyy siis kertoimet, jotka lasketaan aluksi alkuperäisten kertoimien ja palautusprosentin avulla, ja sitten tarvittaessa päivitetään, jos pelivaihdon jakautuminen vaihtoehtojen kesken alkaa poiketa liikaa "oikeista" todennäköisyyksistä aiheuttaen näin lyhyen aikavälin riskinhallinnallisia ongelmia (eli välittäjä joutuisi maksamaan liikaa yhteen otteluun liittyviä voittoja, vaikka pitkässä juoksussa se ottaakin jokaisesta vedosta keskimäärin 15 % itselleen). Lisäksi pelaajien panostusta rajoitetaan asettamalla maksimipanos, joka liittyy jokaiseen vetokohteeseen.

Asiakas voi muuttaa käyttäjätunnustaan, salasanaansa ja lisätä saldoaan. Lisäksi asiakas voi poistaa tilinsä, jos hänellä ei ole avoimia vetoja, muulloin asiakas joutuu odottamaan, että avoimet vedot ratkeavat ja tämän jälkeen asiakas voi poistaa tilinsä. 

Asiakas ei voi perua vetoa sen jälkeen kun se on lyöty. Vedon lyötyään asiakas näkee mahdollisen voiton määrän. Asiakas voi lyödä useita vetoja samasta kohteesta maksimipanostuksen sallimissa rajoissa.

Asiakas voi tarkastella vetohistoriaansa ja tarjolla olevia vetokohteita. Admin voi tarkastella kaikkien kohteiden vaihtoja ja maksettuja voittoja sekä käytettävissä olevien otteluiden listoja. Lisäksi admin voi tarkastella asiakkaiden vedonlyönnin menestyksellisyyttä heidän vetohistorian kautta.

### Alustava luokkakaavio

![Bet1X2 luokkakaavio](https://github.com/Jsos17/Vedonlyonti1X2/blob/master/dokumentaatio/Bet1X2_luokkakaavio.jpg)

### Alustava tietokantakaavio

![Bet1X2 tietokantakaavio](https://github.com/Jsos17/Vedonlyonti1X2/blob/master/dokumentaatio/Bet1X2_tietokantakaavio.jpg)
