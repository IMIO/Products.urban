from DateTime import DateTime
from plone import api
from Products.urban import config
from Products.urban.interfaces import IGenericLicence


def close_licences():
    catalog = api.portal.get_tool("portal_catalog")
    portal_workflow = api.portal.get_tool("portal_workflow")
    date_range = {
        "query": (DateTime("2002-01-01"), DateTime("2021-03-31")),
        "range": "min:max",
    }
    brains = catalog(object_provides=IGenericLicence.__identifier__, created=date_range)
    to_close = [b for b in brains if b.review_state not in config.LICENCE_FINAL_STATES]
    for brain in to_close:
        licence = brain.getObject()
        workflow_def = portal_workflow.getWorkflowsFor(licence)[0]
        closing_state = "accepted"
        if closing_state in workflow_def.states.objectIds():
            workflow_id = workflow_def.getId()
            workflow_state = portal_workflow.getStatusOf(workflow_id, licence)
            if workflow_state:
                workflow_state["review_state"] = closing_state
                portal_workflow.setStatusOf(workflow_id, licence, workflow_state.copy())
            else:
                api.content.transition(licence, "iscomplete")
                api.content.transition(licence, "accept")
            print "closed licence {}".format(licence.Title())
            licence.reindexObject(idxs=["review_state", "allowedRolesAndUsers"])
    print "closed {} licences".format(len(to_close))
