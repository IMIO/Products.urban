# -*- coding: utf-8 -*-
urbanEventTypes = {
                    'buildlicence':
                    (
                    {
                    'id': "accuse-de-reception",
                    'title': "Accusé de réception (dossier complet - article 116 § 1)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'eventTypeType': 'Products.urban.interfaces.IAcknowledgmentEvent',
                    'podTemplates': (
                                     {'id': "urb-accuse", 'title': "Accusé de réception"},
                                     {'id': "urb-accuse-demande-paiement", 'title': "Demande de paiement"},
                                    ),
                    },
                   ),
                   }
