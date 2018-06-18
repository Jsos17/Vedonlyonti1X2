# Asennusohje

Sovelluksen voi kloonata omalle koneelle komennolla

    git clone https://github.com/Jsos17/Vedonlyonti1X2.git

tai 

    git clone git@github.com:Jsos17/Vedonlyonti1X2.git

Tämän jälkeen sovelluksen koodi ja data löytyy Vedonlyönti1X2-kansiosta.

Kansiossa Vedonlyonti1X2 asenna riippuvuudet komennolla:

    pip install -r requirements.txt

Seuraavaksi tarvitset tunnuksen [Herokuun](https://signup.heroku.com/dc) ja [Heroku Command Line Interfacen](https://devcenter.heroku.com/articles/heroku-cli)

Sovellukselle luodaan paikka Herokuun komennolla (Vedonlyonti1X2-kansiossa):

    heroku create <haluttu sovelluksen nimi>

eli *heroku create* -komentoa seuraa antamasi sovelluksen nimi, tai jos jätät sen tyhjäksi niin se saa Herokun antaman satunnaisen nimen.


