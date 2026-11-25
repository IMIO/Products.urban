# -*- coding: utf-8 -*-
"""
link an inquiry event to the right inquiry.

Apply:
    bin/instance run .../fix_inquiry_event_links.py <licence_path> <event_id> <inquiry_id> --apply

Example:
    bin/instance run .../fix_inquiry_event_links.py \
        gracehollogne/gracehollogne/urban/codt_buildlicences/codt_buildlicence.2025-08-28.1603823785 \
        urbaneventinquiry.2026-11-20.8409471307 enquete-ndeg4
"""

import sys


def relink_event(event, inquiry):
    """Only change the 'linkedInquiry' reference of the event."""
    event.setLinkedInquiry(inquiry)
    event.reindexObject()


def main(app, args):
    import transaction

    apply_ = "--apply" in args
    args = [arg for arg in args if arg != "--apply"]
    if len(args) != 3:
        sys.exit(__doc__)
    licence_path, event_id, inquiry_id = args

    licence = app.unrestrictedTraverse(licence_path)
    event = licence[event_id]
    inquiry = licence[inquiry_id]
    old = event.getLinkedInquiry()
    print("{} : {} -> {}".format(event_id, old and old.getId(), inquiry.getId()))

    if not apply_:
        print("DRY RUN: nothing written. Add --apply to fix.")
        return
    relink_event(event, inquiry)
    transaction.get().note("SUP-57748: relink {}".format(event_id))
    transaction.commit()
    print("DONE")


if __name__ == "__main__" and "app" in globals():
    main(app, sys.argv[sys.argv.index("-c") + 2 :])
