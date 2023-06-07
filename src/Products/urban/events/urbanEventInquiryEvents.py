# -*- coding: utf-8 -*-


def setLinkedInquiry(ob, event):
    """
      After creation, link me to my Inquiry
    """
    # find the right inquiry and link me to it
    if ob.portal_type != 'UrbanEventInquiry':
        return
    # we have to return inquiries AND announcement so we can tweak announcement
    # event config with the portal type "UrbanEventInquiry" to be able to do
    # the 50m radius search on announcement events. Source: trust me bro...
    inquiries = ob.aq_inner.aq_parent.getAllInquiriesAndAnnouncements()
    existingUrbanEventInquiries = ob.aq_inner.aq_parent.getUrbanEventInquiries()
    myinquiry = inquiries[len(existingUrbanEventInquiries) - 1]
    ob.setLinkedInquiry(myinquiry)


def setLinkedAnnouncement(ob, event):
    """
      After creation, link me to my Announcement
    """
    # find the right announcement and link me to it
    if ob.portal_type != 'UrbanEventAnnouncement':
        return
    announcements = ob.aq_inner.aq_parent.getAllAnnouncements()
    existingUrbanEventAnnouncements = ob.aq_inner.aq_parent.getUrbanEventAnnouncements()
    myannouncement = announcements[len(existingUrbanEventAnnouncements) - 1]
    ob.setLinkedInquiry(myannouncement)
