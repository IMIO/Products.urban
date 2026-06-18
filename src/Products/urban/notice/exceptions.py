# -*- coding: utf-8 -*-
import traceback

from Products.urban import UrbanMessage as _
from zope.globalrequest import getRequest
from zope.i18n import translate


def shorten_message(message, max_length=5000, cut_in_middle=True):
    """
    Shorten a message if it exceeds max_length.

    Args:
        message (str): The original message.
        max_length (int): The maximum allowed length.
        cut_in_middle (bool): If True, cut in the middle; otherwise, cut from the end.

    Returns:
        str: The shortened message.
    """
    if len(message) <= max_length:
        return message

    if cut_in_middle:
        # Leave room for the ellipsis and some context on both sides
        half = (max_length - 3) // 2
        start = message[:half]
        end = message[-half:]
        return start + "..." + end
    else:
        # Cut from the end
        return message[: max_length - 3] + "..."


class NoticeException(Exception):
    """Base exception for NOTICE-related errors."""

    def __init__(self, message, original_exception=None):
        self.message = message
        self.original_exception = original_exception

        # Capture the traceback string right when the exception is instantiated
        # traceback.format_exc() works because we are still in the 'except' block
        self.traceback_str = (
            traceback.format_exc() if original_exception else "No traceback available"
        )

        # Initialize the base Exception with ONLY the custom message
        super(NoticeException, self).__init__(self.message)

    def get_error_report(self):
        """
        Generates a detailed report for emails, including the original
        exception (shortened) and the traceback.
        """
        report = self.message

        if self.original_exception:
            original_msg = str(self.original_exception)
            # Shorten the original message if it's too long
            shortened_original = shorten_message(original_msg)
            report += "\nMessage: {}".format(shortened_original)

        # In Python 2.7, if no exception is active, format_exc() returns 'NoneType: None'
        if self.traceback_str and "NoneType: None" not in self.traceback_str:
            report += "\n\n{}".format(self.traceback_str)

        return report


# CRON EXCEPTIONS


class FailedGettingRecentNotificationsException(NoticeException):
    """Raised when getting the list of recent notifications fails."""

    def __init__(self, original_exception):
        msg = "Failed getting the list of recent notifications"
        super(FailedGettingRecentNotificationsException, self).__init__(
            msg, original_exception
        )


class ErrorProcessingNotificationException(NoticeException):
    """Raised when there is an error processing a specific notification."""

    def __init__(self, notification_id, original_exception, retry=False):
        msg = "Error while processing notification {}".format(notification_id)
        if retry:
            msg += " (manual retry)"
        super(ErrorProcessingNotificationException, self).__init__(
            msg, original_exception
        )


class NoImplementationFoundException(NoticeException):
    """Raised when no implementation is found for a notification type."""

    def __init__(self, notification_type):
        msg = "No implementation found for notification type {}".format(
            notification_type
        )
        super(NoImplementationFoundException, self).__init__(msg)


class NoLicenceFoundException(NoticeException):
    """Raised when no licence is found for given references."""

    def __init__(self, urban_reference, referenceFT=None, referenceDGATLP=None):
        msg_parts = ["No licence found for URBAN reference {}".format(urban_reference)]
        if referenceFT:
            msg_parts.append("reference FT {}".format(referenceFT))
        if referenceDGATLP:
            msg_parts.append("reference DGATLP {}".format(referenceDGATLP))
        msg = ", or ".join(msg_parts)
        super(NoLicenceFoundException, self).__init__(msg)


class NoEnabledEventConfigFoundException(NoticeException):
    """Raised when no enabled EventConfig is found for a marker."""

    def __init__(self, marker, licence_type):
        msg = "No enabled EventConfig found for marker {} of licence type {}".format(
            marker, licence_type
        )
        super(NoEnabledEventConfigFoundException, self).__init__(msg)


class NoMatchingEventFoundException(NoticeException):
    """Raised when no matching event is found on a licence."""

    def __init__(self, event_type):
        msg = "No matching {} event could be found on this licence".format(event_type)
        super(NoMatchingEventFoundException, self).__init__(msg)


class NoPreviousEventFoundException(NoticeException):
    """Raised when no previous event is found for a specific entity."""

    def __init__(self, event_type, entity_id):
        msg = "No previous {} has been found for {}".format(event_type, entity_id)
        super(NoPreviousEventFoundException, self).__init__(msg)


# FORM EXCEPTIONS


class NoticeResponseException(NoticeException):
    """Raised when there is an error while posting a notification response."""

    user_msg_template = _(
        u"Couldn't process your request. Please contact an administrator."
    )

    def __init__(self, customer_ticket=None, original_exception=None):
        message = u"Unexpected error while posting a NOTICE response\ncustomer ticket: {}".format(
            customer_ticket
        )
        super(NoticeResponseException, self).__init__(message, original_exception)

    def get_user_message(self):
        return translate(self.user_msg_template, "urban", context=getRequest())


class UnprocessableEntityException(NoticeResponseException):
    """Raised when an unprocessable entity (HTTP code 422) is encountered is returned by the WS."""

    user_msg_template = _(
        u"Couldn't process your request. Please contact an administrator."
    )

    def __init__(self, url, details, original_exception=None):
        message = (
            u"Unexpected error while posting a NOTICE response\n"
            u"NOTICE WS returned a 422 code (unprocessable entity)\n"
            u"- URL: {}\n"
            u"- Details: {}"
        ).format(url, details)
        super(NoticeResponseException, self).__init__(message, original_exception)


class WrongStatusException(NoticeResponseException):
    """Raised when trying to answer a notification with wrong status."""

    user_msg_template = _(
        u"Couldn't process your request: this notification does not have the correct status in Notice"
    )

    def __init__(self, information, customer_ticket=None, original_exception=None):
        message = (
            u"Unexpected error while posting a NOTICE response\n"
            u"Notification does not have the correct status in Notice\n"
            u"{}\n"
            u"customer ticket: {}"
        ).format(
            information,
            customer_ticket,
        )
        super(NoticeResponseException, self).__init__(message, original_exception)


class MissingNotificationException(NoticeResponseException):
    """Raised when trying to answer a notification that doesn't exist."""

    user_msg_template = _(
        u"Couldn't process your request: this notification does not exist in Notice"
    )

    def __init__(self, information, customer_ticket=None, original_exception=None):
        message = (
            u"Unexpected error while posting a NOTICE response\n"
            u"Notification does not exist in Notice\n"
            u"{}\n"
            u"customer ticket: {}"
        ).format(
            information,
            customer_ticket,
        )
        super(NoticeResponseException, self).__init__(message, original_exception)


class MalformedFieldException(NoticeResponseException):
    """Raised when trying to answer a notification with a malformed field."""

    user_msg_template = _(
        u"Couldn't process your request. Please contact an administrator."
    )

    def __init__(self, information, customer_ticket=None, original_exception=None):
        message = (
            u"Unexpected error while posting a NOTICE response\n"
            u"A field is malformed\n"
            u"{}\n"
            u"customer ticket: {}"
        ).format(information, customer_ticket)
        super(NoticeResponseException, self).__init__(message, original_exception)


class MissingFieldException(NoticeResponseException):
    """Raised when trying to answer a notification with a missing field."""

    user_msg_template = _(
        u"Couldn't process your request. Please contact an administrator."
    )

    def __init__(self, information, customer_ticket=None, original_exception=None):
        message = (
            u"Unexpected error while posting a NOTICE response\n"
            u"A field is missing\n"
            u"{}\n"
            u"customer ticket: {}"
        ).format(information, customer_ticket)
        super(NoticeResponseException, self).__init__(message, original_exception)
