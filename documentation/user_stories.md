# Käyttäjätarinat/User stories ja esimerkki-SQL-kyselyitä niihin liittyen

* Admin voi lisätä, muokata, nähdä ja poistaa otteluita (CRUD) (Poisto ehdollinen: riippuu siitä onko otteluun lisätty vetokohde eli betting_offer). Tuloksen asettamiseen on erillinen linkki ja muiden ottelun attribuuttien muokkaukseen oma näkymä. Tulos voidaan asettaa yhden kerran (tbd:stä -> void, 1, x, 2).

    ```SQL
    INSERT INTO sport_match (home, away, prob_1, prob_x, prob_2, start_time, result_1x2)
    VALUES ('Barcelona', 'Real Madrid', 41, 28, 31, '2018-06-26 18:00', 'tbd');
    ```
    
    ```SQL
    UPDATE sport_match SET result_1x2 = '<haluttu tulos>' WHERE id = <haluttu id>;
    ```

* Tuloksen asetuksessa adminin pitää näppäillä kaksi kertaa sama tulos, jotta vältytään huolimattomuusvirheiltä, koska tuloksen asetus käynnistää mahdollisesti voitonmaksuja pelaajille.

* Admin voi liittää otteluihin vetokohteita (Betting_offer), kertoimet määrittyvät automaattisesti todennäköisyyksien ja palautusprosentin perusteella, mutta niitä voi myös muokata (yli 90 % aiheuttaa tällä hetkellä pienemmän kuin 1 kertoimen palautusprosentin vuoksi, jolloin lomaketta ei hyväksytä ilman kertoimien alentamista)

     ```SQL
     INSERT INTO betting_offer (match_id, odds_1, odds_x, odds_2, max_stake, active, closed)
     VALUES (<haluttu id>, 2.71, 3.31, 2.24, 100.0, 1, 0);
     ```

