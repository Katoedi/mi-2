import csv
from collections import Counter

#cuvintele din fisierul mare
def incarca_dictionar():
    # din src/hangman.py urc un nivel (..) si intru in folderul data
    with open("../data/big_romanian_list.txt", encoding="utf-8") as fisier:
        cuvinte = []
        for linie in fisier:
            cuvant = linie.strip().lower()
            if cuvant != "":
                cuvinte.append(cuvant)
    return cuvinte

# lista de cuvinte
dictionar = incarca_dictionar()
print("Am încărcat", len(dictionar), "cuvinte.")
print("Primele 10 cuvinte sunt:", dictionar[:10])

# verific daca cuv se potrivesc cu mdoelul
def asemanare_cuvinte(cuvant, model):
    if len(cuvant) != len(model):
        return False
    for litera_cuvant, litera_model in zip(cuvant, model):
        if litera_model != "*" and litera_cuvant != litera_model:
            return False
    return True

def filtreaza_cuvinte(dictionar, model, litere_incluse=None, litere_excluse=None):
    if litere_incluse is None:
        litere_incluse = set()
    if litere_excluse is None:
        litere_excluse = set()

    rezultat = []

    for cuvant in dictionar:
        # 1. se potrivește cu modelul (cu *)
        if not asemanare_cuvinte(cuvant, model):
            continue

        # 2. nu conține litere excluse
        if any(litera_exclusa in cuvant for litera_exclusa in litere_excluse):
            continue

        # 3. conține toate literele obligatorii
        if not all(litera_obligatorie in cuvant for litera_obligatorie in litere_incluse):
            continue

        rezultat.append(cuvant)

    return rezultat

# actualizez modelul dupa ce am ghicit o litera buna
def actualizeaza_model(model_curent, cuvant_tinta, litera_ghicita):
    model_nou = []
    for litera_cuvant_tinta, litera_model in zip(cuvant_tinta, model_curent):
        if litera_cuvant_tinta == litera_ghicita:
            model_nou.append(litera_ghicita)
        else:
            model_nou.append(litera_model)
    return "".join(model_nou)

# rezolv un singur joc de spanzuratoarea
def rezolva_un_joc(game_id, model_initial, cuvant_tinta, dictionar):
    model_curent = model_initial.lower()
    cuvant_tinta = cuvant_tinta.lower()

    litere_bune = set(litera for litera in model_curent if litera != "*")
    litere_rele = set()
    litere_incercate = []

    while "*" in model_curent:
        # caut cuvintele posibile pentru modelul curent
        lista_cuvinte_posibile = filtreaza_cuvinte(
            dictionar, model_curent, litere_bune, litere_rele
        )

        if not lista_cuvinte_posibile:
            break

        # numar frecventa literelor care nu au fost incercate
        frecvente_litere = Counter()
        for cuvant_posibil in lista_cuvinte_posibile:
            for index_pozitie, litera_cuvant in enumerate(cuvant_posibil):
                if (
                    model_curent[index_pozitie] == "*"
                    and litera_cuvant not in litere_bune
                    and litera_cuvant not in litere_rele
                ):
                    frecvente_litere[litera_cuvant] += 1

        if not frecvente_litere:
            break

        # aleg litera cea mai frecventa
        litera_aleasa = frecvente_litere.most_common(1)[0][0]
        litere_incercate.append(litera_aleasa)

        # vad daca litera chiar este in cuvantul tinta
        if litera_aleasa in cuvant_tinta:
            litere_bune.add(litera_aleasa)
            model_curent = actualizeaza_model(
                model_curent, cuvant_tinta, litera_aleasa
            )
        else:
            litere_rele.add(litera_aleasa)

    status = "OK" if model_curent == cuvant_tinta else "FAIL"

    rezultat_un_joc = {
        "game_id": game_id,
        "total_incercari": len(litere_incercate),
        "cuvant_gasit": model_curent,
        "status": status,
        "secventa_incercari": " ".join(litere_incercate),
    }
    return rezultat_un_joc

# citesc fisierul cu jocuri de forma: id;model;cuvant_tinta
def citeste_jocuri(nume_fisier):
    jocuri = []
    with open(nume_fisier, encoding="utf-8") as fisier_jocuri:
        reader = csv.reader(fisier_jocuri, delimiter=";")
        for linie in reader:
            if len(linie) < 3:
                continue
            identificator_joc = linie[0].strip()
            model = linie[1].strip()
            cuvant_tinta = linie[2].strip()
            jocuri.append((identificator_joc, model, cuvant_tinta))
    return jocuri

def main():
    print("Am intrat in main().")

    # din src/hangman.py urc un nivel (..) si intru in data
    jocuri = citeste_jocuri("../data/cuvinte_de_verificat (1).txt")

    print("Am citit", len(jocuri), "jocuri din fisierul cuvinte_de_verificat (1).txt.")

    # extind dictionarul cu toate cuvintele tinta, ca sa fiu sigur ca sunt candidate
    multime_cuvinte = set(dictionar)
    for identificator_joc, model_initial, cuvant_tinta in jocuri:
        multime_cuvinte.add(cuvant_tinta.lower())
    dictionar_extins = list(multime_cuvinte)

    rezultate = []
    total_incercari_toate_jocurile = 0  # din cate incercari a gasit toate cuvintele

    numar_total_jocuri = len(jocuri)

    for index_joc, (identificator_joc, model_initial, cuvant_tinta) in enumerate(
        jocuri, start=1
    ):
        print(
            f"Rezolv jocul {index_joc}/{numar_total_jocuri} cu id={identificator_joc}, model='{model_initial}', cuvant_tinta='{cuvant_tinta}'"
        )

        rezultat_un_joc = rezolva_un_joc(
            identificator_joc, model_initial, cuvant_tinta, dictionar_extins
        )
        rezultate.append(rezultat_un_joc)
        total_incercari_toate_jocurile += rezultat_un_joc["total_incercari"]

        print(
            f"  -> status={rezultat_un_joc['status']}, gasit='{rezultat_un_joc['cuvant_gasit']}', incercari={rezultat_un_joc['total_incercari']}"
        )

    # scriu rezultatele in csv (in folderul results, un nivel mai sus)
    with open(
        "../results/rezultate.csv", "w", newline="", encoding="utf-8"
    ) as fisier_rezultate:
        campuri = [
            "game_id",
            "total_incercari",
            "cuvant_gasit",
            "status",
            "secventa_incercari",
        ]
        writer = csv.DictWriter(fisier_rezultate, fieldnames=campuri)
        writer.writeheader()
        writer.writerows(rezultate)

    print("Rezultatele au fost salvate in fisierul results/rezultate.csv")
    print("Total incercari pentru toate cuvintele:", total_incercari_toate_jocurile)
    print("Numarul de cuvinte rezolvate:", numar_total_jocuri)
    if numar_total_jocuri > 0:
        print(
            "Media de incercari pe cuvant:",
            total_incercari_toate_jocurile / numar_total_jocuri,
        )


if __name__ == "__main__":
    main()

