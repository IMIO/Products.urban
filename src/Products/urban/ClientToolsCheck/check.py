# -*- coding: utf-8 -*-

import _winreg 

i = 0

try:
	firefox = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\mozilla.org\Mozilla',0, _winreg.KEY_READ)
	(valeur, typevaleur) = _winreg.QueryValueEx(firefox,'CurrentVersion')
	_winreg.CloseKey(firefox)
	print u"[+] Firefox est installé avec la version "+ str(valeur) +" ..."
	i += 1
except:
	print u"[-] Firefox n'est pas installé. "
	print u"[-] Veuillez le télécharger à cette adresse: http://www.mozilla.org/fr/firefox/fx/\n"
	
try:
	libreoffice = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\LibreOffice\LibreOffice',0, _winreg.KEY_READ)
	print u"[+] LibreOffice est installé..."
	i += 1
except:
	print u"[-] LibreOffice n est pas installé"
	print u"[-] Veuillez le télécharger à cette adresse: http://fr.libreoffice.org/telecharger/\n"
	
try:
	java = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\JavaSoft',0, _winreg.KEY_READ)
	print u"[+] Java est installé..."
	i += 1
except:
	print u"[-] Java n est pas installé"
	print u"[-] Veuillez le télécharger à cette adresse: http://www.oracle.com/technetwork/java/javase/downloads/jre6u37-downloads-1859589.html\n"

try:
	java = _winreg.OpenKey( _winreg.HKEY_CLASSES_ROOT, 'Zope.ExternalEditor',0, _winreg.KEY_READ)
	print u"[+] Zope External Editor est installé..."
	i += 1
except:
	print u"[-] Zope External Editor n est pas installé"
	print u"[-] Veuillez le télécharger à cette adresse: http://plone.org/products/zope-externaleditor-client\n"	

if i == 4:
	print u"\n[+] Tout est installé [+]"
	
raw_input("Appuyer sur une touche pour quitter le programme")
