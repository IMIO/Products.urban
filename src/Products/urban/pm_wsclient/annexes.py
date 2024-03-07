# -*- coding: utf-8 -*-

from imio.pm.wsclient.interfaces import ISendableAnnexesToPM

from zope.filerepresentation.interfaces import IRawReadFile
from zope.interface import implements


class UrbanEventAnnexesToPM(object):
    """ """

    implements(ISendableAnnexesToPM)

    def __init__(self, context):
        self.urban_event = context
        self.licence = context.aq_parent

    def get(self):
        """ """
        all_documents = [
            ["", self.urban_event.getAttachments() + self.urban_event.getDocuments()],
            ["dossier", self.licence.getAttachments()],
        ]
        for urban_event in self.licence.getUrbanEvents():
            if urban_event != self.urban_event:
                all_documents.append(
                    [urban_event.Title(), urban_event.getAttachments()]
                )
        annexes = []
        for category, documents in all_documents:
            for doc in documents:
                annexes.append(
                    {
                        "title": "{}{}".format(
                            doc.title, category and " ({})".format(category) or ""
                        ),
                        "UID": doc.UID(),
                    }
                )
        return annexes


class UrbanReadFile(object):
    """ """

    implements(IRawReadFile)

    encoding = "utf-8"
    name = None

    def __init__(self, context):
        self.context = context
        self._size = 0

    def size(self):
        stream = self._getStream()
        pos = stream.tell()
        stream.seek(0, 2)
        size = stream.tell()
        stream.seek(pos)
        return size

    def read(self, size=None):
        if size is not None:
            return self._getStream().read(size)
        else:
            return self._getStream().read()

    def readline(self, size=None):
        if size is None:
            return self._getStream().readline()
        else:
            return self._getStream().readline(size)

    def readlines(self, sizehint=None):
        if sizehint is None:
            return self._getStream().readlines()
        else:
            return self._getStream().readlines(sizehint)

    def _getStream(self):
        return self.context.getFile().getIterator()

    def __iter__(self):
        return self

    def next(self):
        return self._getStream().next()

    @property
    def encoding(self):
        return self._getMessage().get_charset() or "utf-8"

    @property
    def name(self):
        return self.context.getFilename()
