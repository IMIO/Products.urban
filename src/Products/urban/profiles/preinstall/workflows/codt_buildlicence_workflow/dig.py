import xml.etree.ElementTree as ET

xml_file = "src/Products.urban/src/Products/urban/profiles/preinstall/workflows/codt_buildlicence_workflow/definition.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

roles_dict = {}  # transition_id -> roles
usecases = []    # (transition_title, roles)

for trans in root.findall(".//transition"):
    title = trans.get("title") or trans.get("id")
    perms = trans.get("permissions", "")
    roles = [r.strip() for r in perms.split(",") if r.strip()]
    usecases.append((title, roles))


with open("workflow_usecase.puml", "w") as f:
    f.write("@startuml\n")
    actors = set(r for _, rs in usecases for r in rs)
   
    for actor in actors:
        f.write("actor {}\n".format(actor))


    for i, (uc, rs) in enumerate(usecases, 1):
        f.write('usecase "{}" as UC{}\n'.format(uc, i))
        for r in rs:
            f.write("{} --> UC{}\n".format(r, i))

    f.write("@enduml\n")
