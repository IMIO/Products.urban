# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from Acquisition import aq_inner
from Products.urban.interfaces import IGenericLicence


def setDefaultLinkedInquiry(opinionRequest, event):
    if opinionRequest.checkCreationFlag():
        licence = opinionRequest.aq_inner.aq_parent
        request_for_opinion = licence.getLastRequestForOpinion()
        opinionRequest.setLinkedInquiry(request_for_opinion)


def set_opinion_round(opinionRequest, event):
    if IGenericLicence.providedBy(opinionRequest):
        return
    licence = aq_parent(aq_inner(opinionRequest))
    all_request_for_opinion = licence.getAllRequestForOpinion()
    last_index = 1
    if len(all_request_for_opinion) < 2:
        return
    previous_request_for_opinion = all_request_for_opinion[-2]
    if previous_request_for_opinion.portal_type == "RequestForOpinion":
        last_index = previous_request_for_opinion.getOpinion_round()
    opinionRequest.setOpinion_round(last_index + 1)


def afterDelete(ob, event):
    """
    After having deleted an Inquiry, we need to generate
    the title of the others so we have something coherent as
    the number of the inquiry is in the title
    """
    # be sure we are on a real Inquiry as some other types heritate from
    # Inquiry and so implements the IInquiry interface
    if IGenericLicence.providedBy(ob):
        return
    for inquiry in ob.getInquiries():
        if not inquiry.portal_type == "RequestForOpinion":
            continue
        inquiry.setTitle(inquiry.generateInquiryTitle())
        inquiry.reindexObject(idxs=("title",))


def setGeneratedTitle(ob, event):
    """
    Set my title
    """
    # be sure we are on a real Inquiry as some other types heritate from
    # Inquiry and so implements the IInquiry interface
    if IGenericLicence.providedBy(ob):
        return
    ob.setTitle(ob.generateInquiryTitle())
    ob.reindexObject(idxs=("title",))
