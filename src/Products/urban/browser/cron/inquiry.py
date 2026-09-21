# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from plone import api

import transaction
import logging

class InquiryRadiusSearch(BrowserView):
    """
    Browser view to call with cron to automatically
    execute all inquiry radius registered.
    """

    def __call__(self):
        """ """
        catalog = api.portal.get_tool("portal_catalog")
        planned_inquiries = (
            api.portal.get_registry_record(
                "Products.urban.interfaces.IAsyncInquiryRadius.inquiries_to_do"
            )
            or {}
        )
        planned_adress_inquiries = (
            api.portal.get_registry_record(
                "Products.urban.interfaces.IAsyncInquiryRadius.inquiries_address_to_do"
            )
            or {}
        )

        for inquiry_UID in planned_inquiries.keys():
            radius = planned_inquiries.pop(inquiry_UID)
            inquiry = catalog.unrestrictedSearchResults(UID=inquiry_UID)[0].getObject()
            inquiry_view = inquiry.restrictedTraverse("@@urbaneventinquiryview")
            inquiry_view.getInvestigationPOs(radius=radius, force=True)
            api.portal.set_registry_record(
                "Products.urban.interfaces.IAsyncInquiryRadius.inquiries_to_do",
                planned_inquiries,
            )
            transaction.commit()

        for inquiry_UID in planned_adress_inquiries.keys():
            radius = planned_adress_inquiries.pop(inquiry_UID)
            inquiry = catalog.unrestrictedSearchResults(UID=inquiry_UID)[0].getObject()
            inquiry_view = inquiry.restrictedTraverse("@@urbaneventinquiryview")
            inquiry_view.get_investigation_adress(radius=radius, force=True)
            api.portal.set_registry_record(
                "Products.urban.interfaces.IAsyncInquiryRadius.inquiries_address_to_do",
                planned_adress_inquiries,
            )
            transaction.commit()


class InquiryClaimantsImport(BrowserView):
    """
    Browser view to call with cron to automatically
    execute all inquiry claimants import registered.
    """

    def __call__(self):
        logger = logging.getLogger("Products.urban import claimant")
        catalog = api.portal.get_tool("portal_catalog")
        planned_claimants_import = (
            api.portal.get_registry_record(
                "Products.urban.interfaces.IAsyncClaimantsImports.claimants_to_import"
            )
            or []
        )

        total = len(planned_claimants_import)
        logger.info("claimants import cron: starting, %d inquiry(ies) planned" % total)

        inquiries_ok = 0
        inquiries_error = 0
        claimants_imported = 0
        claimants_merged = 0
        claimants_failed = 0
        remaining_imports = list(planned_claimants_import)

        for inquiry_UID in planned_claimants_import:
            try:
                result = catalog.unrestrictedSearchResults(UID=inquiry_UID)
                if not result:
                    logger.warning(
                        "claimants import: inquiry UID %s not found in catalog, skipping"
                        % inquiry_UID
                    )
                    inquiries_error += 1
                else:
                    inquiry = result[0].getObject()
                    inquiry_view = inquiry.restrictedTraverse("@@urbaneventinquiryview")
                    imported, merged, failed = inquiry_view.import_claimants_from_csv()

                    claimants_imported += imported
                    claimants_merged += merged
                    claimants_failed += failed

                    if failed:
                        logger.warning(
                            "claimants import: inquiry UID %s (%s): "
                            "%d imported, %d merged, %d failed"
                            % (inquiry_UID, inquiry.absolute_url(1), imported, merged, failed)
                        )
                    else:
                        logger.info(
                            "claimants import: succeeded for inquiry UID %s (%s): "
                            "%d imported, %d merged"
                            % (inquiry_UID, inquiry.absolute_url(1), imported, merged)
                        )
                    inquiries_ok += 1
            except Exception:
                logger.exception(
                    "claimants import: failed for inquiry UID %s" % inquiry_UID
                )
                inquiries_error += 1
            finally:
                remaining_imports.remove(inquiry_UID)
                api.portal.set_registry_record(
                    "Products.urban.interfaces.IAsyncClaimantsImports.claimants_to_import",
                    remaining_imports,
                )
                transaction.commit()

        logger.info(
            "claimants import cron: finished, %d/%d inquiries processed "
            "(%d inquiry-level errors), %d claimants imported, "
            "%d merged, %d failed"
            % (
                inquiries_ok, total, inquiries_error,
                claimants_imported, claimants_merged, claimants_failed,
            )
        )
