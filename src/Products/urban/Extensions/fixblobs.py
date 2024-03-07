# Zope imports
from ZODB.POSException import POSKeyError

# Plone imports
from plone.app.blob.subtypes.file import ExtensionBlobField
from Products.Archetypes.interfaces import IBaseContent
from plone.namedfile.interfaces import INamedFile
from plone.dexterity.content import DexterityContent
from plone import api

blob_fields = {
    "SubTemplate": "odt_file",
    "DashboardPODTemplate": "odt_file",
    "File": "file",
    "UrbanTemplate": "odt_file",
}


def check_at_blobs(context):
    """Archetypes content checker.

    Return True if purge needed
    """

    if IBaseContent.providedBy(context):

        schema = context.Schema()
        for field in schema.fields():
            id = field.getName()
            if isinstance(field, ExtensionBlobField):
                try:
                    field.get_size(context)
                except POSKeyError:
                    print "Found damaged AT FileField %s on %s" % (
                        id,
                        context.absolute_url(),
                    )
                    return field.getName()

    return False


def check_dexterity_blobs(context):
    """Check Dexterity content for damaged blob fields

    XXX: NOT TESTED - THEORETICAL, GUIDELINING, IMPLEMENTATION

    Return True if purge needed
    """

    # Assume dexterity contennt inherits from Item
    if isinstance(context, DexterityContent):

        # Iterate through all Python object attributes
        # XXX: Might be smarter to use zope.schema introspection here?
        for key, value in context.__dict__.items():
            # Ignore non-contentish attributes to speed up us a bit
            if not key.startswith("_"):
                if INamedFile.providedBy(value):
                    try:
                        value.getSize()
                    except POSKeyError:
                        print "Found damaged Dexterity plone.app.NamedFile %s on %s" % (
                            key,
                            context.absolute_url(),
                        )
                        return key
    return False


def fix_blobs(context):
    """
    Iterate through the object variables and see if they are blob fields
    and if the field loading fails then poof
    """

    corrupted_blob_field = check_at_blobs(context) or check_dexterity_blobs(context)
    if corrupted_blob_field:
        print "Bad blobs found on %s" % context.absolute_url()
        return context.portal_type, corrupted_blob_field

    return ("", "")


def catalog_search():
    portal_types = blob_fields.keys()
    catalog = api.portal.get_tool("portal_catalog")
    brains = catalog(portal_type=portal_types)

    count = 0

    for brain in brains:
        to_check = brain.getObject()
        p_type, field_name = fix_blobs(to_check)
        if p_type:
            count += 1

    return count


def check():
    # plone = getMultiAdapter((self.context, self.request), name="plone_portal_state")
    print "Checking blobs"
    error_counts = catalog_search()
    print error_counts
    print "All done"
    return "OK - check console for status messages"
