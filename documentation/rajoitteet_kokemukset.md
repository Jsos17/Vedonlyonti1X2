# Totetus, työn rajoitteet ja puuttuvat ominaisuudt sekä omat kokemukset

## Toteutus

Suurinpiirtein kaikki mitä suunniteltiin sovelluksen toimannallisuuksiksi on toteutettu poislukien ajoitettu kohteen sulkeutuminen ja adminin mahdollisuus tarkastella menestyksellisiä pelaajia heidän pelihistorian kautta.. Ajatuksena oli populoida tietokanta myös jollain generoidulla ottelulistalla, mutta tämä jäi ajanpuutteen vuoksi toteuttamatta. Jos näin olisi ollut, olisi adminin työ ollut huomattavasti helpompaa kun muutamalla klikkauksella olisi voinut luoda vetokohteen.

## Työn rajoitteet ja puuttuvat ominaisuudet

Merkittäviä puutteita ovat indeksoinnin puuttuminen ja sivutuksen puuttuminen.

Indeksoinnin puute heikentää sovelluksen tehokkuutta, koska esimerkiksi haut nimen perusteella eivät välttämättä ole nopeita.

Sivutuksen puute vaikuttaa lähinnä käyttökokemuksen miellyttävyyteen.

Näin kompleksisessa työssä testit olisivat hyvin hyödyllisä mutta sellaista ei vaadittu eikä ohjeistettu, ja niiden toteuttaminen olisi tuonut huomattavasti lisää työaikaa. Kuitenkin tästä seuraa se, että helposti työhön voi jäädä bugeja, joita ei huomaa ennen kuin on liian myöhäistä.

Koodi voisi hyötyä paikon refaktoroinnista ja esimerkiksi Hiddenfieldien validointi on paikoin heitetty hatusta, koska on vaikea tietää miten ne pitäisi validoida, kun oletuksena siellä on itse parametrina annettu tieto mutta toisaalta niitä voi päästä joku peukaloimaan. Tähän asiaan läheisesti liittyy esimerkiksi se miten käyttäjän saldo pitäisi tarkistaa, kun teoriassa hidden fieldeihin pääsee käsiksi ja näin ollen mikään niiden kautta välitetty tieto ei välttämättä ole luotettavaa.

Käytettävyydessä ja ulkoasussa olisi varmasti parannettavaa.

Automaattiseen kertoimenlaskentaan liittyy se ongelma, että jos tapahtuman todennäköisyys on yli 90 niin kerroin menee alle yhden ja se pitää manuaalisesti muuttaa ja lisäksi muita kertoimia pitää säätää manuaalisesti alas huomattavasti jotta laskennallinen 90% palautus validoituu. Koen kuitenkin, että tämän kanssa painiminen menee tämän kurssin aihepiirin ulkopuolelle ja siksi olen tyytynyt sihen mitä on toteutettu. Se vaan vaatii admin-käyttäjältä hiukan manuaalista työtä.

Ottelun luomisessa ajankohdan syöttö on hiukan kömpelö ja mahdollisesti turhauttava.

*Betting_offerin* attribuutit active ja closed sisältävät jonkinverran redundanssia, koska kohteen ajastettu sulkeminen ei totetutunut ja näin mahdollisesti pelkkä yksi boolean value olisi riittänyt.

Pelaajan historiaan olisi voinut liittää myös rahansiirtohistorian ja kuponkeihin ajan milloin on pelattu, ja näin pelaaja olisi voinut tarkastella historiaansa myös ajallisesti.

## Omat kokemukset

Minulla ei ollut mitään kokemusta Pythonista saati sitten websovellus-ohjelmoinnista. Työmäärä on ollut huomattavasti suurempi kuin esimerkiksi kevään 2018 Ohjelmistotekniikan menetelmät kurssilla (eli OTM-harjoitustyössä) siitäkin huolimatta, että tämän kurssin opintopistemäärä on 4 kun OTM:llä se oli 5. Python on kuitenkin ollut suhteellisen helppo oppia. 

Valtaisat ongelmat ovatkin olleet tietokanta/websovellus-ohjelmoinnissa. Osa kirjastojen virallisista dokumentaatioista on hyvin epämääräisiä ja puutteellisia sekä monesti esimerkit ovat liian yksinkertaisia. Monesti myös oikean tiedon löytämisessä on ollut suuria vaikeuksia.

Esimerkiksi sulkujen poisto ylikirjoitetusta *login_required:n* "is_authenticated" funktiosta korjasi (toivottavasti) ajoittaisesti esiintyvän "TypeError: 'bool' object is not callable" ongelman, mutta tämäkin on taas täyttä nopanheittoa siitä oliko tämä nyt oikea ratkaisu vai ei ja toimiiko se nyt varmasti myös herokussa. 

Tiedon välitys turvallisesti, ja erityisesti mitkä ovat "Industry best practices" on monessa tilanteessa ollut arvailujen varassa ja mielestäni tietoturvan suhteen on ikävää joutua nojautumaan googlettamiseen.
