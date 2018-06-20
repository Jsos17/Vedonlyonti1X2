# Käyttöohje

## Tavallinen pelaaja/asiakas

### Rekisteröinti

Paina linkkiä *Create an account* ja anna käyttäjänimi, salasana, ja aloitussaldo. Rekisterötymisen jälkeen pitää erikseen kirjautua vielä sisään.

### Kirjautuminen

Paina linkkiä *Login* ja anna käyttäjätunnuksesi ja salasanasi

### Vedon asettaminen

Mene kohtaan *List betting offers* ja valitse mitkä vetokohteet (betting_offer) haluat mukaan kupongille ja paina sitten *Create a bet coupon* nappia

Tämän jälkeen avautuvassa näkymässä valitse jokaiseen otteluun haluamasi vaihtoehto 1 (kotivoitto), x (tasapeli) tai 2 (vierasvoitto). Lopuksi valitse panos euroina ja centteinä ja paina *Place bet* nappia.

Jos lomakkeessa oli jotain virheellistä ole tarkkana, että valitsemasi vetovaihtoehdot ovat edelleen oikein. (Toimitus huomauttaa: tarkoitus on korjata/tehdä parempi tästä kohdasta)

Onnistuneen vedon jälkeen sinut ohjataan sivulle, missä näet kuponkisi listattuna ja voit tarkastella niitä tarkemmin linkkien kautta.

### Tili

Paina *Show acccount* linkkiä, jonka jälkeen voit päivittää tiliä *Update details* painikkeen kautta (Toimitus huomauttaa: Tällä hetkellä pelkästään rahamäärän muuttaminen mahdollista = ongelmallista)

Nappi *Start account deletion process* ohjaa sinut sivulle missä voit varmistaa halusi poistaa tilisi, jos sinulla ei ole vielä avoimena olevia vetoja. Painamalla *Yes, delete my account* poistat tilisi pysyvästi ja *No, don't delete my account* nappi ei poista tiliäsi. Voit myös poistua tästä näkymästä painamalla jotain sivun linkkiä.

## Admin

Normaalin pelaajatilin voi muuttaa Admin-tiliksi asettamalla komentoriviltä 

    UPDATE bettor SET role='ADMIN' WHERE username = <haluttu username> tai

    UPDATE bettor SET role='ADMIN' WHERE id = <haluttu id>

Admin tilin voi muuttaa takaisin Normaaliksi pelaaja-tiliksi asettamalla komentoriviltä

    UPDATE bettor SET role='CUSTOMER' WHERE username = <haluttu username> tai

    UPDATE bettor SET role='CUSTOMER' WHERE id = <haluttu id>

### Admin-näkymät

#### List matches

Listaa kaikki käytettävissä olevat ottelut ja niiden todennäköisyysarviot

#### Access match information

* *Add offer* to match -ohjaa vetokohteen lisäämisnäkymään, jos kohdetta ei vielä ole olemassa

* *Update match* -ohjaa päivitysnäkymään, jossa voi päivittää kaikkia ottelun tietoja, paitsi tulosta kts. alla
 
* *Set result* -ohjaa ottelutuloksen asetusnäkymään. Tämä toimenpide on "lopullinen" (komentoriviltä tuloksen muutos toki onnistuu, mutta ei sovelluksen kautta enää), sillä se käynnistää ottelutuloksesta riippuvaisten tietokohteiden päivityksen ja esimerkiksi mahdolliset voitonmaksut. Tämän vuoksi tuloksen varmistustoimenpide on tarkoitus lisätä.

* *Delete match* - poistaa ottelun yhdellä klikkauksella, jos otteluun ei vielä ole liitetty vetokohdetta

#### Add a match

Tässä voi lisätä ottelun ja liittää siihen todennäköisyysarvion kokonaisluku-prosentteina. 

Ottelun tulos voi olla:

tbd = to be decided eli ottelun tulos varmistuu myöhemmin

void = ottelu on mitätöity jostain syystä

1 = kotivoitto

x = tasapeli

2 = vierasvoitto

#### Turnover statistics ~ Pelivaihtojen tilastot

Näyttää kuinka paljon rahaa kohteista on lyöty vetoa ja kuinka monella kupongilla kohde on

Linkki *Show distribution of turnover* näyttä vielä kootusti kohteen tiedot siten, että rahan jakautuminen eri vaihtoehtojen kesken näytetään ja samalla alkuperäiset todennäköisyysarviot näytetään, jotta voitaisiin tehdä päätös siitä, pitääkö esim jonkun vaihtoehdon kertoimia laskea ja toista nostaa

#### Manage betting offers

Tässä näkymässä näkyy kootusti kaikki pelikohteet ja muun muassa tieto siitä onko kohde aktiivinen tai suljettu.

Jos kohteesta ei ole lyöty vetoa niin tämän näkymän kautta kohteen voi poistaa (*Delete offer*), ja lisäksi painamalla *Update offer* linkiä pääsee muokkaamaan pelikohdetta. 

Jotta kohteen voi poistaa on se ensin asetettava ei-aktiiviseksi, jotta se ei näy enää pelaajille *List betting offers* listauksessa.

HUOMAUTUS (Samanaikaisuuden hallinnan ongelma): Tilannetta jossa admin on poistamassa pelikohdetta samalla kun pelaaja on jo valinnut kohteen kupongilleen, ja sitten admin poistaa kohteen ennenkuin pelaaja asettaa vedon ei ole testattu/tämä luultavasti aiheuttaa ongelmia. Eli siis pelaaja on valinnut kohteen kupongille ja siirtynyt pelivaihtoehtojen ja panoksen valintanäkymään ennen kuin admin ehti muuttamaan kohteen ei-aktiiviseksi, mutta samanaikaisesti admin voi poistaa kohteen koska vielä kohteesta ei ole lyöty vetoa.

#### List betting offers

Sama näkymä kuin pelajalla, paitsi että kupongin luomismahdollisuus on poistettu

#### Adminin tili

Toistaiseksi admin ei voi tarkastella tiliään koska, siihen liittyisi vain "rahat" (ongelmallista)
