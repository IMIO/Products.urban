from Products.urban.utils import set_default_optional_field

import logging


logger = logging.getLogger("urban: migrations")


def set_additional_reference_as_default(context):
    logger = logging.getLogger(
        "urban: Activate additionalReference for all licences types"
    )
    logger.info("starting upgrade steps")
    updated_types = set_default_optional_field("additionalReference")
    logger.info("Licences updated: {0}".format(", ".join(updated_types)))
    logger.info("migration step done!")
