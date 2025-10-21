# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

# Fichier d'entrée et sortie
INPUT = "src/Products.urban/src/Products/urban/profiles/default/actions.xml"
OUTPUT = "actions_usecases.puml"

def parse_actions(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    usecases = []  # [(title, [roles], available_expr)]
    for obj in root.findall(".//object[@meta_type='CMF Action']"):
        title = obj.findtext("property[@name='title']")
        if not title:
            title = obj.get("name")

       
        roles = []
        perms = obj.find("property[@name='permissions']")
        if perms is not None:
            for el in perms.findall("element"):
                roles.append(el.get("value"))

      
        available_expr = obj.findtext("property[@name='available_expr']")

        usecases.append((title, roles, available_expr))

    return usecases


def generate_puml(usecases, outfile):
    with open(outfile, "w") as f:
        f.write("@startuml\n")
        f.write("left to right direction\n\n")

        # Collecter tous les rôles distincts
        all_roles = set()
        for _, roles, _ in usecases:
            all_roles.update(roles)

        # Ajouter acteurs
        for role in all_roles:
            if role.strip():
                f.write('actor "{}"\n'.format(role))

        f.write("\n")

        # Ajouter use cases
        for i, (uc, roles, available) in enumerate(usecases, 1):
            uc_name = "UC{}".format(i)
            f.write('usecase "{}" as {}\n'.format(uc, uc_name))

            # Relier acteurs aux use cases
            for r in roles:
                if r.strip():
                    f.write('"{}" --> {}\n'.format(r, uc_name))

            # Ajouter note si available_expr
            if available and available.strip():
                f.write("note right of {}\n".format(uc_name))
                f.write("Condition: {}\n".format(available.strip()))
                f.write("end note\n")

            f.write("\n")

        f.write("@enduml\n")


if __name__ == "__main__":
    ucs = parse_actions(INPUT)
    generate_puml(ucs, OUTPUT)
    print("Fichier PlantUML  :", OUTPUT)
