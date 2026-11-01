# Funkuframsýningin · Snar

Funkur, sum næmingar hava gjørt í Funkusmiðjuni í *Kota og vitlíki* á Snar.
Síðan: https://snarportal.github.io/funkur/

Bert Snar leggur út. Lærarar senda funkurnar til snar.portal@gmail.com í einari zip-fílu.

## Soleiðis verður ein funka løgd út

1. Goym zip-fíluna frá læraranum.
2. Koyr skriptið: `python -I legg-funkur-afturat.py "leið\til\funkur.zip"`
   Fílurnar koma í `funkur/`, og ein linja fyri hvørja funku kemur í `funkur.json` við `"vis": false`.
3. Kanna hvørja funku: eingi eftirnøvn ella persónligar upplýsingar, eingin leinkja út, og at hon riggar.
4. Skriva eitt gott `heiti` og eina stutta `lysing` í `funkur.json`, og set `"vis": true`.
5. Legg `funkur/` og `funkur.json` upp á GitHub.

## Fílurnar

- `index.html` – framsýningin (kort, filtur, leiting, «Royn», «Sí kotuna», «Broyt»)
- `ritil.html` – ritilin; `ritil.html?f=funkur/xxx.html` letur eina funku upp
- `funkur.json` – listin yvir funkurnar
- `funkur/` – sjálvar funkurnar
- `felags.css` – felags stílur

Hvør funka koyrir í einari trygdarramma (`sandbox="allow-scripts"` uttan `allow-same-origin`), so hon ikki kann síggja ella broyta nakað annað á síðuni.
