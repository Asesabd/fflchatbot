import difflib

# =========================
# FIX LINKEK
# =========================
ADOMANY_URL = "https://segitsteis.hu"
RECEPT_URL = "https://eteltazeletert.hu/wp-content/uploads/2025/10/Jotekony_izek.pdf"

# =========================
# RÁSZORULÓI INFORMÁCIÓ
# =========================
RASZORULO_FOINFO = (
    "💚 Fontos információ rászorulóknak:\n\n"
    "🎄 Budapesti Karácsonyi Nagy Szeretetlakoma\n"
    "🗓️ December 24–25–26.\n\n"
    "📍 Helyszín: Népliget\n"
    "(Rapaics Raymund sétány és a Hell Miksa sétány találkozásánál)\n\n"
    "🎟️ Karszalagosztás: 8:00–11:00\n"
    "🍲 Meleg étel osztása: 11:00-tól\n\n"
    "🍲 Meleg ételt MINDENKI kap.\n"
    "🎁 Tartós élelmiszercsomagot 18 év felett tudunk adni.\n\n"
    "Az esemény minden rászoruló számára nyitva áll.\n\n"
    "🙏 Kérjük, akinek fontos lehet, ossza meg ezt az információt.\n"
    f"💚 Ha szeretnél segíteni: 👉 {ADOMANY_URL}\n\n"
    "3️⃣ Főmenü"
)

def fo_menu():
    return (
        "🔁 Főmenü\n\n"
        "1️⃣ Rászoruló vagyok\n"
        "2️⃣ Támogató vagyok\n"
        "3️⃣ Főmenü"
    )

# =========================
# SEGÉDFÜGGVÉNYEK
# =========================
def _match(u: str, keywords: list[str], cutoff: float = 0.84) -> bool:
    for k in keywords:
        if k in u:
            return True
        if difflib.get_close_matches(u, [k], n=1, cutoff=cutoff):
            return True
    return False

def _ensure_state(allapot: dict):
    allapot.setdefault("ag", None)                   # None / raszorulo / tamogato
    allapot.setdefault("var_recept_valaszt", False)  # várjuk-e a recept igen/nem választ
    allapot.setdefault("recept_elkuldve", False)

def _recept_azonnal():
    return (
        "🎁 Ajándék receptkönyv – *Jótékony ízek*\n\n"
        f"👉 {RECEPT_URL}\n\n"
        "💚 Köszönjük, hogy segítesz másokon is.\n"
        f"Ha szeretnél támogatni: 👉 {ADOMANY_URL}\n\n"
        "3️⃣ Főmenü"
    )

# =========================
# FŐ BOT LOGIKA
# =========================
def valaszolo_bot(uzenet: str, allapot={"ag": None}):
    _ensure_state(allapot)
    u = (uzenet or "").lower().strip()

    # 3️⃣ FŐMENÜ – BÁRHONNAN
    if u in ["3", "főmenü", "fomenü", "menu", "menü", "vissza", "back", "/start", "start"]:
        allapot["ag"] = None
        allapot["var_recept_valaszt"] = False
        return fo_menu()

    # RECEPT VÁLASZTÁS – támogató ágon
    if allapot["ag"] == "tamogato" and allapot["var_recept_valaszt"]:
        if _match(u, ["igen", "kérem", "kerem", "1", "ok", "jöhet", "johet", "küldd", "kuldd"]):
            allapot["var_recept_valaszt"] = False
            allapot["recept_elkuldve"] = True
            return _recept_azonnal()

        if _match(u, ["nem", "2", "köszönöm", "koszonom", "kihagyom"]):
            allapot["var_recept_valaszt"] = False
            return (
                "Rendben. 💚\n\n"
                f"🙏 Ha szeretnél segíteni: 👉 {ADOMANY_URL}\n\n"
                "3️⃣ Főmenü"
            )

        return (
            "🎁 Szeretnél egy ajándék receptkönyvet?\n"
            "1️⃣ Igen, kérem\n"
            "2️⃣ Nem kérem\n\n"
            "3️⃣ Főmenü"
        )

    # INDULÁS – ÁG VÁLASZTÁS
    if allapot["ag"] is None:
        if _match(u, ["1", "rászoruló", "raszorulo", "étel", "etel", "osztás", "osztas", "népliget", "nepliget"]):
            allapot["ag"] = "raszorulo"
            return RASZORULO_FOINFO

        if _match(u, ["2", "támogató", "tamogato", "adomány", "adomany", "segítenék", "segitenek"]):
            allapot["ag"] = "tamogato"
            allapot["var_recept_valaszt"] = True
            return (
                "🤝 Köszönjük, hogy segítesz! 💚\n\n"
                "🎁 Szeretnél egy ajándék receptkönyvet?\n"
                "1️⃣ Igen, kérem\n"
                "2️⃣ Nem kérem\n\n"
                "3️⃣ Főmenü"
            )

        return fo_menu()

    # RÁSZORULÓ ÁG
    if allapot["ag"] == "raszorulo":
        if _match(u, ["adomány", "adomany", "segítenék", "segitenek"]):
            allapot["ag"] = "tamogato"
            allapot["var_recept_valaszt"] = True
            return (
                "💚 Köszönjük!\n\n"
                "🎁 Szeretnél egy ajándék receptkönyvet?\n"
                "1️⃣ Igen, kérem\n"
                "2️⃣ Nem kérem\n\n"
                "3️⃣ Főmenü"
            )

        return RASZORULO_FOINFO

    # TÁMOGATÓ ÁG – default
    if allapot["ag"] == "tamogato":
        if _match(u, ["recept", "receptkönyv", "receptkonyv", "pdf"]):
            return _recept_azonnal()

        return (
            "🙏 Köszönjük, hogy segítesz! 💚\n\n"
            f"👉 Adományozás: {ADOMANY_URL}\n\n"
            "🎁 Ha kérsz ajándék receptkönyvet, írd: „recept”.\n"
            "3️⃣ Főmenü"
        )

    allapot["ag"] = None
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
