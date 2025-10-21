import csv
from Products.CMFCore.utils import getToolByName

portal = app['testBuilding']  # remplace par l'ID de ton site
wf_tool = getToolByName(portal, 'portal_workflow')

with open("/tmp/workflows.csv", "wb") as f:  # 'wb' pour Python 2
    writer = csv.writer(f)
    writer.writerow(["Workflow", "State", "Permission", "Roles"])
    for wf_id in wf_tool.listWorkflows():
        wf = wf_tool.getWorkflowById(wf_id)
        for state_id, state_def in wf.states.items():
            for perm, roles in state_def.permission_roles.items():
                writer.writerow([
                    wf_id.encode('utf-8'),
                    state_id.encode('utf-8'),
                    perm.encode('utf-8'),
                    ", ".join(roles).encode('utf-8')
                ])

print("Export CSV termin : /tmp/workflows.csv")
