# -*- coding: utf-8 -*-

def onDelete(ob, event):
    """ Reindex licence after deletion """
    parent = ob.aq_inner.aq_parent
    #as the name of the applicant appears in the licence's title, update it!
    parent.updateTitle()


def reindexLicenceApplicantInfos(applicant, event):
    """ Reindex applicant infos of licence containing the modified applicant """

    parent = applicant.aq_parent
    parent.reindexObject(idxs=['applicantInfosIndex'])
