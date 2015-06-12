#!/bin/sh
#
# Shell script to manage .po files.
#
# Run this file in the folder main __init__.py of product
#
# E.g. if your product is yourproduct.name
# you run this file in yourproduct.name/yourproduct/name
#
#
# Copyright 2009 Twinapex Research http://www.twinapex.com
# Adapted by CommunesPlone sge
#

# Assume the product name is the current folder name
CURRENT_PATH=`pwd`
CATALOGNAME="urban"

# List of managed languages (separated by space)
LANGUAGES="fr"

# Create locales folder structure for languages
install -d locales
for lang in $LANGUAGES; do
    install -d locales/$lang/LC_MESSAGES
done

# Rebuild .pot
if ! test -f locales/$CATALOGNAME.pot; then
    i18ndude rebuild-pot --pot locales/$CATALOGNAME.pot --create $CATALOGNAME .
fi

# Finding pot files
for pot in $(find locales -mindepth 1 -maxdepth 1 -type f -name "*.pot" ! -name generated.pot); do
    catalog=`echo $pot | cut -d "/" -f 2 | cut -d "." -f 1`
    echo "=> Found pot $pot"
    # Compile po files
    for lang in $(find locales -mindepth 1 -maxdepth 1 -type d); do
    
        if test -d $lang/LC_MESSAGES; then
    
            PO=$lang/LC_MESSAGES/$catalog.po
            # Create po file if not exists
            touch $PO
    
            # Sync po file
            echo " -> Syncing $PO"
            i18ndude sync --pot $pot $PO
    
            # Compile .po to .mo
            MO=$lang/LC_MESSAGES/$catalog.mo
            echo " -> Compiling $MO"
            msgfmt -o $MO $lang/LC_MESSAGES/$catalog.po
        fi
    done
done