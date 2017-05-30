# -*- coding: utf-8 -*-


def get_procedure_category(context, request):
    """
    Return the procedure category (CODT/CWATUPE) for the given context
    and request
    """
    category = request.form.get('category', 'CODT')
    if category in ('CODT', 'CWATUPE'):
        return category
    if context.id.startswith('codt'):
        return 'CODT'
    return 'CWATUPE'
