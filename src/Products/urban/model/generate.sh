archgenxml --cfg generate.conf urban.zargo
#manage generated.pot
cp ../i18n/generated.pot ../locales
rm -rf ../i18n

#remove the content_icon defined for the different content_types
for i in $( ls ../profiles/default/types); do
    sed '/content_icon/d' ../profiles/default/types/$i > tmpfile
    cp tmpfile ../profiles/default/types/$i
done
rm tmpfile
