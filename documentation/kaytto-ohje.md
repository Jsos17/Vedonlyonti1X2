# Käyttöohje

## Tavallinen pelaaja/asiakas

### Rekisteröinti

Paina linkkiä *Create an account* ja anna käyttäjänimi, salasana, ja aloitussaldo. Rekisterötymisen jälkeen pitää erikseen kirjautua vielä sisään.

### Kirjautuminen

Paina linkkiä *Login* ja anna käyttäjätunnuksesi ja salasanasi

### Vedon asettaminen

Mene kohtaan *List betting offers* ja valitse mitkä vetokohteet (betting_offer) haluat mukaan kupongille ja paina sitten *Create a bet coupon* nappia

Tämän jälkeen avautuvassa näkymässä valitse jokaiseen otteluun haluamasi vaihtoehto 1 (kotivoitto), x (tasapeli) tai 2 (vierasvoitto). Lopuksi valitse panos euroina ja centteinä ja paina *Place bet* nappia.

Jos lomakkeessa oli jotain virheellistä pitää valinnat tehdä uudelleen sillä ne tyhjenevät.

Onnistuneen vedon jälkeen sinut ohjataan sivulle, missä näet pelihistoriasi, kuponkisi listattuna ja voit tarkastella niitä tarkemmin linkkien kautta.

### Tili

Paina *Show acccount* linkkiä, jonka jälkeen voit siirtää rahaa tilillesi *Deposit money* tai sieltä pois *Withdraw money*, vaihtaa salasanan *Change password* tai aloittaa tilin poiston *Start account deletion process*.

Nappi *Start account deletion process* ohjaa sinut sivulle missä voit varmistaa halusi poistaa tilisi, jos sinulla ei ole vielä avoimena olevia vetoja. Painamalla *Yes, delete my account* poistat tilisi pysyvästi ja *No, don't delete my account* nappi ei poista tiliäsi. Voit myös poistua tästä näkymästä painamalla jotain sivun linkkiä.

## Tili, Role-taulu ja User_role taulu

Tietokantaan luodaan Role-tauluun automaattisesti entryt name = "CUSTOMER" ja name = "ADMIN". Kaikkiin uusiin käyttäjiin liitetään automaattisesti liitostaulu *User_role* entry missä *role_id* vastaa CUSTOMER entryn id:tä.


Jos oletetaan, että adminin entry Role-taulussa on: id=2, name='ADMIN' ja käyttäjän id = 8, niin käyttäjän roolin asetus adminiksi tapahtuu seuraavasti tietokannanhallintajärjestelmän kautta:

    ```SQL
    INSERT INTO user_role (bettor_id, role_id) VALUES (8, 2);
    ```

Jos käyttäjä asetetaan adminiksi on häneltä hyvä poistaa sen jälkeen rooli CUSTOMER, oletuksena id=1, name='CUSTOMER' ja käyttäjä id edelleen id = 8:

    ```SQL
    DELETE FROM user_role WHERE bettor_id = 8 AND role_id = 1;
    ```
Saman toiminnallisuuden voisi myös tehdä vain päivittämällä olemassa olevaa *User_role* taulun entryä role_id:n osalta.

Jos käyttäjään liittyy vain yksi rooli:

    ```SQL
    SELECT user_role.id FROM user_role WHERE user_role_bettor_id = <haluttu id>;
   	```


    ```SQL
	UPDATE user_role SET role_id = 2 WHERE user_role.bettor_id = <haluttu id>;
    ```

### Admin-näkymät

#### List matches

Listaa kaikki käytettävissä olevat ottelut ja niiden todennäköisyysarviot

#### Access match information

Jos ottelun tulos ei ole vielä ratkennut, niin seuraavat linkit näkyvät:

* *Add offer* to match -ohjaa vetokohteen lisäämisnäkymään, jos kohdetta ei vielä ole olemassa

* *Update match* -ohjaa päivitysnäkymään, jossa voi päivittää kaikkia ottelun tietoja, paitsi tulosta kts. alla
 
* *Set result* -ohjaa ottelutuloksen asetusnäkymään. Tämä toimenpide on "lopullinen" (komentoriviltä tuloksen muutos toki onnistuu, mutta ei sovelluksen kautta enää), sillä se käynnistää ottelutuloksesta riippuvaisten tietokohteiden päivityksen ja esimerkiksi mahdolliset voitonmaksut. Tulos pitää syöttää kahteen kertaan ja vielä varmistaa checkboxin avulla, mahdollisten voitonmaksujen vuoksi.

	Ottelun tulos voi olla:
	void = ottelu on mitätöity jostain syystä
	1 = kotivoitto
	x = tasapeli
	2 = vierasvoitto

Jos otteluun ei liity vetokohdetta, niin ottelun poistolinkki näkyy:

* *Delete match* - poistaa ottelun yhdellä klikkauksella, jos otteluun ei vielä ole liitetty vetokohdetta

#### Add a match

Tässä voi lisätä ottelun ja liittää siihen todennäköisyysarvion kokonaisluku-prosentteina. 

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

Jos käyttäjällä on pelkästään ADMIN-rooli ei hän juuri näe tilitietojaan, jos käyttäjällä on sekä CUSTOMER että ADMIN rooli näkee hän samat näkymät kuin CUSTOMER

### Search betting offers

Tarjoaa yksinkertaisen hakutoiminnon ottelun/vetokohteen hakemiseen koti- tai vierasjoukkueen nimen perusteella ja samalla mahdollisuuden lyödä heti vetoa löydetyistä kohteista, jos käyttäjä on CUSTOMER. ADMIN näkee vain pelkät hakutulokset.
