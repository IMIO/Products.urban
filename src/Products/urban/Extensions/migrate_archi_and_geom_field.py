# -*- coding: utf-8 -*-

from Products.urban.interfaces import IBaseBuildLicence


def migrate_fields(self):
    licence = self
    change = False
    if not IBaseBuildLicence.providedBy(licence):
        return
    architects = licence.getField("architects")
    if architects:
        for architect in architects.get(licence):
            print(
                "{} : move architect {} in representativeContacts".format(
                    licence.getReference(), architect.name1.encode("utf-8")
                )
            )
            rc_list = licence.getRepresentativeContacts()
            rc_list.append(architect)
            licence.setRepresentativeContacts(rc_list)
            licence.setArchitects([])
            change = True
    geometricians = licence.getField("geometricians")
    if geometricians:
        for geometrician in geometricians.get(licence):
            print(
                "{} : move geometrician {} in representativeContacts".format(
                    licence.getReference(), geometrician.name1.encode("utf-8")
                )
            )
            rc_list = licence.getRepresentativeContacts()
            rc_list.append(geometrician)
            licence.setRepresentativeContacts(rc_list)
            licence.setGeometricians([])
            change = True
    return change
