# Käyttäjäryhmät, käyttäjätarinat ja esimerkki-SQL-kyselyitä niihin liittyen

## Käyttäjäryhmät

* Sovelluksella on oletuksena kaksi käyttäjäryhmää: CUSTOMER ja ADMIN, joille on oma taulu *Role* ja oletuksena uuteen käyttäjään liitetään aina rooli "CUSTOMER" ja komentoriviltä voi tavallisen käyttäjän asettaa "ADMIN":ksi ja suositeltavaa on, että samalla poistetaan entry "CUSTOMER" käyttäjältä, joka juuri asetettiin adminiksi. Role-taulun avulla käyttäjäryhmiä on tarpeen vaatiessa helppo laajentaa. Sovellus tallentaa tietokantaan automaattisesti Role-tauluun entryt "CUSTOMER" ja "ADMIN". Käyttäjän ja roolin välillä on liitostaulu user_role.

    ```SQL
    INSERT INTO role (name) VALUES = 'CUSTOMER';
    INSERT INTO role (name) VALUES = 'ADMIN';
    ```
    
    ```SQL
    SELECT id FROM role WHERE name = 'CUSTOMER';
    SELECT id FROM role WHERE name = 'ADMIN';
    ```
    
    Oletuksena, että customerin role_id = 1 ja adminin role_id = 2 ja olkoon bettor_id = 1
    
    ```SQL
    INSERT INTO user_role (bettor_id, role_id) VALUES (1, 1);
    INSERT INTO user_role (bettor_id, role_id) VALUES (1, 2);
    ```
    
    Poistetaan adminilta customer-rooli
    
    ```SQL
    DELETE FROM user_role WHERE bettor_id = 1 AND role_id = 1;
    ```
    Muutoksen adminiksi voi myös tehdä pelkästään päivittämällä olemassaolevaa user_role entryä (jos niitä on vain yksi, muutoin user_role tauluun tulee useampi  samalnainen entry (poislukien id) mikä ei ole erityisen toivottavaa tai hyödyllistä):
    
    ```SQL
    UPDATE user_role SET role_id = 2 WHERE user_role.bettor_id = 1;
    ```
    
## Käyttäjätarinat ja SQL-kyselyt    

* Admin voi lisätä, muokata, nähdä ja poistaa otteluita (CRUD) (Poisto ehdollinen: riippuu siitä onko otteluun lisätty vetokohde eli betting_offer). Tuloksen asettamiseen on erillinen linkki ja muiden ottelun attribuuttien muokkaukseen oma näkymä. Tulos voidaan asettaa yhden kerran (tbd:stä -> void, 1, x, 2).

    ```SQL
    INSERT INTO sport_match (home, away, prob_1, prob_x, prob_2, start_time, result_1x2)
    VALUES ('Barcelona', 'Real Madrid', 41, 28, 31, '2018-06-26 18:00:00.000000', 'tbd');
    ```
    
    ```SQL
    UPDATE sport_match SET result_1x2 = '<haluttu tulos>' WHERE id = <haluttu id>;
    ```

Tuloksen asetuksessa adminin pitää näppäillä (sovelluksessa) kaksi kertaa sama tulos, jotta vältytään huolimattomuusvirheiltä, koska tuloksen asetus käynnistää mahdollisesti voitonmaksuja pelaajille. Lisäksi lomakkeessa on erillinen BooleanField hyväksyntä painike, joka pitää olla valittuna.

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
    ```
    
    Pelaajan saldo otetaan selville, jotta siitä voidaan vähentää tai lisätä siihen haluttu määrä.
    
    ```SQL
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
Yllä *:offer_id* on käyttäjältä saatu parametri

* Admin voi asettaa ottelun tuloksen, ja sen jälkeen kaikki tuloksesta riippuvien tietokohteiden tapahtumat käynnistyvät:
  
  Kupongilla olevien vetokohteiden statuksen päivitys ("hit", "miss" tai "nil", kupongin merkitseminen voitoksi, tappioksi tai mitätöidyksi ("win", "loss", "void), pelaajan saldon lisäys,jos kuponki on voitollinen. Jos yksikin kohde kupongilla on väärin, niin kuponki merkitään heti tappioksi, vaikka osa kupongilla olevista muista kohteista olisi vielä ratkeamatta.
    
    Jos ottelun tulos on void, eli ottelu on mitätöity, niin silloin kaikki kyseisen ottelun vetokohteeseen liittyvien betting_offer_of_coupon:ien status arvoksi asetetaan "nil" ja vastaavasti bet_coupon:in bet_status arvoksi asetetaan "void". Tämä tarkoittaa sitä, että kaikille pelaajille, joilla on kupongissa mitätöity ottelu palautetaan panokset. Eli vaikka kaikki muut ottelut olisivat oikein, niin yhdenkin ottelun mitätöinti aiheuttaa panoksien palautuksen. Todellisuudessa ottelutuloksien mitätöinti on hyvin harvinainen tapahtuma.
    
    ```SQL
    UPDATE sport_match SET result_1x2 = '<haluttu tulos>' WHERE id = <haluttu id>;
    
    SELECT id FROM betting_offer WHERE match_id = <päivitetty match id>;
    UPDATE betting_offer SET active = 0, closed = 1 WHERE id = <juuri selvitetty id>;
    ```
    
    Selvitetään kaikki betting_offeriin liittyvät betting_offer_of_couponit:
    
    ```SQL
    SELECT id FROM betting_offer_of_coupon WHERE betting_offer_id = <selvitetty offer id >;
    ```
    
    Kustakin betting_offer_of_couponista selvitetään siihen liittyvä kuponki
    
    ```SQL
    SELECT bet_coupon.id FROM bet_coupon, betting_offer_of_coupon 
    WHERE bet_coupon.id = < saatu betting_offer_of_coupon>.bet_coupon_id;
    ```
    
    Jonka jälkeen mahdollisesti betting_offer_of_coupon statukseksi asetetaan "hit", "miss" tai "nil" ja bet_couponin bet_status asetetaan voitoksi, tappioksi tai mitätöidyksi
    
    ```SQL
    UPDATE betting_offer_of_coupon SET status = "hit" WHERE id = <offer_of_coupon_id>;
    UPDATE betting_offer_of_coupon SET status = "miss" WHERE id = <offer_of_coupon_id>;
    UPDATE betting_offer_of_coupon SET status = "nil" WHERE id = <offer_of_coupon_id>;
    
    UPDATE bet_coupon SET bet_status = "win" WHERE id = <saatu id>;
    UPDATE bet_coupon SET bet_status = "loss" WHERE id = <saatu id>;
    UPDATE bet_coupon SET bet_status = "void" WHERE id = <saatu id>;
    ```
    Lisäksi pelaajan tilin päivitys mahdolllisesti käynnistyy, jos kuponki merkitään voitolliseksi tai panokset palautetaan ja kuponki merkitään mitätöidyksi. Tilin saldon muuttamisen käyttäjätarina on käsitelty jo aiemmin rahan siirron yhteydessä ja toiminnallisuus on käytännössä sama.

* Pelaaja voi nähdä vetohistoriaansa pelatun rahan ja voittojen sekä vetokuponkien määrän muodossa

    ```SQL
    SELECT FROM bet_coupon WHERE bettor_id = current_user.id;
    ```
    
    Jonka jälkeen saadut kupongit on sovelluksessa käyty ohjelmallisesti läpi ja laskettu niiden voitot+panosten palautukset ja panokset erikseen. 
