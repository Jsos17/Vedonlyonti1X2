# Käyttäjätarinat/User stories

* Admin voi lisätä, muokata, nähdä ja poistaa otteluita (CRUD) (poisto ehdollinen)

* Admin voi liittää otteluihin vetokohteita (Betting_offer), kertoimet määrittyvät automaattisesti todennäköisyyksien ja palautusprosentin perusteella, mutta niitä voi myös muokata (yli 90 % aiheuttaa tällä hetkellä pienemmän kuin 1 kertoimen palautusprosentin vuoksi, jolloin lomaketta ei hyväksytä ilman kertoimien alentamista)

* Pelaaja voi rekisteröityä, muokata tiliä, nähdä tilinsä tiedot, ja poistaa tilinsä (CRUD) (poisto ehdollinen)
(poisto toiminto otettu hetkellisesti pois käytöstä, jotta joku ei käy poistamasta pelaaja1 tiliä)

* Pelaaja voi rekisteröityä ja sen jälkeen lyödä vetoa liittämällä vetokuponkiin (Bet_coupon) yhden tai useamman vetokohteen (Betting_offer) (tällä hetkellä vetokunkiin voi liitttä yhden kohteen)

* Vedon ja vetokohteen muodostama yhteys yksilöidään Betting_offer_of_coupon-taulussa

* Pelaaja voi tarkastella vetohistoriaansa

* Admin voi tarkastella kaikki vetoja ja vetokohteiden vaihtoja 
