from fuzzywuzzy import fuzz


def hasonlo(kifejezes, lehetosegek, kuszob=85):
    for kulcs in lehetosegek:
        if fuzz.partial_ratio(kifejezes, kulcs) >= kuszob:
            return True
    return False


def valaszolo_bot(kerdes):
    kerdes = kerdes.lower()

    if hasonlo(kerdes, [
        "küldenétek", "küldjetek", "küldjetek nekem", "ide is küldjetek",
        "miért nem küldtök", "nem kaptam", "hoznátok", "hozzatok", 
        "küldjetek csomagot", "küldenétek csomagot", "csomagot szeretnék"
    ]):
        return (
            "Missziónk jelenleg az ételosztó pontokon való szolgáltatásra korlátozódik. "
            "Nem tudunk csomagot küldeni vagy postázni. Tájékozódj itt: "
            "https://www.elelmiszerbank.hu/hu/tevekenysegunk/hova_kerulnek_a_megmentett_elelmiszerek.html"
        )

    elif hasonlo(kerdes, ["szia", "helló", "hello", "üdv", "jó napot", "jó reggelt"]):
        return "Szia! Örülök, hogy írtál! Miben segíthetek?"

    elif hasonlo(kerdes, ["hol van osztás", "hol lesz osztás", "hol lehet ételhez jutni"]):
        return (
            "Budapesten és 3 vidéki városban van rendszeres osztás: Egerben, Marcaliban hétköznapokon, "
            "Debrecenben vasárnaponként. Alkalmanként vidéki akciók is vannak. Részletek: www.eteltazeletert.hu"
        )

    elif hasonlo(kerdes, ["budapest", "hol budapest", "bp hol", "bp hol van", "budapesti osztás"]):
        return (
            "Budapesten 5 helyszínen van ételosztás minden hétköznap:\n"
            "• Népliget, Planetárium mögötti parkoló (12:00 – 13:00)\n"
            "• Óbudai Rehabilitációs Központ, Benedek Elek utca 1–3 (11:30 – 12:00)\n"
            "• Viziorgona utca 7., Óbuda (12:30 – 13:00)\n"
            "• Rózsa utca 3., VII. kerület (12:00 – 12:45)\n"
            "• Bosnyák utca 46., XIV. kerület (12:00 – 12:45)\n"
            "Részletek: https://karitativ.hu/kapcsolat/"
        )

    elif hasonlo(kerdes, ["eger", "egerben hol", "eger mikor", "hol van egerben osztás"]):
        return "Eger, Tűzoltó tér 5. – minden hétköznap 13:30 – 14:30 óra között."

    elif hasonlo(kerdes, ["marcali", "somogy", "somogyvámos", "marcali mikor", "somogyban hol"]):
        return (
            "Marcali, Piac tér – hétfőtől csütörtökig 12:00 – 12:25,\n"
            "péntekenként 13:00 – 13:25 között van osztás."
        )

    elif hasonlo(kerdes, ["debrecen", "debrecenben hol", "debrecen mikor", "hol van debrecenben osztás"]):
        return (
            "Debrecen, Magyari utca 2. (Govinda Étterem mellett) – vasárnaponként 12:00 – 13:00 óra között."
        )

    elif hasonlo(kerdes, ["hétvégén"]):
        return (
            "Hétvégén csak a budapesti ideiglenes szállókra szállítunk. Nyilvános ételosztásaink hétköznap zajlanak."
        )

    elif "mikor" in kerdes and "érkezzek" in kerdes:
        return "Érdemes a Népligethez kicsit 12:00 előtt érkezni, mert érkezési sorrendben szolgálunk ki."

    elif hasonlo(kerdes, ["mennyi ételt kapok", "mennyit kapok", "mennyi étel jár"]):
        return "Az ételmennyiséget az illetékes családsegítő intézmény állapítja meg."

    elif hasonlo(kerdes, ["regisztrálni szeretnék", "hogyan regisztrálhatok", "regisztráció"]):
        return "Igen, a kerületi családsegítőnél kell regisztrálni. Ők igazoló kártyát állítanak ki."

    elif hasonlo(kerdes, ["elviheti helyettem", "másnak is elvihető", "átveheti más"]):
        return (
            "Igen, ha valaki beteg vagy mozgásában korlátozott, hozzátartozója átveheti az ételt helyette."
        )

    elif hasonlo(kerdes, ["elvesztettem a kártyám"]):
        return "Új igazolást kell kérni a családsegítő intézményben."

    elif hasonlo(kerdes, ["hozhatok valamit", "segíthetek"]):
        return "Szívesen fogadunk eszközöket, például ételtartó dobozt, műanyag tányért. Köszönjük!"

    elif hasonlo(kerdes, ["telefon", "elérhetőség"]):
        return "Elérhetőségek: https://www.karitativ.hu/kapcsolat"

    elif hasonlo(kerdes, ["hány éves kortól", "ki jogosult"]):
        return "18 év felett jogosult ételt felvenni, előzetes regisztrációval."

    elif "iskola" in kerdes and "önkéntes" in kerdes:
        return "Igen, várjuk az iskolák önkéntes csatlakozását is! Részletek: www.karitativ.hu/hogyan-segithetsz/"

    elif hasonlo(kerdes, ["házi süti", "sütemény"]):
        return "Kérlek előzetesen vedd fel velünk a kapcsolatot. Kizárólag ellenőrzött élelmiszert osztunk."

    elif hasonlo(kerdes, ["raktár", "hová vihetem"]):
        return (
            "Kérjük egyeztess velünk előre! Budapesten a Lehel utca 15. alatt található raktárunk. "
            "Az üzemi működés miatt előzetes megbeszélés szükséges."
        )

    elif hasonlo(kerdes, ["autós segítség", "fuvar"]):
        return "Nagyon köszönjük, de jelenleg el vagyunk látva szállító autókkal."

    elif hasonlo(kerdes, ["ünnep", "karácsony"]):
        return (
            "Igen, rendszeresen szervezünk kiemelt ünnepi ételosztásokat. Kövesd híreinket és értesítünk!"
        )

    elif hasonlo(kerdes, ["csomagban"]):
        return (
            "A csomag 10–12 féle tartós élelmiszert tartalmaz, pl. étolaj, liszt, cukor, savanyúság, csoki, dió."
        )

    elif hasonlo(kerdes, ["meleg étel"]):
        return (
            "Csak vegetáriánus meleg ételt osztunk. Pl. főzelék, tészták, levesek. Ételallergiával kapcsolatban "
            "az osztóknál lehet érdeklődni."
        )

    elif hasonlo(kerdes, ["önkéntes munka", "önkéntes lehetek", "segítenék"]):
        return "Bővebben itt olvashatsz: www.karitativ.hu/hogyansegithetek"

    elif hasonlo(kerdes, ["adomány", "milyen adomány"]):
        return (
            "Háromféleképp tudsz segíteni: élelmiszerrel, tárgyi adománnyal és pénzzel. Köszönjük!"
        )

    elif hasonlo(kerdes, ["pénzt", "pénzadomány"]):
        return (
            "Pénzadományból tartjuk fenn magunkat. Különböző csomagok közül választhatsz a támogatás mértékéhez igazodva."
        )

    elif hasonlo(kerdes, ["szuperek vagytok", "köszi", "köszönöm"]):
        return "Köszönjük a kedvességed, igazán jól esik! :)"

    elif hasonlo(kerdes, ["jöttök", "nem jöttök", "kellene"]):
        return (
            "Jelenleg a Mint egy falat kenyér programunk keretében foglalkozunk különleges vidéki étel- és csomagosztásokkal. "
            "Ezeket előzetesen egyeztetjük az érintett önkormányzatokkal. Minden megkeresést szívesen fogadunk, "
            "de kapacitásunk korlátozott, így egyszerre csak egy helyszínt tudunk kiszolgálni."
        )

    elif hasonlo(kerdes, ["meleg ételhez jutni", "szeretnék enni", "meleg ételt szeretnék", "hol lehet kaját kapni"]):
        return (
            "Meleg ételhez osztópontjainkon lehet hozzájutni, jellemzően hétköznapokon. "
            "A lakóhelyedhez legközelebbi helyszínt érdemes felkeresni:\n\n"
            "Budapest – Népliget, hétfőtől péntekig 12:00-tól (érdemes korábban érkezni)\n"
            "Eger – rendszeres hétköznapi osztás\n"
            "Debrecen – vasárnapi osztás\n"
            "Somogyvámos – hétköznapi osztás\n"
            "Szolnok, Szeged, Békéscsaba – alkalmi, előre bejelentett osztások\n\n"
            "A részletes címeket és időpontokat megtalálod a karitativ.hu/kapcsolat oldalon."
        )

    else:
        return (
            "Ezt még nem tudom biztosan. Írhatsz nekünk az info@karitativ.hu címre, vagy nézd meg a karitativ.hu oldalt!"
        )


if __name__ == "__main__":
    print("Szia! Ételt az Életért chatbot vagyok. Miben segíthetek?")
    while True:
        beker = input("Te: ")
        if beker.lower() in ["kilép", "exit", "bye"]:
            print("Viszlát! 🌱")
            break
        valasz = valaszolo_bot(beker)
        print("Bot:", valasz)
