archgenxml --cfg generate.conf urban.zargo -o tmp

# only keep workflows
cp -rf tmp/profiles/default/workflows ../profiles/default
rm -rf tmp

#remove the content_icon defined for the different content_types
for i in $( ls ../profiles/default/types); do
    sed '/content_icon/d' ../profiles/default/types/$i > tmpfile
    cp tmpfile ../profiles/default/types/$i
done
rm tmpfile
