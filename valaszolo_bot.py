import difflib

# =========================
# FIX LINKEK
# =========================
ADOMANY_URL = "https://segitsteis.hu"
RECEPT_URL = "https://eteltazeletert.hu/wp-content/uploads/2025/10/Jotekony_izek.pdf"
ONKENTES_URL = "https://karitativ.hu/szeretnek-onkentes-lenni/"
HIRLEVEL_URL = "https://karitativ.hu/hirlevel/"
FALAT_URL = "https://www.eteltazeletert.hu"

# =========================
# SZÖVEGEK
# =========================
BEVEZETO_SZOVEG = (
    "🙏 Hare Krisna! Az Ételt az Életért *menürendszer chatbotja* vagyok.\n\n"
    "📋 Segítek eligazodni az ételosztás, segítségnyújtás és önkéntesség világában.\n"
    "💬 Csevegni nem tudsz velem. Ha személyes kérdésed van, írj: info@karitativ.hu\n\n"
    "👇 Válassz:\n"
    "1️⃣ Rászoruló vagyok\n"
    "2️⃣ Érdeklődöm / segíteni szeretnék\n"
    "3️⃣ Főmenü"
)

FO_MENU_RASZORULO = (
    "🌍 Kérlek, válaszd ki a várost:\n"
    "1️⃣ Budapest\n"
    "2️⃣ Eger\n"
    "3️⃣ Somogy vármegye\n"
    "4️⃣ Debrecen\n"
    "5️⃣ Szeged\n\n"
    "3️⃣ Főmenü"
)


VAROS_INFOK = {
    "budapest": (
        "🍲 *Budapest*\n"
        "📍 Ételosztás minden hétköznap:\n"
        "• Népliget – Planetárium mögött (12:00–13:00)\n"
        "• Benedek Elek u. 1–3 (11:30–12:00)\n"
        "• Viziorgona u. 7 mögött (12:30–13:00)\n"
        "• Rózsa u. 3. (12:00–12:45)\n"
        "• Bosnyák u. 46. (12:00–12:45)\n"
        "📞 Kapcsolat: Nagy Gergely – +36 30 678 3217"
    ),
    "eger": (
        "🍲 *Eger és környéke*\n"
        "• Tűzoltó tér 5. (14:00–15:00)\n"
        "• Árnyékszala út 42. (13:00–13:30)\n"
        "• Felnémet, Mezőkövesd, Családok Otthona – kiszállítás\n"
        "📞 Nyolcas Olivér – +36 30 779 4449"
    ),
    "somogy": (
        "🍲 *Somogy vármegye*\n"
        "• Marcali Piac tér (H–Cs 12:00–12:25, P: 13:00–13:25)\n"
        "• Horvátkút, Kéthely – kiszállítás\n"
        "📞 Nagy Gergely – +36 30 678 3217"
    ),
    "debrecen": (
        "🍲 *Debrecen*\n"
        "• Magyari u. 2. – Govinda mellett (vasárnap 12:00–13:00)\n"
        "📞 Faludi Kata – +36 70 416 5651"
    ),
    "szeged": (
        "🍲 *Szeged*\n"
        "– Időszakos városi osztás – 150–200 adag\n"
        "• Zarda u. 11.\n"
        "📞 Hatvany Viktória – +36 70 147 4115"
    )
}

def _match(u: str, keywords: list[str], cutoff: float = 0.84) -> bool:
    for k in keywords:
        if k in u:
            return True
        if difflib.get_close_matches(u, [k], n=1, cutoff=cutoff):
            return True
    return False

def _ensure_state(allapot: dict):
    allapot.setdefault("ag", None)
    allapot.setdefault("var_recept_valaszt", False)
    allapot.setdefault("recept_elkuldve", False)
    allapot.setdefault("varos_valasztas", False)

def fo_menu():
    return BEVEZETO_SZOVEG

def _recept_azonnal():
    return (
        "🎁 *Ajándék receptgyűjtemény – Jótékony ízek*\n\n"
        f"📩 A receptkönyv letöltéséhez iratkozz fel a hírlevelünkre:\n👉 {HIRLEVEL_URL}\n\n"
        f"🎉 A feliratkozás után letöltheted innen: {RECEPT_URL}\n\n"
        f"ℹ️ További információk: {FALAT_URL}\n"
        f"🤝 Ha önkéntesként segítenél: {ONKENTES_URL}\n\n"
        "3️⃣ Főmenü"
    )

