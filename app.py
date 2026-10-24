import streamlit as st
import datetime
from fpdf import FPDF
import base64

# ==========================================
# 1. PAGINA CONFIGURATIE & HUISSTIJL (CSS)
# ==========================================
st.set_page_config(
    page_title="SiMa Poorten — Premium Configurator",
    page_icon="🚪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling voor een luxe uitstraling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 18px;
        border-left: 5px solid #1E3A8A;
        margin-bottom: 15px;
    }
    .price-tag {
        font-size: 1.8rem;
        font-weight: bold;
        color: #059669;
    }
    .stButton>button {
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🚪 SiMa Poorten — Toonzaal Configurator & Offerte</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Interne applicatie voor prijsberekening, advies en directe PDF-generatie</p>', unsafe_allow_html=True)

# ==========================================
# 2. PDF GENERATOR KLASSE (FPDF2)
# ==========================================
class OffertePDF(FPDF):
    def header(self):
        # Blauwe hoofdbalk
        self.set_fill_color(30, 58, 138) # SiMa Blauw
        self.rect(0, 0, 210, 25, 'F')
        
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, 'SiMa POORTEN — OFFICIELE OFFERTE', 0, 1, 'L')
        self.ln(5)

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, 'SiMa Poorten BVBA - Kwaliteit & Vakmanschap in Poorten en Hekwerk', 0, 1, 'C')
        self.cell(0, 5, f'Pagina {self.page_no()}', 0, 0, 'C')

