# Asennusohje

Sovelluksen voi kloonata omalle koneelle komennolla

    git clone https://github.com/Jsos17/Vedonlyonti1X2.git

tai 

    git clone git@github.com:Jsos17/Vedonlyonti1X2.git

Tämän jälkeen sovelluksen koodi ja data löytyy Vedonlyonti1X2-kansiosta.

Asennetaan virtuaaliympäristön riippuvuudet samaisessa kansiossa ollessa:

    python3 -m venv venv
    
Jonka jälkeen (edelleen kansiossa Vedonlyonti1X2)

    source venv/bin/activate

Kansiossa Vedonlyonti1X2 asenna riippuvuudet komennolla:

    pip install -r requirements.txt
    
 Tarvittaessa päivitys:
 
    pip install --upgrade pip
    
Virtuaaliympäristön tietoja ei haluta versionhallintaan:

    echo "venv" > .gitignore
    
Voit luoda GitHubiin kopion omalle tilillesi (sieltä saat github-projektin osoite kts alla), jolloin heroku voi hakea muutokset suoraan sieltä.

Luodaan projektikansiolle git-versionhallinta komennolla

    git init
    
Lisätään githubissa oleva repositorio kansion paikallisen versionhallinnan etäpisteeksi, ja lisätään ja pushataan tiedostot:

    git remote add origin <github-projektin osoite>
    git add .
    git push -u origin master
 
Jäädytetään riippuvuudet herokua varten
 
    pip freeze > requirements.txt
    
 Jos requirements.txt tiedostoon päätyy rivi 
 
     pkg-resources==0.0.0 
     
 niin poista se.
Seuraavaksi tarvitset tunnuksen [Herokuun](https://signup.heroku.com/dc) ja [Heroku Command Line Interfacen](https://devcenter.heroku.com/articles/heroku-cli)

Sovellukselle luodaan paikka Herokuun komennolla (Vedonlyonti1X2-kansiossa):

    heroku create <haluttu sovelluksen nimi>

eli *heroku create* -komentoa seuraa antamasi sovelluksen nimi, tai jos jätät sen tyhjäksi niin se saa Herokun antaman satunnaisen nimen.

Saat tietää herokun antaman paikan tietokannalle komentoriviltä ja se on muotoa: 

    https://git.heroku.com/joku-app.git
    
Lisää tieto tästä paikalliseen versionhallintaan (joku-app on tietysti eri nimeltään)
 
    git remote add heroku https://git.heroku.com/joku-app.git
    
Herokuun lähetys:

    git add .
    git commit -m "Initial commit"
    git push heroku master
    
Tämän jälkeen saat tietää tietokannan osoitteen joka on muotoa https://"joku-app".herokuapp.com/

[GitHub-integraation](https://devcenter.heroku.com/articles/github-integration) avulla voit järjestää Herokussa olevan sovelluksen automaattisen päivityksen, jos teet muutoksia sovellukseen ja pushaat ne GitHubiin.