def valaszolo_bot(uzenet: str, allapot={"ag": None}):
    _ensure_state(allapot)
    u = (uzenet or "").lower().strip()

    # Főmenü
    if u in ["3", "főmenü", "menu", "menü", "vissza", "back", "/start", "start"]:
        allapot.update({"ag": None, "var_recept_valaszt": False, "varos_valasztas": False})
        return fo_menu()

    # Receptválasz érdeklődő ágon
    if allapot["ag"] == "erdeklodo" and allapot["var_recept_valaszt"]:
        if _match(u, ["igen", "kérem", "kerem", "1", "ok", "jöhet", "küldd"]):
            allapot["var_recept_valaszt"] = False
            allapot["recept_elkuldve"] = True
            return _recept_azonnal()
        if _match(u, ["nem", "2", "köszönöm", "kihagyom"]):
            allapot["var_recept_valaszt"] = False
            return (
                "Rendben. 💚\n\n"
                f"👉 Adományozás: {ADOMANY_URL}\n"
                f"🤝 Önkéntes jelentkezés: {ONKENTES_URL}\n"
                f"ℹ️ Programunk: {FALAT_URL}\n\n"
                "3️⃣ Főmenü"
            )
        return (
            "🎁 Szeretnél egy ajándék receptgyűjteményt?\n"
            "1️⃣ Igen, kérem\n"
            "2️⃣ Nem kérem\n\n"
            f"📩 Feliratkozás: {HIRLEVEL_URL}\n"
            "3️⃣ Főmenü"
        )

    # Ágválasztás
    if allapot["ag"] is None:
        if _match(u, ["1", "rászoruló", "étel", "osztás", "népliget"]):
            allapot["ag"] = "raszorulo"
            allapot["varos_valasztas"] = True
            return FO_MENU_RASZORULO
        if _match(u, ["2", "érdeklődő", "támogató", "adomány", "önkéntes", "segítenék"]):
            allapot["ag"] = "erdeklodo"
            allapot["var_recept_valaszt"] = True
            return (
                "💚 Köszönjük, hogy érdeklődsz az Ételt az Életért iránt!\n\n"
                "🎁 Szeretnél egy ajándék receptgyűjteményt?\n"
                "1️⃣ Igen, kérem\n"
                "2️⃣ Nem kérem\n\n"
                f"👐 Önkéntes jelentkezés: {ONKENTES_URL}\n"
                f"ℹ️ Program: {FALAT_URL}\n\n"
                "3️⃣ Főmenü"
            )
        return fo_menu()

    # Rászorulói ág – városválasztás
    if allapot["ag"] == "raszorulo":
        if allapot["varos_valasztas"]:
            if _match(u, ["1", "budapest"]):
                return VAROS_INFOK["budapest"] + "\n\n3️⃣ Főmenü"
            if _match(u, ["2", "eger"]):
                return VAROS_INFOK["eger"] + "\n\n3️⃣ Főmenü"
            if _match(u, ["3", "somogy", "somogy vármegye", "somogyvarmegye", "marcali"]):
                return VAROS_INFOK["somogy"] + "\n\n3️⃣ Főmenü"
            if _match(u, ["4", "debrecen"]):
                return VAROS_INFOK["debrecen"] + "\n\n3️⃣ Főmenü"
            if _match(u, ["5", "szeged"]):
                return VAROS_INFOK["szeged"] + "\n\n3️⃣ Főmenü"
            return FO_MENU_RASZORULO
        else:
            allapot["varos_valasztas"] = True
            return FO_MENU_RASZORULO

    # Érdeklődő ág default
    if allapot["ag"] == "erdeklodo":
        if _match(u, ["recept", "pdf", "receptkönyv"]):
            return _recept_azonnal()
        return (
            "💚 Köszönjük, hogy érdeklődsz!\n\n"
            f"👉 Adományozás: {ADOMANY_URL}\n"
            f"🤝 Önkéntes jelentkezés: {ONKENTES_URL}\n"
            f"ℹ️ Program: {FALAT_URL}\n"
            "🎁 Ha kérsz receptgyűjteményt, írd be: „recept”\n"
            "3️⃣ Főmenü"
        )

    return fo_menu()


# =========================
# KONZOLOS TESZT
# =========================
if __name__ == "__main__":
    print("Szia! Ételt az Életért chatbot vagyok. 💚")
    allapot = {"ag": None}
    while True:
        beker = input("Te: ").strip()
        if beker.lower() in ["kilép", "kilep", "exit", "bye"]:
            print("Bot: Viszlát! 🌱")
            break
        print("Bot:", valaszolo_bot(beker, allapot))