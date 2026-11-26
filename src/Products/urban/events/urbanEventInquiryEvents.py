# -*- coding: utf-8 -*-


def _get_inquiry_to_link(candidates, existing_events):
    """
    Return the first inquiry/announcement of 'candidates' not yet linked to an
    inquiry/announcement event.
    Falls back on the position based on the number of existing events if every
    candidate is already linked.
    """
    for candidate in candidates:
        if not candidate.getLinkedUrbanEventInquiry():
            return candidate
    return candidates[len(existing_events) - 1]


def setLinkedInquiry(ob, event):
    """
    After creation, link me to my Inquiry
    """
    # find the right inquiry and link me to it
    if ob.portal_type != "UrbanEventInquiry":
        return
    # we have to return inquiries AND announcement so we can tweak announcement
    # event config with the portal type "UrbanEventInquiry" to be able to do
    # the 50m radius search on announcement events. Source: trust me bro...
    licence = ob.aq_inner.aq_parent
    myinquiry = _get_inquiry_to_link(
        licence.getAllInquiriesAndAnnouncements(),
        licence.getUrbanEventInquiries(),
    )
    ob.setLinkedInquiry(myinquiry)


def setLinkedAnnouncement(ob, event):
    """
    After creation, link me to my Announcement
    """
    # find the right announcement and link me to it
    if ob.portal_type != "UrbanEventAnnouncement":
        return
    licence = ob.aq_inner.aq_parent
    myannouncement = _get_inquiry_to_link(
        licence.getAllAnnouncements(),
        licence.getUrbanEventAnnouncements(),
    )
    ob.setLinkedInquiry(myannouncement)
