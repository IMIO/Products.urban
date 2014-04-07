*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote


Suite Setup  Suite Setup
Suite Teardown  Close all browsers

Test Setup  Test Setup
Test Teardown  Test Teardown

*** Variables ***

${CU1_FOLDER_PATH}  /plone/urban/urbancertificateones
${CU1_FOLDER_URL}  ${PLONE_URL}/urban/urbancertificateones
${CU1_ID}  test-urbancertificateone

*** Test Cases ***

Test fieldeditoverlay button is visible when configured
    Edit tab  location
    Scroll browser to field  locationSpecificFeatures
    Page Should Not Contain Link  fieldeditoverlay-schema-developpement-espace-regional
    Configure specificfeature item  schema-developpement-espace-regional
    Set related fields  pca  isInPCA  locationFloodingLevel
    Save changes
    Go to CU1
    Edit tab  location
    Scroll browser to field  locationSpecificFeatures
    Page Should Contain Link  fieldeditoverlay-schema-developpement-espace-regional
    Cancel edit


*** Keywords ***

Suite Setup
    Open test browser
    Enable autologin as  urbanmanager

Test Setup
    Create CU1

Test Teardown
    Delete CU1

Create CU1
    Create content  type=UrbanCertificateOne  id=${CU1_ID}  container=${CU1_FOLDER_PATH}
    Go to CU1

Delete CU1
    Delete content  uid_or_path=${CU1_FOLDER_PATH}/${CU1_ID}

Edit
    Click Image  edit.gif

Cancel edit
    Click Button  form.button.cancel

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

Scroll browser to field
    [Arguments]  ${field_name}

    Scroll browser to  archetypes-fieldname-${field_name}

Scroll browser to
    [Arguments]  ${element_id}

    Execute Javascript  document.getElementById('${element_id}').scrollIntoView()
