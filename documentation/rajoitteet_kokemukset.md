# Työn rajoitteet ja omat kokemukset

## Työn rajoitteet

Merkittäviä puutteita ovat indeksoinnin puuttuminen ja sivutuksen puuttuminen.

Indeksoinnin puute heikentää sovelluksen tehokkuutta, koska esimerkiksi haut nimen perusteella eivät nopeita.

Sivutuksen puute vaikuttaa lähinnä käyttökokemuksen miellyttävyyteen.

Koodi voisi hyötyä paikon refaktoroinnista ja esimerkiksi Hiddenfieldien validointi on paikoin heitetty hatusta, koska on vaikea tietää miten ne pitäisi validoida, kun oletuksena siellä on itse parametrina annettu tieto mutta toisaalta niitä voi päästä joku peukaloimaan... 

Tähän asiaan läheisesti liittyy esimerkiksi se miten käyttäjän saldo pitäisi tarkistaa, kun teoriassa hidden fieldeihin pääsee käsiksi ja näin ollen mikään niiden kautta välitetty tieto ei välttämättä ole luotettavaa.

Käytettävyydessä ja ulkoasussa olisi varmasti parannettavaa.

## Omat kokemukset

Minulla ei ollut mitään kokemusta Pythonista saati sitten web-ohjelmoinnista. Työmäärä on ollut huomattavasti suurempi kuin esimerkiksi kevään 2018 Ohjelmistotekniikan menetelmät kurssilla (eli OTM-harjoitustyössä) siitäkin huolimatta, että tämän kurssin opintopistemäärä on 4 kun OTM:llä se oli 5 ja näin myös työmäärässä pitäisi näkyä ero. Python on kuitenkin ollut suhteellisen helppo oppia. 

Valtaisat ongelmat ovatkin olleet tietokanta/web-ohjelmoinnissa. Osa kirjastojen virallisista dokumentaatioista on hyvin epämääräisiä ja puutteellisia ja monesti esimerkit ovat liian yksinkertaisia. Monesti myös oikean tiedon löytämisessä on ollut suuria vaikeuksia. 

Esimerkiksi sulkujen poisto ylikirjoitetusta *login_required:n* "is_authenticated" funktiosta korjasi (toivottavasti) ajoittaisesti esiintyvän "TypeError: 'bool' object is not callable" ongelman, mutta tämäkin on taas täyttä nopanheittoa siitä oliko tämä nyt oikea ratkaisu vai ei ja toimiiko se nyt varmasti herokussa... . 

Tiedon välitys turvallisesti, ja erityisesti mitkä ovat "Industry best practices" on monessa tilanteessa ollut arvailujen varassa ja mielestäni tietoturvan suhteen ei pitäisi joutua nojautumaan googlettamiseen.
