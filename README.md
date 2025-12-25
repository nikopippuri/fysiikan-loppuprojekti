# Fysiikan lopputyö - Askelten laskenta ja reitin näyttäminen

Tämä Streamlit-sovellus laskee askelten määrän kiihtyvyysdatan perusteella ja näyttää reitin kartalla GPS-datan avulla.

## Asennus

1. Varmista, että sinulla on Python asennettuna (versio 3.8 tai uudempi)

2. **Luo virtuaaliympäristö (suositeltu):**
   
   Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   Linux/Mac:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Asenna tarvittavat kirjastot:
   ```bash
   pip install -r requirements.txt
   ```

   Tai asenna käsin:
   ```bash
   pip install streamlit streamlit-folium pandas numpy matplotlib scipy folium
   ```

## Käyttö

**Muista aktivoida virtuaaliympäristö ennen käynnistämistä!**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

Käynnistä sovellus jollakin seuraavista tavoista:

### Vaihtoehto 1: Python moduulina (suositeltu)
```bash
python -m streamlit run https://raw.githubusercontent.com/nikopippuri/fysiikan-loppuprojekti/refs/heads/main/lopputyo.py
```

### Vaihtoehto 2: Streamlit-komennolla (jos streamlit on PATH:ssa)
```bash
streamlit run https://raw.githubusercontent.com/nikopippuri/fysiikan-loppuprojekti/refs/heads/main/lopputyo.py
```

Sovellus avautuu automaattisesti selaimessa osoitteessa `http://localhost:8501`

**Poistu virtuaaliympäristöstä kun olet valmis:**
```bash
deactivate
```

## Riippuvuudet

- streamlit - Web-sovelluskehys
- streamlit-folium - Karttanäkymä Streamlitissä
- pandas - Data-analyysi
- numpy - Numeeriset laskelmat
- matplotlib - Graafit
- scipy - Signaalinkäsittely
- folium - Karttanäkymät

## Huomio

Sovellus lataa CSV-tiedostot suoraan GitHubista. Varmista, että sinulla on internet-yhteys käynnistyessä.

