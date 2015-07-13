*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote


Suite Setup  Suite Setup
Suite Teardown  Close all browsers

Test Setup  Test Setup

*** Variables ***

${CU1_FOLDER_PATH}  /plone/urban/urbancertificateones
${CU1_FOLDER_URL}  ${PLONE_URL}/urban/urbancertificateones
${CU1_ID}  test-urbancertificateone
${specific_feature}  schema-developpement-espace-regional
${field_id_1}  isInPCA
${field_id_2}  folderZone
${field_id_3}  locationFloodingLevel

*** Test Cases ***

Test fieldeditoverlay button is visible when configured
    Edit tab  location
    Scroll browser to field  locationSpecificFeatures
    Page Should Not Contain Link  fieldeditoverlay-${specific_feature}
    Configure specificfeature item  ${specific_feature}
    Set related fields  ${field_id_1}
    Save changes
    Go to CU1
    Edit tab  location
    Scroll browser to field  locationSpecificFeatures
    Page Should Contain Link  fieldeditoverlay-${specific_feature}


Test fieldeditoverlay popup when clicking button
    Configure specificfeature item  ${specific_feature}
    Set related fields  ${field_id_1}
    Save changes
    Go to CU1
    Edit tab  location
    Scroll browser to field  locationSpecificFeatures
    Click Link  fieldeditoverlay-${specific_feature}
    Page Should Contain Element  css=div.spf_edit_schortcut


Test configured fields are visible in the popup
    Configure specificfeature item  ${specific_feature}
    Set related fields  ${field_id_1}  ${field_id_2}
    Save changes
    Go to CU1
    Edit tab  location
    Scroll browser to field  locationSpecificFeatures
    Click Link  fieldeditoverlay-${specific_feature}
    Fields are in popup  ${field_id_1}  ${field_id_2}
    Fields are not in popup  ${field_id_3}


Test selected values in edit form are also selected in popup
    Configure specificfeature item  ${specific_feature}
    Set related fields  ${field_id_1}  ${field_id_2}  ${field_id_3}
    Save changes
    Go to CU1
    Edit tab  location
    Scroll browser to field  locationSpecificFeatures
    Click Link  fieldeditoverlay-${specific_feature}
#
# so far nothing should be selected
    ${popup_field_id_1}  Get field overlay XPath  ${field_id_1}
    Checkbox Should Not Be Selected  xpath=${popup_field_id_1}/input
    ${popup_field_id_3}  Get field overlay XPath  ${field_id_3}
    ${field_3_selection}  Get Selected List Value  xpath=${popup_field_id_3}/select
    Should Be Equal  ${field_3_selection}  \
    Click button  Cancel
#
# select values for these fields
    Scroll browser to field  ${field_id_1}
    ${field_id_1_xpath}  Get field XPath  ${field_id_1}
    Select Checkbox  xpath=${field_id_1_xpath}/input
    Scroll browser to field  ${field_id_2}
    ${field_id_2_xpath}  Get field XPath  ${field_id_2}
    Select From List By Value  xpath=${field_id_2_xpath}/select  zh
    Scroll browser to field  ${field_id_3}
    ${field_id_3_xpath}  Get field XPath  ${field_id_3}
    Select From List By Value  xpath=${field_id_3_xpath}/select  moderate
    Save changes

# now these values should be selected in the fields of the popup as well
    Edit tab  location
    Scroll browser to field  locationSpecificFeatures
    Click Link  fieldeditoverlay-${specific_feature}
    ${popup_field_id_1}  Get field overlay XPath  ${field_id_1}
    Checkbox Should Be Selected  xpath=${popup_field_id_1}/input
    ${popup_field_id_2}  Get field overlay XPath  ${field_id_2}
    ${field_2_selection}  Get Selected List Values  xpath=${popup_field_id_2}/select
    ${expected_list_2}  Create List  zh
    Should Be Equal  ${field_2_selection}  ${expected_list_2}
    ${popup_field_id_3}  Get field overlay XPath  ${field_id_3}
    ${field_3_selection}  Get Selected List Value  xpath=${popup_field_id_3}/select
    Should Be Equal  ${field_3_selection}  moderate


Test form fields are updated when values are selected in the popup
    Configure specificfeature item  ${specific_feature}
    Set related fields  ${field_id_1}  ${field_id_2}  ${field_id_3}
    Save changes
    Go to CU1
    Edit tab  location

# so far nothing should be selected
    ${xpath_id_1}  Get field XPath  ${field_id_1}
    Checkbox Should Not Be Selected  xpath=${xpath_id_1}/input
    ${xpath_id_3}  Get field XPath  ${field_id_3}
    ${field_3_selection}  Get Selected List Value  xpath=${xpath_id_3}/select
    Should Be Equal  ${field_3_selection}  \

