#!/bin/bash
declare -a languages=("fr")
for lang in "${languages[@]}"; do
		mkdir -p $lang/LC_MESSAGES
done

declare -a domains=("urban")
declare -a extra_domains=("plone" "datagridfield" "collective.eeafaceted.z3ctable" "imio.schedule")

for lang in $(find . -mindepth 1 -maxdepth 1 -type d); do
		for domain in "${domains[@]}"; do
				i18ndude rebuild-pot --pot $domain.pot --merge ./$domain-manual.pot --create $domain ../
				if test -d $lang/LC_MESSAGES; then
						touch $lang/LC_MESSAGES/$domain.po
						i18ndude sync --pot $domain.pot $lang/LC_MESSAGES/$domain.po
				fi
		done
		for domain in "${extra_domains[@]}"; do
				if test -d $lang/LC_MESSAGES; then
						touch $lang/LC_MESSAGES/$domain.po
						i18ndude sync --pot $domain.pot $lang/LC_MESSAGES/$domain.po
				fi
		done

done
