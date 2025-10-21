# -*- coding: utf-8 -*-
import csv

input_csv = "src/Products.urban/src/Products/urban/profiles/preinstall/workflows/codt_buildlicence_workflow/workflows.csv"
output_puml = "workflow1_usecase.puml"

actors = set()
usecases = []

with open(input_csv, "rb") as f:  # Python 2, binaire
    reader = csv.DictReader(f)
    for row in reader:
        uc = row["Permission"].strip()
        roles = [r.strip() for r in row["Roles"].split(",") if r.strip()]
        usecases.append((uc, roles))
        for r in roles:
            actors.add(r)

with open(output_puml, "wb") as f:
    f.write("@startuml\n")
    # Déclaration des acteurs
    for actor in actors:
        f.write(u"actor {}\n".format(actor).encode('utf-8'))
    # Déclaration des use cases et liens
    for i, (uc, roles) in enumerate(usecases, 1):
        f.write(u'usecase "{}" as UC{}\n'.format(uc, i).encode('utf-8'))
        for r in roles:
            f.write(u"{} --> UC{}\n".format(r, i).encode('utf-8'))
    f.write("@enduml\n")

print("✅ Fichier PlantUML généré :", output_puml)
