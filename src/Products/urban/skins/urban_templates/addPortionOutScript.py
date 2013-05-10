## Script (Python) "createurbanevent"
##title=addPortionOutScript
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##
parcel_data = {
    'division': context.REQUEST.get('division', None),
    'section': context.REQUEST.get('section', None),
    'radical': context.REQUEST.get('radical', None),
    'bis': context.REQUEST.get('bis', None),
    'exposant': context.REQUEST.get('exposant', None),
    'puissance': context.REQUEST.get('puissance', None),
    'partie': context.REQUEST.get('partie', None),
    'outdated': context.REQUEST.get('old', False),
    'location': context.REQUEST.get('location', False),
}

proprietary_data = {
    'proprietary': context.REQUEST.get('proprietary', None),
    'proprietary_city': context.REQUEST.get('proprietary_city', None),
    'proprietary_street': context.REQUEST.get('proprietary_street', None),
}

if not parcel_data['section'] or not parcel_data['division']:
    return context.REQUEST.RESPONSE.redirect(context.absolute_url())

if proprietary_data['proprietary']:
    return context.createParcelAndProprietary(parcel_data=parcel_data, proprietary_data=proprietary_data)

parcel_data.pop('location')
return context.createParcel(parcel_data=parcel_data)

return context.portal_urban.createPortionOut(path=context,division=division,section=section,radical=radical,bis=bis,exposant=exposant,puissance=puissance, partie=partie, old=old)
