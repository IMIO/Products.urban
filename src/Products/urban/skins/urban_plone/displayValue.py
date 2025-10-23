## Script (Python) "displayValue"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=vocab, value, widget=None
##title=Use DisplayList getValue method to translate internal value to a label
##

# XXX changes from urban
# this script comes from Products.Archetypes
# this way, if the value is empty, it display a 'N.C.' and not an empty string
if not value:
    return "<span class='discreet'>%s</span>" % context.utranslate(
        msgid="content_none", domain="urban"
    )
# XXX end of changes
t = context.restrictedTraverse("@@at_utils").translate
return t(vocab, value, widget)