def genereer_pdf(klant, configuratie, prijs_details, totaal_excl, btw_bedrag, totaal_incl, levertermijn):
    pdf = OffertePDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Datum & Documentnummer
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 10)
    pdf.ln(5)
    pdf.cell(100, 6, f"Datum: {datetime.date.today().strftime('%d-%m-%Y')}", 0, 0)
    pdf.cell(90, 6, f"Offertenummer: SIMA-{datetime.datetime.now().strftime('%Y%m%d%H%M')}", 0, 1, 'R')
    pdf.ln(5)

    # Klant- & Projectgegevens
    pdf.set_fill_color(240, 243, 246)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(190, 7, "  KLANT- & PROJECTGEGEVENS", 0, 1, 'L', fill=True)
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(95, 6, f"Klantnaam: {klant['naam']}", 0, 0)
    pdf.cell(95, 6, f"Projecttype: {klant['project']}", 0, 1)
    pdf.cell(95, 6, f"Adres: {klant['adres']}", 0, 0)
    pdf.cell(95, 6, f"Telefoon: {klant['tel']}", 0, 1)
    pdf.cell(95, 6, f"E-mail: {klant['email']}", 0, 1)
    pdf.ln(5)

    # Specificaties
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(190, 7, "  CONFIGURATIE & SPECIFICATIES", 0, 1, 'L', fill=True)
    pdf.set_font('Arial', '', 10)
    
    for key, val in configuratie.items():
        pdf.cell(70, 6, f"{key}:", 0, 0)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(120, 6, f"{val}", 0, 1)
        pdf.set_font('Arial', '', 10)
    
    pdf.ln(5)

    # Prijsopbouw Tabel
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(190, 7, "  PRIJSBEREKENING", 0, 1, 'L', fill=True)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(130, 7, "Omschrijving", 1, 0)
    pdf.cell(60, 7, "Bedrag (€)", 1, 1, 'R')
    
    pdf.set_font('Arial', '', 10)
    for omschrijving, bedrag in prijs_details:
        pdf.cell(130, 6, f" {omschrijving}", 1, 0)
        pdf.cell(60, 6, f"€ {bedrag:,.2f} ", 1, 1, 'R')
        
    # Totalen
    pdf.ln(3)
    pdf.cell(130, 6, "Subtotaal Excl. BTW", 0, 0, 'R')
    pdf.cell(60, 6, f"€ {totaal_excl:,.2f}", 1, 1, 'R')
    
    pdf.cell(130, 6, f"BTW ({klant['btw_tarief']}%)", 0, 0, 'R')
    pdf.cell(60, 6, f"€ {btw_bedrag:,.2f}", 1, 1, 'R')
    
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(130, 7, "TOTAAL INCLUSIEF BTW", 0, 0, 'R')
    pdf.cell(60, 7, f"€ {totaal_incl:,.2f}", 1, 1, 'R')

    pdf.ln(8)
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 6, f"Verwachte levertermijn: {levertermijn}", 0, 1)
    pdf.cell(0, 6, "Offerte geldig tot 30 dagen na datum.", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1', errors='replace')

# ==========================================
# 3. SIDEBAR: KLANTGEGEVENS & INSTELLINGEN
# ==========================================
st.sidebar.header("👤 Klant & Project")
klant_naam = st.sidebar.text_input("Naam klant", "Familie Janssens")
klant_adres = st.sidebar.text_input("Adres / Werfadres", "Dorpstraat 12, Keerbergen")
klant_email = st.sidebar.text_input("E-mailadres", "klant@example.com")
klant_tel = st.sidebar.text_input("Telefoonnummer", "0470 12 34 56")

project_type = st.sidebar.radio("Projecttype", ["Nieuwbouw", "Vervanging bestaande poort"])
btw_percentage = st.sidebar.selectbox("BTW Tarief", [6, 21], index=0, help="6% voor renovatie/vervanging > 10 jaar oud, anders 21%")

if project_type == "Vervanging bestaande poort":
    st.sidebar.info("💡 **Verkooptip:** Vraag naar de bestaande dagmaten en controleer of het railsysteem herbruikbaar is.")

st.sidebar.divider()

# Instelling basisprijzen (beheerderspaneel in klapmenu)
with st.sidebar.expander("⚙️ Prijsinstellingen (Aanpasbaar)"):
    basis_m2_prijs = st.number_input("Basisprijs per m² (€)", value=220)
    prijs_sima100 = st.number_input("Meerkost SiMa 100 (€)", value=250)
    prijs_60mm = st.number_input("Meerkost 60mm panelen (€)", value=300)
    prijs_uv = st.number_input("Meerkost UV-coating (€)", value=120)
    prijs_kleurmatch = st.number_input("Meerkost Kleurmatch (€)", value=150)
    prijs_loopdeur = st.number_input("Meerkost Loopdeur (€)", value=750)
    prijs_motor = st.number_input("Sommer Motor set (€)", value=450)
    prijs_nood_buiten = st.number_input("Noodontkoppeling buiten (€)", value=125)

# ==========================================
# 4. HOOFDSCHERM CONFIGURATOR
# ==========================================
col_config, col_summary = st.columns([2, 1.2])

prijs_details = []
configuratiefiche = {}

with col_config:
    st.subheader("1. Poort- & Materiaalkeuze")
    
    categorie = st.selectbox(
        "Categorie", 
        ["Sectionaalpoort (Staal)", "Houten Poort", "Hekwerk (Schuif/Draai)"]
    )
    configuratiefiche["Categorie"] = categorie
    
    # AFMETINGEN
    st.write("---")
    st.write("**Afmetingen (in millimeters)**")
    c_w, c_h = st.columns(2)
    breedte = c_w.number_input("Breedte (mm)", min_value=1000, max_value=8000, value=3000, step=100)
    hoogte = c_h.number_input("Hoogte (mm)", min_value=1000, max_value=4000, value=2125, step=25)
    
    oppervlakte_m2 = (breedte / 1000) * (hoogte / 1000)
    configuratiefiche["Afmetingen"] = f"{breedte} mm (B) x {hoogte} mm (H) [{oppervlakte_m2:.2f} m²]"
    
    # Bereken basisprijs
    basisprijs_berekend = oppervlakte_m2 * basis_m2_prijs
    prijs_details.append((f"Basisconstructie ({oppervlakte_m2:.2f} m²)", basisprijs_berekend))

    # Constructie-regels
    dubbel_beslag = breedte >= 5000 or categorie == "Houten Poort"
    if dubbel_beslag:
        st.warning("⚠️ **Automatische regel:** Dubbel beslag & verstevigingstrushen zijn verplicht voorzien (windbelasting & doorbuigen).")
        prijs_details.append(("Dubbel beslag & verstevigingstrushen", 180.0))
        configuratiefiche["Extra constructie"] = "Dubbel beslag + Verstevigingstrushen"

    # SPECIFIEK PER CATEGORIE
    if categorie == "Sectionaalpoort (Staal)":
        st.write("---")
        st.write("**Railsysteem & Panelen**")
        
        rail = st.radio(
            "Railsysteem", 
            ["SiMa Economy line (Trekveren)", "SiMa 80 (Torsieveren - Middensegment)", "SiMa 100 (Torsieveren - Luxe Topafwerking)"],
            index=2
        )
        configuratiefiche["Railsysteem"] = rail
        if "SiMa 100" in rail:
            prijs_details.append(("Luxe Railsysteem SiMa 100", float(prijs_sima100)))
            
        st.markdown("""
        <div class="card">
            👉 <b>Toonzaal-actie:</b> Neem de klant mee naar de railsystemen-wand! Laat hen het gewichtsverschil van de torsieveren en de dikte van de SiMa 100 rail voelen.
        </div>
        """, unsafe_allow_html=True)

        dikte = st.selectbox("Paneeldikte", ["40 mm (Standaard - min. 0,8mm staal)", "60 mm (Passiefbouw / Max. Isolatie)"])
        configuratiefiche["Paneeldikte"] = dikte
        
        if "60 mm" in dikte:
            prijs_details.append(("Isolatiepanelen 60mm (Passief)", float(prijs_60mm)))
            st.success("🌱 **Isolatie:** U-waarde = 0,29 W/m²K. Enkel vlak of structuurlak mogelijk.")
            profiel = "Vlak"
            structuur = st.selectbox("Oppervlakte", ["Vlak (Egaal)", "Structuurlak"])
        else:
            profiel = st.selectbox("Profieltype", ["Vlak", "Gelijnd (om 10cm)", "Middenprofilering", "Topprofilering", "Balkmotief"])
            structuur = st.selectbox("Oppervlakte-afwerking", ["Vlak", "Stucco (Fijne korrel)", "Houtmotief (Reliëf)", "Microline", "Houtimitatie (Folie)"])
        
        configuratiefiche["Profilering & Structuur"] = f"{profiel} / {structuur}"

        if structuur == "Houtimitatie (Folie)":
            hout_folie = st.selectbox("Houtimitatie tint (toonzaalvolgorde)", [
                "1. Rustieke eik", "2. Mahonie", "3. Donkere eik", "4. Lichte eik"
            ])
            st.info(f"👉 **Toonzaal-actie:** Toon staal **'{hout_folie}'** aan de wand.")
            configuratiefiche["Houtfolie"] = hout_folie

        st.write("---")
        st.write("**Kleur & Bescherming**")
        kleur_type = st.radio("Kleurkeuze", ["Standaard RAL-kleur", "Eigen staal namaken (Kleurmatch)"])
        if kleur_type == "Eigen staal namaken (Kleurmatch)":
            st.warning("📌 Klant moet staal van 20x5 cm binnenbrengen. Langere levertermijn.")
            prijs_details.append(("Kleurmatch op staal", float(prijs_kleurmatch)))
            configuratiefiche["Kleur"] = "Eigen staal (Kleurmatch)"
        else:
            ral_code = st.text_input("RAL Kleurcode (bijv. RAL 7016 Antraciet)", "RAL 7016")
            configuratiefiche["Kleur"] = f"Standaard {ral_code}"

        uv_coating = st.checkbox("UV-coating (voorkomt afschijnen/verkleuring)")
        if uv_coating:
            prijs_details.append(("UV-coating beschermlaag", float(prijs_uv)))
            configuratiefiche["Extra laklaag"] = "Inclusief UV-Coating"

        # Loopdeur
        st.write("---")
        st.write("**Opties & Deuren**")
        kan_loopdeur = not ("60 mm" in dikte or profiel == "Topprofilering")
        if kan_loopdeur:
            loopdeur = st.checkbox("Geïntegreerde Loopdeur (Draait enkel naar buiten)")
            if loopdeur:
                prijs_details.append(("Geïntegreerde Loopdeur", float(prijs_loopdeur)))
                configuratiefiche["Loopdeur"] = "Ja (Inclusief trush en lage drempel)"
        else:
            st.caption("🚫 *Loopdeur is niet mogelijk i.c.m. 60mm panelen of topprofilering.*")
            loopdeur = False

    elif categorie == "Houten Poort":
        st.write("---")
        st.write("**Houtsoort & Uitvoering**")
        st.markdown("""
        <div class="card">
            👉 <b>Toonzaal-actie:</b> Wijs de 'Pastorij' opstelling aan met de makelaar, plint en knots.
        </div>
        """, unsafe_allow_html=True)
        
        houtsoort = st.selectbox("Houtsoort", [
            "Afzelia (Zeer stabiel, leeft weinig)",
            "Padoek (Stabiel, roodachtig in begin)",
            "Afrormosia (Unieke vlamtekening)",
            "Eik (Klassiek, leeft sterk)",
            "Meranti (Ideaal om te lakken)"
        ])
        behandeling = st.radio("Afwerking", ["Onbehandeld (natuurlijk vergrijzen)", "Behandelen met Rubio Monocoat"])
        
        configuratiefiche["Houtsoort"] = houtsoort
        configuratiefiche["Behandeling"] = behandeling
        prijs_details.append((f"Houtuitvoering ({houtsoort.split(' ')[0]})", 450.0))

    elif categorie == "Hekwerk (Schuif/Draai)":
        st.write("---")
        st.write("**Type Hekwerk**")
        hek_type = st.radio("Uitvoering", ["Vrijdragend schuifhekwerk", "Schuifhekwerk op rail", "Dubbele vleugel (Draaihek)"])
        configuratiefiche["Hekwerk type"] = hek_type
        
        if hek_type == "Schuifhekwerk op rail":
            st.warning("🌲 **Advies:** Bosrijke omgeving of gravel oprit? Raad **Vrijdragend** aan om vuil in de rail te voorkomen!")

    # Motorisatie
    st.write("---")
    st.write("**Motorisatie & Accessoires**")
    motor = st.checkbox("Sommer-motor set (Inclusief 2 zenders & onderloopbeveiliging)", value=True)
    if motor:
        prijs_details.append(("Sommer Motorset + 2 zenders", float(prijs_motor)))
        configuratiefiche["Motorisatie"] = "Sommer-motor meelopend systeem"
        
        nood_buiten = st.checkbox("Noodontkoppeling buiten met sleutel")
        if nood_buiten:
            prijs_details.append(("Noodontkoppeling buiten", float(prijs_nood_buiten)))
            configuratiefiche["Noodbediening"] = "Cilinder + sleutel buiten"

# ==========================================
# 5. OVERZICHT & OFFERTE GENERATIE
# ==========================================
with col_summary:
    st.subheader("📊 Offerte Overzicht")
    
    # Berekeningen
    subtotaal = sum(item[1] for item in prijs_details)
    btw_bedrag = subtotaal * (btw_percentage / 100)
    totaal_incl = subtotaal + btw_bedrag
    
    # Bepaal levertermijn
    if categorie == "Houten Poort":
        levertermijn = "10–15 weken (afhankelijk van houtlevering)"
    elif categorie == "Sectionaalpoort (Staal)" and configuratiefiche.get("Loopdeur") == "Ja":
        levertermijn = "± 10 weken"
    else:
        levertermijn = "6–8 weken"

    # Weergave kaart
    st.markdown(f"""
    <div class="card">
        <h4>Totaalprijs</h4>
        <p class="price-tag">€ {totaal_incl:,.2f} <span style="font-size:0.9rem; color:#6B7280;">(Incl. {btw_percentage}% BTW)</span></p>
        <p style="margin-bottom:0;">Excl. BTW: <b>€ {subtotaal:,.2f}</b></p>
        <p style="margin-bottom:0;">BTW Bedrag: <b>€ {btw_bedrag:,.2f}</b></p>
        <hr>
        <p>⏱️ <b>Verwachte levertermijn:</b><br>{levertermijn}</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("**Prijsopbouw:**")
    for omschrijving, bedrag in prijs_details:
        st.write(f"- {omschrijving}: **€ {bedrag:,.2f}**")

    st.divider()
    
    # Klantgegevens verzamelen voor PDF
    klant_data = {
        "naam": klant_naam,
        "adres": klant_adres,
        "email": klant_email,
        "tel": klant_tel,
        "project": project_type,
        "btw_tarief": btw_percentage
    }

    # PDF Genereren Knop
    if st.button("📄 Genereer Offerte (PDF)", use_container_width=True):
        try:
            pdf_bytes = genereer_pdf(
                klant=klant_data,
                configuratie=configuratiefiche,
                prijs_details=prijs_details,
                totaal_excl=subtotaal,
                btw_bedrag=btw_bedrag,
                totaal_incl=totaal_incl,
                levertermijn=levertermijn
            )
            
            st.success("✅ Offerte PDF succesvol aangemaakt!")
            
            # Downloadknop
            st.download_button(
                label="💾 Download Offerte PDF",
                data=pdf_bytes,
                file_name=f"Offerte_SiMa_{klant_naam.replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Er is een fout opgetreden bij het maken van de PDF: {e}")