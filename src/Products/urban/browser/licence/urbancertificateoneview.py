from Products.urban.browser.licence.licenceview import UrbanCertificateBaseView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _


class UrbanCertificateOneView(UrbanCertificateBaseView):
    """
    This manage the view of UrbanCertificateOne
    """

    def __init__(self, context, request):
        super(UrbanCertificateBaseView, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets on licences
        self.request.set("disable_plone.rightcolumn", 1)
        self.request.set("disable_plone.leftcolumn", 1)
        plone_utils = getToolByName(context, "plone_utils")
        if not self.context.getProprietaries():
            plone_utils.addPortalMessage(_("warning_add_an_applicant"), type="warning")

    def getMacroViewName(self):
        return "urbancertificateone-macros"

    def getPatrimonyFields(self):
        return self.getSchemataFields(schemata="urban_patrimony")

    def getRankingOrdinanceTitle(self):
        code_dgo4 = "code dgo4"
        libelle = "libelle"
        historique_dossier = "historique_dossier"
        liendoc = "liendoc"
        return "{} - {} - {} - {}".format(
            code_dgo4, libelle, historique_dossier, liendoc
        )

    def getRankingOrdinanceLink(self):
        liendoc = "http://spw.wallonie.be/dgo4/index.php?thema=bc_pat&details=57081-CLT-0239-01"
        return liendoc