* Admin voi poistaa vetokohteen, jos siitä ei ole lyöty vetoa ja kun se on asetettu ei-aktiiviseksi (CRUD)

    ```SQL
    SELECT * FROM betting_offer_of_coupon WHERE betting_offer_id = <haluttu id>:
    ```
    
    Jos tämä haku ei tuota tulosta, kohteen voi poistaa jos se on ei-aktiivinen. Tässä vain asetus ei-aktiiviseksi
    
    ```SQL
    UPDATE betting_offer SET active = 0 WHERE id = <haluttu id>;
    ```
    
    Itse poisto:
    
    ```SQL
    DELETE FROM betting-offer WHERE id = <haluttu id>;

* Pelaaja voi rekisteröityä, muokata tilitietoja (salasana, saldo), nähdä tilinsä tiedot, ja poistaa tilinsä (CRUD). Poisto on ehdollinen siten, että pelaajan kaikkien vetokuponkien tulee olla ratkennut. Eli jos yhdenkin bet_couponin bet_status on "tbd", niin poistoa ei sallita.

    ```SQL
    INSERT INTO bettor (username, password, balance_eur, balance_cent) 
    VALUES ('akuankka', '$5$rounds=535000$.HMHKCwt/FrPsre7$yD.iNvoNjrMd6mdtwHRrYZK1.5WGyMLFl75WvTCwkP2',0,0);
    ```
    
    ```SQL
    SELECT * FROM bettor WHERE username = 'akuankka';
    ```
    
    ```SQL
    DELETE FROM bettor WHERE id = <haluttu id>;
    ```

* Kun pelaaja poistaa tilinsä, niin jos hänellä on ollut olemassa pelikuponkeja, niin niiden vierasavaimeksi tulee null, eli pelaajaan liittyviä pelikuponkeja ei poisteta järjestelmästä.

    ```SQL
    DELETE FROM bettor WHERE id = <haluttu id>
    ```

* Pelaaja voi muuttaa salasanaansa

    ```SQL
    UPDATE bettor 
    SET password = '$5$rounds=535000$.HMHKCwt/FrPsre7$yD.iNvoNjrMd6mdtwHRrYZK1.5WGyMLFl75WvTCwkP2' 
    WHERE id = <haluttu id>;
    ```
    Tässä salasana on hashatyssä muodossa kuten se tallennetaan tietokantaankin
    
* Pelaaja voi siirtää rahaa tililleen ja rahaa pois tililtä

    ```SQL
    SELECT balance_eur, balance_cent FROM bettor WHERE id = <haluttu id>;
    
    UPDATE bettor SET balance_eur = <uusi_arvo>, balance_cent = <uusi arvo>
    WHERE id = <haluttu id>;
    ```

* Pelaaja voi rekisteröityä, jonka jälkeen hän voi kirjautua ja siirtää tililleen rahaa. Sen jälkeen hän voi lyödä vetoa liittämällä vetokuponkiin (Bet_coupon) yhden tai useamman vetokohteen (Betting_offer_of_coupon)

    ```SQL
    INSERT INTO bet_coupon (bettor_id, combined_odds, stake_eur, stake_cent, possible_win_eur,
    possible_win_cent, bet_status) VALUES (<pelaajan id>, 1, 0, 0, 0, 0, 'no bets');
    
    UPDATE bet_coupon SET combined_odds = <yhteiskerroin>, stake_eur= <panos>, stake_cent = <panos>,
    possible_win_eur = <laskettu>, possible_win_cent = <laskettu>, bet_status = 'tbd'
    WHERE id = <haluttu id>;
    ```
    
    Eli ensin luodaan tyhjä kuponki, ja kun siihen on liitetty Betting_offer_of_couponeja niin niiden perusteella lasketaan yhteiskerroin, asetetaan panos ja edellisten perusteella lasketaan mahdollinen voitto ja lopulta päivitetään kuponki.
    
    

* Admin voi tarkastella vetokohteisiin pelattua rahamäärää ja kuinka monella kupongilla kohde on (turnover statistics).

    ```SQL
    SELECT sport_match.home, sport_match.away, sport_match.id, betting_offer.id, 
    COUNT(bet_coupon.id), SUM(bet_coupon.stake_eur), SUM(bet_coupon.stake_cent), sport_match.start_time 
    FROM sport_match, betting_offer, bet_coupon, betting_offer_of_coupon 
    WHERE betting_offer.match_id = sport_match.id 
    AND betting_offer_of_coupon.betting_offer_id = betting_offer.id 
    AND betting_offer_of_coupon.bet_coupon_id = bet_coupon.id 
    GROUP BY sport_match.id, betting_offer.id;
    ```

* Lisäksi admin voi tarkastella tarkemmin yksittäisen kohteen pelivaihdon jakautumista eri vaihtoehtojen kesken

    ```SQL
    SELECT sport_match.home, sport_match.away, COUNT(bet_coupon.id), 
    betting_offer_of_coupon.choice_1x2, SUM(bet_coupon.stake_eur), SUM(bet_coupon.stake_cent), 
    sport_match.prob_1, sport_match.prob_x, sport_match.prob_2 
    FROM sport_match, betting_offer, bet_coupon, betting_offer_of_coupon 
    WHERE betting_offer_id = :offer_id AND betting_offer.match_id = sport_match.id 
    AND betting_offer_of_coupon.betting_offer_id = betting_offer.id 
    AND betting_offer_of_coupon.bet_coupon_id = bet_coupon.id 
    GROUP BY sport_match.id, betting_offer_of_coupon.choice_1x2;
    ```
Yllä *:offer* on käyttäjältä saatu parametri

* Admin voi asettaa ottelun tuloksen, ja sen jälkeen kaikki tuloksesta riippuvien tietokohteiden tapahtumat käynnistyvät:
  
  Kupongilla olevien vetokohteiden statuksen päivitys ("hit", "miss" tai "nil", kupongin merkitseminen voitoksi, tappioksi tai mitätöidyksi ("win", "loss", "void), pelaajan saldon lisäys,jos kuponki on voitollinen. Jos yksikin kohde kupongilla on väärin, niin kuponki merkitään heti tappioksi, vaikka osa kupongilla olevista muista kohteista olisi vielä ratkeamatta.
    
    Jos ottelun tulos on void, eli ottelu on mitätöity, niin silloin kaikki kyseisen ottelun vetokohteeseen liittyvien betting_offer_of_coupon:ien status arvoksi asetetaan "nil" ja vastaavasti bet_coupon:in bet_status arvoksi asetetaan "void". Tämä tarkoittaa sitä, että kaikille pelaajille, joilla on kupongissa mitätöity ottelu palautetaan panokset. Eli vaikka kaikki muut ottelut olisivat oikein, niin yhdenkin ottelun mitätöinti aiheuttaa panoksien palautuksen. Todellisuudessa ottelutuloksien mitätöinti on hyvin harvinainen tapahtuma. 

* Pelaaja voi nähdä vetohistoriaansa pelatun rahan ja voittojen sekä vetokuponkien määrän muodossa
