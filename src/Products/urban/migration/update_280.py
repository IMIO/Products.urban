
def reimport_actions_for_listing_zip_code_notaries(setup):
    """Reimport actions to include the new zip code listing action for notaries."""
    setup.runImportStepFromProfile('profile-Products.urban:default', 'actions')
