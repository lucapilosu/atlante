# Registro delle versioni

## v0.44 · 18 novembre 2026
- Mappa: il pulsante "Apri scheda" nel popup era quasi invisibile (testo chiaro su fondo chiaro); ora è leggibile in tutte e cinque le palette.
- Mappa: il popup non copre più il punto toccato. Si apre sopra il punto se c'è spazio, altrimenti sotto; la freccia indica sempre il punto; evita la barra temporale e la navigazione in basso; segue il punto quando si scorre la pagina o si fa zoom sulla mappa. Prima, su iPhone, il riquadro della mappa lo ritagliava e lo spingeva sopra il punto.
- Timeline: su desktop la rotella scorre la finestra temporale anche quando il puntatore è sopra una barra (prima si fermava).
- Footer: indicava "versione 0.34"; ora la versione è allineata a titolo e intestazione.
- Aggiunti i test automatici di regressione (`tests/regression.py`), eseguiti su desktop e iPhone 13 emulato.

Difetto noto, non corretto: i filtri della mappa "Civiltà e culture", "Siti" e "Reti e idee" non nascondono alcun punto (la funzione di filtro esiste ma non viene mai chiamata). Da decidere quali tipologie vanno sotto ciascun filtro.

## v0.43 · 17 novembre 2026 (base ereditata)
Versione sviluppata con ChatGPT e consegnata con il pacchetto di handover. Alla scelta di un risultato di ricerca: campo svuotato, anteprima e tastiera chiuse, scheda aperta.
