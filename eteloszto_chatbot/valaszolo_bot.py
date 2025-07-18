import difflib

def valaszolo_bot(uzenet):
    u = uzenet.lower().strip()

    temak = {
        "udvozles": ["szia", "hello", "üdv", "jó napot", "jó reggelt"],
        "etelosztas": ["1", "1.", "ételosztás", "osztás", "hol van osztás"],
        "regisztracio": ["2", "2.", "regisztráció", "regisztrálni", "csatlakozás"],
        "atvetel": ["3", "3.", "átvétel", "másnak is elvihető", "elviheti"],
        "budapest": ["4", "4.", "budapest", "bp"],
        "videk": ["5", "5.", "eger", "marcali", "debrecen", "vidék"],
        "kiemelt": ["kiemelt", "ünnepi", "következő nagy osztás", "nagy osztás", "legközelebb mikor", "extra ételosztás"],
        "adomany": ["7", "7.", "adomány", "segítenék", "adakozás"],
        "onkentes": ["8", "8.", "önkéntes", "önkéntesség"],
        "koszonet": ["köszi", "köszönöm", "szuperek vagytok", "hálás", "kössz", "kosz", "koszi", "kosi", "király", "szuper", "juhé", "nagyon jó"],
        "kilepes": ["kilépés", "exit", "quit"]
    }

    valaszok = {
        "udvozles": (
            "🙏 Üdvözöllek! Itt az Ételt az Életért chatbot. Miben segíthetek?\n\n"
        ),
        "etelosztas": (
            "🍲 Ételt hétköznapokon osztunk Budapesten, Egerben, Marcaliban és környékén. Debrecenben vasárnap van osztás.\n"
            "📍 Pontos helyszínekhez válaszd a 4-es vagy az 5-ös gombot."
        ),
        "regisztracio": (
            "📝 Az ételosztáshoz regisztráció szükséges, melyet a lakóhely szerinti családsegítő központban lehet kérni."
        ),
        "atvetel": (
            "✅ Igen, előzetes egyeztetéssel más is átveheti a csomagot. Érdemes a helyi kapcsolattartóval vagy segítővel előre egyeztetni."
        ),
        "budapest": (
            "🏙️ Budapesti osztópontok hétköznapokon:\n"
            "• Népliget (12:00)\n"
            "• Óbuda, Benedek Elek utca\n"
            "• Viziorgona utca 7.\n"
            "• Rózsa utca 3.\n"
            "• Bosnyák utca 46.\n"
            "👉 Részletek: https://karitativ.hu/kapcsolat/"
        ),
        "videk": (
            "🏡 Vidéki osztások:\n"
            "• Eger – hétköznap 13:30–14:30\n"
            "• Marcali – hétfőtől csütörtökig 12:00–12:25, péntek 13:00–13:25\n"
            "• Debrecen – vasárnap 12:00–13:00"
        ),
        "kiemelt": (
            "📅 A kiemelt, ünnepi ételosztások időpontjáról a weboldalunkon és a Facebook-oldalunkon tájékozódhatsz majd előre.\n"
            "👉 https://karitativ.hu vagy Facebook: Ételt az Életért Alapítvány"
        ),
        "adomany": (
            "🙏 Háromféleképp segíthetsz: élelmiszerrel, tárgyi adománnyal vagy pénzzel.\n"
            "👉 www.karitativ.hu"
        ),
        "onkentes": (
            "💪 Szeretnél önkéntes lenni? Szuper! Töltsd ki az űrlapot itt:\n"
            "👉 www.karitativ.hu/hogyan-segithetsz/"
        ),
        "koszonet": "😊 Örülök, ha segíthettem. Hálásak vagyunk minden jó szóért!",
        "kilepes": "exit"
    }

    # Beágyazott menü sablon minden válasz végére (kivéve kilépésnél)
    menu = (
        "\n\n📋 Válassz egy témát szám szerint:\n"
        "1️⃣ Ételosztás időpontok és helyszínek\n"
        "2️⃣ Regisztrációs tudnivalók\n"
        "3️⃣ Átveheti-e más a csomagot?\n"
        "4️⃣ Budapesti osztópontok\n"
        "5️⃣ Vidéki osztások\n"
        "6️⃣ Kiemelt ételosztás\n"
        "7️⃣ Adományozás lehetőségei\n"
        "8️⃣ Önkéntes munka"
    )

    # Előfeldolgozás: összes kulcsszó egy listába
    osszes_kulcsszo = [(tema, kulcsszo) for tema, kulcsok in temak.items() for kulcsszo in kulcsok]

    for tema, kulcsszo in osszes_kulcsszo:
        if kulcsszo in u or difflib.get_close_matches(u, [kulcsszo], n=1, cutoff=0.8):
            valasz = valaszok.get(tema)
            if valasz == "exit":
                return "👋 Köszönjük a megkeresést. Viszlát!"
            return valasz + menu

    return (
        "❓ Ezt most nem értettem teljesen.\n"
        "📋 Írd be a számot, ami érdekel:\n"
        "1 – Ételosztás\n"
        "2 – Regisztráció\n"
        "3 – Átveheti más?\n"
        "4 – Budapesti pontok\n"
        "5 – Vidéki helyszínek\n"
        "6 – Kiemelt ételosztás\n"
        "7 – Adományozás\n"
        "8 – Önkéntes segítség"
    )

