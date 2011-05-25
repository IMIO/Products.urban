# -*- coding: utf-8 -*-

import os
def getOsTempFolder():
    tmp = '/tmp'
    if os.path.exists(tmp) and os.path.isdir(tmp):
        res = tmp
    elif os.environ.has_key('TMP'):
        res = os.environ['TMP']
    elif os.environ.has_key('TEMP'):
        res = os.environ['TEMP']
    else:
        raise "Sorry, I can't find a temp folder on your machine."
    return res

drainageTechnicalRequirementsDefaultValue = """
<p>1. Aucun descendant d’eaux pluviales ne pourra faire saillie sur le domaine public.  Ils seront intégrés dans la maçonnerie de façade.  Ils seront munis d’un dauphin en fonte d’une hauteur de 1 mètre à partir du sol.  Ils seront raccordés au réseau privatif du bâtiment car aucun rejet d’eaux pluviales sur le domaine public n’est autorisé. Cette donnée technique n’est d’application que si le projet prévoit des descendants d’eaux pluviales en façade à rue.</p>
<p>2. Reprise de l’extension du réseau d’égouttage sur le réseau existant du bâtiment.</p>
<p>3. L’égout public n’aboutissant pas encore à une station d’épuration collective, les eaux usées transiteront via fosse septique by passable d’une capacité minimale de 3000 litres, rejet vers égout public. (**) Art. R.277§4</p>
<p>4. Eaux pluviales via citerne de 10m³ avec trop-plein vers tranchée drainante / vers égout public.</p>
<p>5. Le niveau de la sortie des eaux sera tel que le raccordement au futur égout public devra être réalisable via une chambre de prélèvement situé en domaine privé, à la limite du domaine public.</p>
<p>6. Le raccordement à l’égout public fera l’objet d’une demande d’autorisation séparée auprès de l’administration communale.  Il est à noter que ces travaux sont à charge du demandeur.  Il est également rappelé que, l’évacuation des eaux urbaines résiduaires doit se faire soit gravitairement, soit par système de pompage. (**) Art. R.277 § 3</p>
<p>7. Le demandeur réalisera l’obstruction du raccordement à l’égout public des bâtiments démolis et ce afin d’éviter toutes intrusions de boue, de terre, de déchets… dans l’égouttage public.  La condamnation du raccord particulier abandonné se fera à la limite du domaine public et du domaine privé par un bouchon.</p>
<p>8. Toute nouvelle habitation doit être équipée d’un système séparant l’ensemble des eaux pluviales des eaux usées. Toutes nouvelle habitation située le long d’une voirie non encore égouttée, doit être équipée d’une fosse sceptique by-passable d’une capacité de 3000 litres. La fosse septique by-passable est implantée préférentiellement entre l’habitation et le futur réseau d’égouttage de manière à faciliter le raccordement ultérieur au futur égout public. Les eaux usées en sortie de la fosse septique seront évacuées vers XXXX. (**) Art. R. 277 § 4</p>
<p>9. Toute nouvelle habitation construite en zone soumise au régime d’assainissement collectif le long d’une voirie non encore équipée d’égouts doit être équipée d’origine d’un système d’épuration répondant aux conditions définies dans les arrêtés pris en exécution du décret du 11 mars 1999 relatif au permis d’environnement, lorsqu’il est d’ores et déjà établi le coût du raccordement à un égout futur serait excessif en vertu du 1<sup>er</sup> Art. R. 278 (**)</p>
<p>10. En ce qui concerne le système dispersant, nous rappelons au demandeur que le XXXX a procédé à un test de percolation.  Nous nous référons aux conclusions dudit rapport y relatif de XXXX qui préconisait l’emploi d’un YYYYY pour la dispersion des eaux usées traitées et de pluies.  L’implantation du système de dispersion par le demandeur se fera suivant les normes en vigueur.</p>
<p>11. En aucun cas la Ville de Mons ne pourra être tenue responsable du non respect du rapport de XXXX ainsi que du non respect des normes pour l’implantation dudit système, par le demandeur.  Nous rappelons au demandeur que le système de dispersion ne peut être à moins de 5m de toute zone capable de bâtisse et à moins de 3m de toute limite de propriété voisine et arbres.</p>
<p>12. En ce qui concerne le principe de dispersion, le demandeur réalisera à ses frais un test de conductivité hydraulique afin de s’assurer du système de dispersion à retenir ainsi que de son bon dimensionnement.  La Ville de Mons ne pourra être tenue responsable de tout problème lié au système de dispersion choisi par le demandeur.  Nous rappelons au demandeur que le système de dispersion ne peut être à moins de 5m de toute zone capable de bâtisse et à moins de 3m de toute limite de propriété voisine et arbres.</p>
<p>13. Le bâtiment étant existant, ce dernier doit être déjà raccordé à l’égout public, dès lors tout nouveau raccord à l’égout public devra clairement être justifié par le biais d’une demande d’autorisation séparée auprès de notre administration qui étudiera la motivation du demandeur. Il est à noter que ces travaux de raccord sont à charge du demandeur. (**) Art. R. 277 § 1<sup>er</sup></p>
<p>14. Le raccordement à cet endroit présente des risques d’inondation en cas de fortes pluies.  Le demandeur prend en charge les risques éventuels liés aux inondations ainsi que toutes les précautions inhérentes à ce type de raccordement.</p>
<p>15. Eaux de ruissellement du hall technique et des aires de manœuvres transiteront via séparateur d’hydrocarbure et débourbeur.</p>
<p>16. <span>La piscine doit être entretenue par filtre.  Le rejet des eaux excédentaires et des eaux de vidange se fera via une pompe dans le réseau existant de l’habitation privée jouxtant la piscine.</span></p>
<p>17. Vu l’espace réduit pour un système de dispersion performant, une fosse à vidanger est une solution envisageable dans l’attente d’un raccord au futur égout public. Néanmoins, nous attirons l’attention du demandeur sur le principe de la fosse à vidanger. Cette solution est accordée à titre exceptionnelle. Le demandeur veillera à entretenir et à vidanger à fréquence régulière sa fosse. La Ville de Mons ne pourra être tenu responsable de toute négligence de la part du demandeur à l’encontre de la fosse à vidanger et de la citerne à eaux de pluies. Le demandeur prendra toutes les mesures utiles et nécessaires ainsi que toutes les précautions inhérentes à ce système d’égouttage</p>
<p><b>(**) A.G.W. du 3 mars 2005 relatif au livre II du Code de l’Environnement contenant le Code de l’Eau (M.B. 12/04/2005 – err.21/06/2005), modifié par A.G.W. le 06 décembre 2006 (MB 17.01.2007) relatif au règlement général d’assainissement des eaux urbaines résiduaires.</b></p>
"""