# select values on popup fields and click "Ok"
    Scroll browser to field  locationSpecificFeatures
    Click Link  fieldeditoverlay-${specific_feature}
    ${popup_id_1_xpath}  Get field overlay XPath  ${field_id_1}
    Select Checkbox  xpath=${popup_id_1_xpath}/input
    ${popup_id_2_xpath}  Get field overlay XPath  ${field_id_2}
    Select From List By Value  xpath=${popup_id_2_xpath}/select  zh
    ${popup_id_3_xpath}  Get field overlay XPath  ${field_id_3}
    Select From List By Value  xpath=${popup_id_3_xpath}/select  moderate
    Click button  Ok

# now these values should be selected in the edit form as well
    Checkbox Should Be Selected  xpath=${xpath_id_1}/input
    ${xpath_id_2}  Get field XPath  ${field_id_2}
    ${field_2_selection}  Get Selected List Values  xpath=${xpath_id_2}/select
    ${expected_list_2}  Create List  zh
    Should Be Equal  ${field_2_selection}  ${expected_list_2}
    ${field_3_selection}  Get Selected List Value  xpath=${xpath_id_3}/select
    Should Be Equal  ${field_3_selection}  moderate
    Cancel changes


Test field hidden in the edit form still appears in the popup
    Configure specificfeature item  ${specific_feature}
    Set related fields  ${field_id_1}  ${field_id_2}  ${field_id_3}
    Save changes

# hide fields from the edit form
    Configure procedure  urbancertificateone
    Hide fields  ${field_id_1}  ${field_id_2}  ${field_id_3}
    Save changes

    Go to CU1
    Edit tab  location
    Scroll browser to field  locationSpecificFeatures
    Click Link  fieldeditoverlay-${specific_feature}
    Fields are in popup  ${field_id_1}  ${field_id_2}  ${field_id_3}

*** Keywords ***

Suite Setup
    Open test browser
    Enable autologin as  urbanmanager

Test Setup
    Create CU1

Create CU1
    Create content  type=UrbanCertificateOne  id=${CU1_ID}  container=${CU1_FOLDER_PATH}
    Go to CU1
    Edit
# set foldermanager
    ${foldermanager_xpath}  Get field XPath  foldermanagers
    Click element  xpath=${foldermanager_xpath}//input[@class="searchButton addreference"]
    Click element  xpath= //div[@id="atrb_foldermanagers"]//table//input
    Click element  xpath= //div[@id="atrb_foldermanagers"]//div[@class="close"]
    Save changes

Delete CU1
    Delete content  uid_or_path=${CU1_FOLDER_PATH}/${CU1_ID}

Edit
    Click Image  edit.png

Edit tab
    [Arguments]  ${tab_name}

    Edit
    Go to tab  ${tab_name}

Go to CU1
    Go to  ${CU1_FOLDER_URL}/${CU1_ID}

Go to CU1 location specific features config
    Go to  ${PLONE_URL}/portal_urban/urbancertificateone/locationspecificfeatures

Go to tab
    [Arguments]  ${tab_name}

    Scroll browser to  fieldsetlegend-urban_${tab_name}
    Click link  fieldsetlegend-urban_${tab_name}

Configure procedure
    [Arguments]  ${licence_type}

    Go to  ${PLONE_URL}/portal_urban/${licence_type}/edit

Hide fields
    [Arguments]  @{field_ids}

    Scroll browser to field  usedAttributes
    :FOR  ${field_id}  IN  @{field_ids}
    \    Unselect From List By Value  usedAttributes  ${field_id}

Configure specificfeature item
    [Arguments]  ${specificfeature_id}

    Go to  ${PLONE_URL}/portal_urban/urbancertificateone/locationspecificfeatures/${specificfeature_id}/edit

Set related fields
    [Arguments]  @{field_ids}

    Scroll browser to field  relatedFields
    :FOR  ${field_id}  IN  @{field_ids}
    \    Select From List By Value  relatedFields_options  ${field_id}
    Click Button  >>

Save changes
    Click Button  form.button.save

Cancel changes
    Click Button  form.button.cancel

Scroll browser to field
    [Arguments]  ${field_name}

    Scroll browser to  archetypes-fieldname-${field_name}

Scroll browser to
    [Arguments]  ${element_id}

    Execute Javascript  document.getElementById('${element_id}').scrollIntoView()


Fields are in popup
    [Arguments]  @{field_ids}

    Fields appear in popup X times  ${field_ids}  1

Fields are not in popup
    [Arguments]  @{field_ids}

    Fields appear in popup X times  ${field_ids}  0

Fields appear in popup X times
    [Arguments]  ${field_id}  ${X}

    :FOR  ${field_id}  IN  @{field_ids}
    \    ${field_xpath} =  Get field overlay XPath  ${field_id}
    \    Xpath Should Match X Times  ${field_xpath}  ${X}

Get field XPath
    [Arguments]  ${field_id}
    [Return]  //div[@id="archetypes-fieldname-${field_id}"]

Get field overlay XPath
    [Arguments]  ${field_id}
    [Return]  //div[@class="spf_edit_schortcut"]//div[@id="archetypes-fieldname-${field_id}"]

