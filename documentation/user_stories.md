# Käyttäjätarinat/User stories

* Admin voi lisätä, muokata, nähdä ja poistaa otteluita (CRUD) (Poisto ehdollinen: riippuu siitä onko otteluun lisätty vetokohde eli betting_offer)

* Admin voi liittää otteluihin vetokohteita (Betting_offer), kertoimet määrittyvät automaattisesti todennäköisyyksien ja palautusprosentin perusteella, mutta niitä voi myös muokata (yli 90 % aiheuttaa tällä hetkellä pienemmän kuin 1 kertoimen palautusprosentin vuoksi, jolloin lomaketta ei hyväksytä ilman kertoimien alentamista)

* Admin voi poistaa vetokohteen, jos siitä ei ole lyöty vetoa (CRUD)

* Pelaaja voi rekisteröityä, muokata tiliä, nähdä tilinsä tiedot, ja poistaa tilinsä (CRUD) (poisto ehdollinen)
(poisto toiminto otettu hetkellisesti pois käytöstä, jotta joku ei käy poistamasta pelaaja1 tiliä)

* Pelaaja voi rekisteröityä, jonka jälkeen hän voi kirjautua ja sen jälkeen lyödä vetoa liittämällä vetokuponkiin (Bet_coupon) yhden tai useamman vetokohteen (Betting_offer)

* Vedon ja vetokohteen muodostama yhteys yksilöidään Betting_offer_of_coupon-taulussa

* Admin voi tarkastella kaikki vetokohteisiin pelattua rahamäärää ja kuinka monella kupongilla kohde on (turnover statistics).

* Lisäksi admin voi tarkastella tarkemmin yksittäisen kohteen pelivaihdon jakautumista eri vaihtoehtojen kesken
