# 🤖 Pametno Svjetlo (Night-Light Mode) - AlphaBot2-Pi

Autonomni sustav za upravljanje rasvjetom mobilnog robota temeljen na Raspberry Pi platformi i infracrvenim (IR) podnim senzorima. Projekt automatski prepoznaje ulazak robota u tamnije prostore te upravlja LED rasvjetom u stvarnom vremenu.

---

## 📋 Sadržaj
- [O projektu](#-o-projektu)
- [Glavne značajke](#-glavne-značajke)
- [Tehnička specifikacija i princip rada](#-tehnička-specifikacija-i-princip-rada)
- [Struktura koda](#-struktura-koda)
- [Zaključak i analiza](#-zaključak-i-analiza)
- [Autor](#-autor)

---

## 🚀 O projektu
U razvoju modernih mobilnih robota, prilagodba uvjetima okoline ima ključnu ulogu. Ovaj projekt rješava problem autonomnog upravljanja osvjetljenjem s ciljem:
* **Energetske učinkovitosti:** Automatskim gašenjem rasvjete na svjetlu štedi se energija baterije.
* **Poboljšanja navigacije:** Uključivanjem dodatnog svjetla u tamnim zonama osigurava se stabilniji rad senzora i sigurnije kretanje robota.
* **Svijesti o kontekstu (Context Awareness):** Prepoznavanje okruženja poput baze, prolaznih zona ili garaža.

---

## 🛠️ Glavne značajke
- **Nisko-razinski bit-banging SPI protokol:** Ručno upravljanje GPIO linijama za komunikaciju s TLC1543 ADC pretvaračem.
- **Uzorci i filtriranje prosjeka:** Prikupljanje podataka sa svih 5 IR senzora uz izračun aritmetičke sredine radi smanjenja utjecaja šuma.
- **Dinamička dvostruka kalibracija:** Interaktivni postupak u dva koraka (svijetli i tamni prostor) kojim se automatski izračunava optimalni prag detekcije (*threshold*).
- **Kontinuirano praćenje u realnom vremenu:** Petlja koja svakih 50 ms provjerava stanje senzora i donosi odluke o paljenju/gašenju rasvjete.

---

## ⚙️ Tehnička specifikacija i princip rada

Infracrveni senzori na donjoj strani robota sastoje se od IR diode (odašiljača) i fototranzistora (prijamnika). Jačina reflektiranog signala ovisi o refleksivnim svojstvima podloge:
* Svjetlije površine reflektiraju više IR zračenja.
* Tamne i matirane površine apsorbiraju veći dio zračenja.

### Arhitektura koda (`alphabot2_night_light_mode.py`)
1. **Inicijalizacija i SPI komunikacija (`setup_all` & `_perform_bit_bang`):** Postavljanje BCM načina rada GPIO pinova i slanje 4-bitne adrese prema ADC-u.
2. **Uzorci senzora (`get_sensors_average`):** Čitanje vrijednosti svih 5 kanala i vraćanje srednje vrijednosti.
3. **Kalibracija (`calibrate_garage`):** Snimanje 20 uzastopnih uzoraka u svijetlom i tamnom prostoru te izračun srednje granične vrijednosti.
4. **Glavna petlja (`run_garage_light`):** Neprekidno praćenje stanja i ispis kontrolnih signala (`1` za paljenje, `0` za gašenje rasvjete).

---

## 📊 Zaključak iz eksperimenata
Rezultati pokazuju da sustav postiže iznimno stabilne performanse u uvjetima s izraženim kontrastom između svijetlih i tamnih površina. U graničnim slučajevima s kompleksnim materijalima (sličnih refleksivnih svojstava) dolazi do smanjenja razlike između kalibracijskih stanja, što naglašava važnost kvalitetne kalibracije okoline.

---

## 👤 Autor
* **Lara Lacić**
* Fakultet elektrotehnike, računarstva i informacijskih tehnologija Osijek (FERIT)[cite: 4]
* Sveučilišni diplomski studij Računarstvo[cite: 4]
