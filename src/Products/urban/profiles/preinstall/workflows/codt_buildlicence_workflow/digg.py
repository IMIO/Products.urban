from graphviz import Digraph
import re

puml_file = "/src/Products.urban/src/Products/urban/profiles/preinstall/workflows/codt_buildlicence_workflow/workflow1_usecase.puml"
dot = Digraph(comment='Use Case')

actors = {}
usecases = {}

with open(puml_file, 'r') as f:
    for line in f:
        line = line.strip()
        # acteur
        m = re.match(r'^actor\s+(.+)$', line)
        if m:
            actor = m.group(1)
            actors[actor] = actor
            dot.node(actor, actor, shape='actor')
            continue
        # usecase
        m = re.match(r'^usecase\s+"(.+)"\s+as\s+(\w+)$', line)
        if m:
            uc_name, uc_id = m.group(1), m.group(2)
            usecases[uc_id] = uc_name
            dot.node(uc_id, uc_name, shape='ellipse')
            continue
        # lien
        m = re.match(r'^(.+)\s+-->\s+(\w+)$', line)
        if m:
            src, tgt = m.group(1), m.group(2)
            dot.edge(src, tgt)

dot.render('/usecase_diagram', format='png', view=True)
print("Diagramme  : /usecase_diagram.png")
