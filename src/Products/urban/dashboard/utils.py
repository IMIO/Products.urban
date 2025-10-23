# -*- coding: utf-8 -*-

from Products.urban.utils import get_env_variable_value

import os


def get_procedure_category(context, request):
    """
    Return the procedure category (CODT/CWATUPE) for the given context
    and request
    """
    category = request.form.get("category", "CODT")
    if category in ("CODT", "CWATUPE"):
        return category
    if context.id.startswith("codt"):
        return "CODT"
    return "CWATUPE"


def switch_config_folder(config_file, base_folder="config"):
    current_path = os.path.dirname(os.path.abspath(__file__))
    config = get_env_variable_value("URBAN_DASHBOARD_CONFIGS", "classic")
    return os.path.join(current_path, base_folder, config, config_file)
