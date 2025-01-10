[1mdiff --git a/src/Products/urban/setuphandlers.py b/src/Products/urban/setuphandlers.py[m
[1mindex d2f583251..22895b4ee 100644[m
[1m--- a/src/Products/urban/setuphandlers.py[m
[1m+++ b/src/Products/urban/setuphandlers.py[m
[36m@@ -398,13 +398,20 @@[m [mdef addDefaultEventConfig(context):[m
     """This will add some default event configs that were exported beforehand."""[m
     if context.readDataFile("urban_new_install_marker.txt") is None:[m
         return[m
[31m-    _import_profile_content(context, "event_configs.json")[m
[32m+[m[32m    try:[m
[32m+[m[32m        _import_profile_content(context, "event_configs.json")[m
[32m+[m[32m    except:[m
[32m+[m[32m        import ipdb; ipdb.set_trace() # TODO: REMOVE BEFORE FLIGHT <----------------------------------------------------[m
 [m
 def addDefaultTemplates(context):[m
     """This will add some default pod templates that were exported beforehand."""[m
     if context.readDataFile("urban_new_install_marker.txt") is None:[m
         return[m
[31m-    _import_profile_content(context, "templates.json")[m
[32m+[m[32m    try:[m
[32m+[m[32m        _import_profile_content(context, "base_templates.json")[m
[32m+[m[32m        _import_profile_content(context, "templates.json")[m
[32m+[m[32m    except Exception as e:[m
[32m+[m[32m        import ipdb; ipdb.set_trace()[m
 [m
 def getSharedVocabularies(urban_type, licence_vocabularies):[m
     shared_vocs = licence_vocabularies.get("shared_vocabularies")[m
