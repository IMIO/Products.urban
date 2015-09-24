files="urban plone datagridfield collective.eeafaceted.z3ctable"
for file in $files; do
    i18ndude sync --pot $file.pot fr/LC_MESSAGES/$file.po
    msgfmt -o fr/LC_MESSAGES/$file.mo fr/LC_MESSAGES/$file.po
done
