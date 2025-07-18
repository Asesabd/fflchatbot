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
        "kiemelt": ["6", "6.", "kiemelt", "ünnepi", "nagy osztás", "következő nagy osztás", "extra ételosztás"],
        "adomany": ["7", "7.", "adomány", "segítenék", "adakozás"],
        "onkentes": ["8", "8.", "önkéntes", "önkéntesség"],
        "csomagkeres": ["küldjetek csomagot", "küldenétek csomagot", "kapok csomagot", "küldenek?", "küldenétek?", "kaphatok csomagot", "küldenétek nekem is"],
        "koszonet": ["köszi", "köszönöm", "szuperek vagytok", "hálás", "kössz", "kosz", "koszi", "kosi", "király", "szuper", "juhé", "nagyon jó"],
        "kilepes": ["kilépés", "exit", "quit"]
    }

    valaszok = {
        "udvozles": (
            "🙏 Üdvözöllek! Itt az Ételt az Életért chatbot. Miben segíthetek?\n"
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
            "📅 A kiemelt, vagy ünnepi ételosztások időpontjáról a weboldalunkon és a Facebook-oldalunkon tájékozódhatsz majd előre.\n"
            "👉 https://karitativ.hu"
        ),
        "adomany": (
            "🙏 Háromféleképp segíthetsz: élelmiszerrel, tárgyi adománnyal vagy pénzzel.\n"
            "👉 www.karitativ.hu"
        ),
        "onkentes": (
            "💪 Szeretnél önkéntes lenni? Szuper! Töltsd ki az űrlapot itt:\n"
            "👉 www.karitativ.hu/hogyan-segithetsz/"
        ),
        "csomagkeres": (
            "📦 Missziónk jelenleg az ételosztó pontokon való szolgáltatásra korlátozódik. "
            "Kapacitásunk sajnos nem teszi lehetővé, hogy élelmiszercsomagot küldjünk. "
            "Kérlek keresd fel a lakóhelyed szerinti családsegítőt, vagy nézd meg ezt az oldalt:\n"
            "👉 https://www.elelmiszerbank.hu/hu/tevekenysegunk/hova_kerulnek_a_megmentett_elelmiszerek.html"
        ),
        "koszonet": "😊 Örülök, ha segíthettem. Hálásak vagyunk minden jó szóért!",
        "kilepes": "exit"
    }

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

    visszakerdezes = (
        "\n\n❓ Sikerült választ kapnod?\n"
        "✉️ Ha nem, írj nekünk: info@karitativ.hu vagy hívj: +36 30 678 3217"
    )

    osszes_kulcsszo = [(tema, kulcsszo) for tema, kulcsok in temak.items() for kulcsszo in kulcsok]

    for tema, kulcsszo in osszes_kulcsszo:
        if kulcsszo in u or difflib.get_close_matches(u, [kulcsszo], n=1, cutoff=0.8):
            valasz = valaszok.get(tema)
            if valasz == "exit":
                return "👋 Köszönjük a megkeresést. Viszlát!"
            return valasz + visszakerdezes + menu

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

