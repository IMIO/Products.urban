# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from Products.urban import UrbanMessage as _
from Products.urban.interfaces import IGenericLicence
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form import field
from z3c.form.form import Form
from zope import schema
from zope.interface import Interface

import transaction
import logging


logger = logging.getLogger("Closed task utils view")


class ICloseTaskSchema(Interface):
    folder_manager = schema.List(
        title=_("Licence Folder Manager"),
        value_type=schema.Choice(vocabulary="urban.folder_managers"),
        required=False,
    )

    licence_type = schema.List(
        title=_("Licence Types"),
        value_type=schema.Choice(vocabulary="urban.vocabularies.licence_types"),
        required=False,
    )

    review_state = schema.List(
        title=_("Licence States"),
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.WorkflowStates"),
        required=False,
    )

    force_close_frozen = schema.Bool(
        title=_("Force close frozen task"), required=False, default=True
    )


class CloseTaskForm(Form):
    fields = field.Fields(ICloseTaskSchema)
    ignoreContext = True

    def search_tasks(self, data):
        query = {
            "context": api.portal.get()["urban"],
            "object_provides": IGenericLicence,
        }
        licence_type = data.get("licence_type", None)
        if licence_type:
            query["portal_type"] = licence_type

        folder_manager = data.get("folder_manager", None)
        if folder_manager:
            query["folder_manager"] = folder_manager

        review_state = data.get("review_state", None)
        if review_state:
            query["review_state"] = review_state

        brains = api.content.find(**query)

        tasks = [item for brain in brains for item in brain.getObject().getAllTasks()]
        return tasks

    @button.buttonAndHandler(u"Close")
    def handleClose(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        tasks = self.search_tasks(data)
        force_close_frozen = data.get("force_close_frozen", False)
        for task in tasks:
            closed_task = False
            if task.get_state() == "frozen" and force_close_frozen:
                task._thaw()
                closed_task = True
            task._end()
            task.reindex_parent_tasks(idxs=["is_solvable_task"])
            if task.get_state() != "frozen":
                closed_task = True
            if closed_task:
                msg = u"Task closed : {} ({})".format(
                    safe_unicode(task.Title()), task.get_container().absolute_url()
                )
                api.portal.show_message(message=msg, request=self.request)
                logger.info(msg)
        transaction.commit()


class CloseTaskView(FormWrapper):
    form = CloseTaskForm
    index = ViewPageTemplateFile("templates/close_task.pt")
