def sum_eur_cent(eur, cent):
    money_in_cents = 100 * eur + cent
    new_eur = money_in_cents // 100
    new_cent = money_in_cents % 100
    return (new_eur, new_cent)

def to_cents(eur, cent):
    eur_cent = sum_eur_cent(eur, cent)
    return 100 * eur_cent[0] + eur_cent[1]
