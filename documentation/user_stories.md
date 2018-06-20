# Käyttäjätarinat/User stories

* Admin voi lisätä, muokata, nähdä ja poistaa otteluita (CRUD) (Poisto ehdollinen: riippuu siitä onko otteluun lisätty vetokohde eli betting_offer). Tuloksen asettamiseen on erillinen linkki ja muiden ottelun attribuuttien muokkaukseen oma näkymä. Tulos voidaan asettaa yhden kerran (tbd:stä -> void, 1, x, 2). Tähän on tarkoitus lisätä varmistustoimenpide tuloksesta (koska sitä ei voi sovelluksen kautta enää muuttaa).

* Admin voi liittää otteluihin vetokohteita (Betting_offer), kertoimet määrittyvät automaattisesti todennäköisyyksien ja palautusprosentin perusteella, mutta niitä voi myös muokata (yli 90 % aiheuttaa tällä hetkellä pienemmän kuin 1 kertoimen palautusprosentin vuoksi, jolloin lomaketta ei hyväksytä ilman kertoimien alentamista)

* Admin voi poistaa vetokohteen, jos siitä ei ole lyöty vetoa (CRUD)

* Pelaaja voi rekisteröityä, muokata tiliä, nähdä tilinsä tiedot, ja poistaa tilinsä (CRUD) (poisto ehdollinen)
(poisto toiminto otettu hetkellisesti pois käytöstä, jotta joku ei käy poistamasta pelaaja1 tiliä)

* Pelaaja voi muuttaa salasanaansa (ei toteutettu)

* Pelaaja voi lisätä tai vähentää saldoaan (toteutettu, mutta toteutustyyli on kehno, tarkoitus päivittää)

* Pelaaja voi rekisteröityä, jonka jälkeen hän voi kirjautua ja sen jälkeen lyödä vetoa liittämällä vetokuponkiin (Bet_coupon) yhden tai useamman vetokohteen (Betting_offer)

* Admin voi tarkastella vetokohteisiin pelattua rahamäärää ja kuinka monella kupongilla kohde on (turnover statistics).

* Lisäksi admin voi tarkastella tarkemmin yksittäisen kohteen pelivaihdon jakautumista eri vaihtoehtojen kesken

* Admin voi asettaa ottelun tuloksen, ja sen jälkeen kaikki tuloksesta riippuvien tietokohteiden tapahtumat käynnistyvät:
  
  Kupongilla olevien vetokohteiden statuksen päivitys ("hit" tai "miss", kupongin merkitseminen voitoksi tai tappioksi ("win" tai   "loss"), pelaajan saldon lisäys,jos kuponki on voitollinen. Jos yksikin kohde kupongilla on väärin, niin kuponki merkitään heti tappioksi, vaikka osa kupongilla olevista muista kohteista olisi vielä ratkeamatta.  
    
    Tällä hetkellä void vaihtoehtoa ei ole toteutettu. Void-vaihtoehdon tarkoitus olisi seuraava: Jos ottelu mitätöidään, niin silloin tulos merkittäisiin void, ja panokset palautettaisiin pelaajille. 

* Pelaaja voi nähdä vetohistoriaansa pelatun rahan ja voittojen sekä vetokuponkien määrän muodossa (ei toteutettu vielä/kupongeista pelkkä listaus)
