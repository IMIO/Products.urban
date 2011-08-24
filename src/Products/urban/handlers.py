from logging import getLogger

from ZODB.POSException import ConflictError

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.exceptions import ReferenceException

from Products.urban.interfaces import IReferenceableVocabulary

vocabularyRelationship = u"referenceableVocabularyTerm"


def modifiedArchetype(obj, event):
    """ an archetype based object was modified """
    try:    # TODO: is this a bug or a needed workaround?
        existing = set(obj.getReferences(relationship=vocabularyRelationship))
    except AttributeError:
        return
    refs = set()
    for field in obj.Schema().fields():
        if IReferenceableVocabulary.providedBy(field.vocabulary):
            accessor = field.getAccessor(obj)
            value = accessor()
            refs = refs.union(field.vocabulary.getObjectsSet(obj, value))
    for ref in refs.difference(existing):   # add new references and...
        try:
            obj.addReference(ref, relationship=vocabularyRelationship)
        except ReferenceException:
            pass
    for ref in existing.difference(refs):   # removed leftovers
        try:
            obj.deleteReference(ref, relationship=vocabularyRelationship)
        except ReferenceException:
            try:
                # try to get rid of the dangling reference, but let's not
                # have this attempt to clean up break things otherwise...
                # iow, the `try..except` is there, because internal methods
                # of the reference catalog are being used directly here.  any
                # changes regarding these shouldn't break things over here,
                # though...
                refcat = getToolByName(obj, 'reference_catalog')
                uid, dummy = refcat._uidFor(obj)
                brains = refcat._queryFor(uid, None,
                        relationship=vocabularyRelationship)
                objs = refcat._resolveBrains(brains)
                for obj in objs:
                    refcat._deleteReference(obj)
            except ConflictError:
                raise
            except:
                getLogger(__name__).warning('dangling "linkintegrity" '
                    'reference to %r could not be removed.', obj)
