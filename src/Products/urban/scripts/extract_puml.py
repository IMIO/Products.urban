# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import BaseObject
import codecs

try:
    from zope.schema import getFieldsInOrder
except ImportError:
    getFieldsInOrder = None  # Dexterity fallback


def export_archetypes_and_dexterity_to_puml(app, site_id='Plone', output_path="archetypes.puml"):
    portal = app['testBuilding']
    portal_types = getToolByName(portal, 'portal_types')

    with codecs.open(output_path, "w", "utf-8") as ff:
        ff.write(u"@startuml\n\n")
        ff.write(u"title Diagramme des types Archetypes et Dexterity\n\n")


        relations = []

        for fti in portal_types.objectValues():
            schema = None
            if hasattr(fti, 'lookupSchema'):
                try:
                    schema = fti.lookupSchema()
                except Exception:
                    schema = None
            elif hasattr(fti, 'schema') and not isinstance(fti.schema, str):
                schema = fti.schema

            if schema is None:
                continue

         
            fields = []
            if hasattr(schema, 'fields'):
                fields = list(schema.fields())
            elif getFieldsInOrder is not None:
                try:
                    fields = [f for _, f in getFieldsInOrder(schema)]
                except Exception:
                    continue

           
            ff.write(u'class {0} as "{1}" {{\n'.format(fti.id, fti.Title()))
            for field in fields:
                field_type = field.__class__.__name__
                name = getattr(field, 'getName', lambda: getattr(field, '__name__', ''))()
                ff.write(u'  {0}: {1}\n'.format(name, field_type))

               
                if field_type in ('ReferenceField', 'ReferenceBrowserWidget', 'RelationChoice', 'RelationList'):
                    rel_target = getattr(field, 'relationship', None) or getattr(field, 'vocabulary', None)
                    if rel_target:
                        
                        target_type = getattr(field, 'allowed_types', None)
                        if target_type:
                            if isinstance(target_type, (list, tuple)):
                                for t in target_type:
                                    relations.append((fti.id, t, name))
                            else:
                                relations.append((fti.id, target_type, name))
            ff.write(u"}\n\n")

        for src, dst, name in relations:
            ff.write(u'{0} --> {1} : {2}\n'.format(src, dst, name))

        ff.write(u"@enduml\n")

    print("Diagramme généré :", output_path)


if __name__ == "__main__":
    import sys
    site_id = 'testBuilding'
    output_path = 'archetypes.puml'
    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            site_id = arg
            break

    # `app` doit être défini par Zope/instance
    export_archetypes_and_dexterity_to_puml(app, site_id, output_path)
