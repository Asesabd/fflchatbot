import difflib

# Ideiglenes "adatbázis": felhasználó állapotok (raszorulo vagy tamogato)
felhasznalo_allapot = {}

def valaszolo_bot(uzenet, user_id="default"):
    u = uzenet.lower().strip()

    if user_id not in felhasznalo_allapot:
        if any(k in u for k in ["rászoruló", "ételt kérek", "segítség kell"]):
            felhasznalo_allapot[user_id] = "raszorulo"
            return "✅ Rögzítettem, hogy rászorulóként érdeklődsz. Írd be a számot, ami érdekel:\n" + menu_raszorulo
        elif any(k in u for k in ["segíteni", "támogatni", "adományozni"]):
            felhasznalo_allapot[user_id] = "tamogato"
            return "🙏 Köszönjük, hogy segítenél! Írd be a számot, ami érdekel:\n" + menu_tamogato
        else:
            return ("🙏 Köszönjük, hogy írtál!\n"
                    "Kérlek válaszd ki, hogy miben segíthetünk:\n"
                    "1️⃣ Rászoruló vagyok\n"
                    "2️⃣ Segíteni szeretnék")

    allapot = felhasznalo_allapot[user_id]

    if allapot == "raszorulo":
        return valasz_raszoruloknak(u)
    elif allapot == "tamogato":
        return valasz_tamogatoknak(u)

    return "🤖 Hiba történt. Kérlek indítsd újra a beszélgetést."

def valasz_raszoruloknak(u):
    temak = {
        "etelosztas": ["1", "ételosztás", "osztás", "hol van osztás"],
        "regisztracio": ["2", "regisztráció"],
        "atvetel": ["3", "átvétel"],
        "helyszin": ["4", "budapest", "eger", "marcali", "debrecen", "vidék"],
        "csomagkeres": ["5", "küldjetek csomagot", "elviheti"],
    }
    valaszok = {
        "etelosztas": "🍲 Ételt osztunk hétköznapokon... (részletes válasz)",
        "regisztracio": "📝 Regisztráció a családsegítőnél történik.",
        "atvetel": "✅ Más is átveheti egyeztetéssel.",
        "helyszin": "📍 Budapest, Eger, Marcali, Debrecen... (részletek)",
        "csomagkeres": "📦 Sajnos nem tudunk csomagot küldeni."
    }
    return kulcsszo_alapu_valasz(u, temak, valaszok, menu_raszorulo)

def valasz_tamogatoknak(u):
    temak = {
        "adomany": ["1", "adomány", "pénz", "támogatás"],
        "etelfelajanlas": ["2", "élelmiszer", "étel adomány"],
        "onkentes": ["3", "önkéntes"]
    }
    valaszok = {
        "adomany": "💸 Köszönjük! Támogatás: www.karitativ.hu",
        "etelfelajanlas": "🎁 Írj nekünk: info@karitativ.hu az adományról!",
        "onkentes": "💪 Önkéntes űrlap: karitativ.hu/hogyan-segithetsz"
    }
    return kulcsszo_alapu_valasz(u, temak, valaszok, menu_tamogato)

def kulcsszo_alapu_valasz(u, temak, valaszok, menu):
    for tema, kulcsok in temak.items():
        for kulcs in kulcsok:
            if kulcs in u or difflib.get_close_matches(u, [kulcs], n=1, cutoff=0.8):
                return valaszok[tema] + "\n\n" + menu
    return "❓ Ezt nem értettem. Kérlek válassz számot.\n" + menu

menu_raszorulo = (
    "\n📋 Rászorulóknak választható menüpontok:\n"
    "1️⃣ Ételosztás\n"
    "2️⃣ Regisztráció\n"
    "3️⃣ Átveheti más?\n"
    "4️⃣ Osztópontok\n"
    "5️⃣ Csomagküldés"
)

menu_tamogato = (
    "\n📋 Segítőknek választható menüpontok:\n"
    "1️⃣ Pénzbeli támogatás\n"
    "2️⃣ Tárgyi/étel adomány\n"
    "3️⃣ Önkéntesség"
)

# --- Lokális teszt
if __name__ == "__main__":
    print("Szia! Ételt az Életért chatbot vagyok. Írj valamit!")
    while True:
        beker = input("Te: ")
        if beker.lower() in ["kilép", "exit", "bye"]:
            print("Viszlát! 🌱")
            break
        valasz = valaszolo_bot(beker, user_id="teszt")
        print("Bot:", valasz)

