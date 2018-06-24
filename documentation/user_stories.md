# Käyttäjätarinat/User stories

* Admin voi lisätä, muokata, nähdä ja poistaa otteluita (CRUD) (Poisto ehdollinen: riippuu siitä onko otteluun lisätty vetokohde eli betting_offer). Tuloksen asettamiseen on erillinen linkki ja muiden ottelun attribuuttien muokkaukseen oma näkymä. Tulos voidaan asettaa yhden kerran (tbd:stä -> void, 1, x, 2).

* Tuloksen asetuksessa adminin pitää näppäillä kaksi kertaa sama tulos, jotta vältytään huolimattomuusvirheiltä, koska tuloksen asetus käynnistää mahdollisesti voitonmaksuja pelaajille.

* Admin voi liittää otteluihin vetokohteita (Betting_offer), kertoimet määrittyvät automaattisesti todennäköisyyksien ja palautusprosentin perusteella, mutta niitä voi myös muokata (yli 90 % aiheuttaa tällä hetkellä pienemmän kuin 1 kertoimen palautusprosentin vuoksi, jolloin lomaketta ei hyväksytä ilman kertoimien alentamista)

* Admin voi poistaa vetokohteen, jos siitä ei ole lyöty vetoa (CRUD)

* Pelaaja voi rekisteröityä, muokata tilitietoja (salasana, saldo), nähdä tilinsä tiedot, ja poistaa tilinsä (CRUD). Poisto on ehdollinen siten, että pelaajan kaikkien vetokuponkien tulee olla ratkennut. Eli jos yhdenkin bet_couponin bet_status on "tbd", niin poistoa ei sallita. 

* Kun pelaaja poistaa tilinsä, niin jos hänellä on ollut olemassa pelikuponkeja, niin niiden vierasavaimeksi tulee null, eli pelaajaan liittyviä pelikuponkeja ei poisteta järjestelmästä.

* Pelaaja voi muuttaa salasanaansa

* Pelaaja voi siirtää rahaa tililleen ja rahaa pois tililtä

* Pelaaja voi rekisteröityä, jonka jälkeen hän voi kirjautua ja siirtää tililleen rahaa. Sen jälkeen hän voi lyödä vetoa liittämällä vetokuponkiin (Bet_coupon) yhden tai useamman vetokohteen (Betting_offer)

* Admin voi tarkastella vetokohteisiin pelattua rahamäärää ja kuinka monella kupongilla kohde on (turnover statistics).

* Lisäksi admin voi tarkastella tarkemmin yksittäisen kohteen pelivaihdon jakautumista eri vaihtoehtojen kesken

* Admin voi asettaa ottelun tuloksen, ja sen jälkeen kaikki tuloksesta riippuvien tietokohteiden tapahtumat käynnistyvät:
  
  Kupongilla olevien vetokohteiden statuksen päivitys ("hit", "miss" tai "nil", kupongin merkitseminen voitoksi, tappioksi tai mitätöidyksi ("win", "loss", "void), pelaajan saldon lisäys,jos kuponki on voitollinen. Jos yksikin kohde kupongilla on väärin, niin kuponki merkitään heti tappioksi, vaikka osa kupongilla olevista muista kohteista olisi vielä ratkeamatta.  
    
    Jos ottelun tulos on void, eli ottelu on mitätöity, niin silloin kaikki kyseisen ottelun vetokohteeseen liittyvien betting_offer_of_coupon:ien status arvoksi asetetaan "nil" ja vastaavasti bet_coupon:in bet_status arvoksi asetetaan "void". Tämä tarkoittaa sitä, että kaikille pelaajille, joilla on kupongissa mitätöity ottelu palautetaan panokset. Eli vaikka kaikki muut ottelut olisivat oikein, niin yhdenkin ottelun mitätöinti aiheuttaa panoksien palautuksen. Todellisuudessa ottelutuloksien mitätöinti on hyvin harvinainen tapahtuma. 

* Pelaaja voi nähdä vetohistoriaansa pelatun rahan ja voittojen sekä vetokuponkien määrän muodossa
