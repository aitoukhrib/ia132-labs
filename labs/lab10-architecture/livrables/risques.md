# Registre des risques — Cantine+

| Risque | Probabilité | Impact | Mesure de réduction / réponse |
| --- | --- | --- | --- |
| Allergène manquant ou erroné dans un menu publié | Moyenne | Critique : risque pour la santé et responsabilité légale | Champs obligatoires, double approbation par site, historique immuable, blocage à la publication si donnée incomplète et procédure de retrait immédiat |
| Lot SAP SOAP nocturne en retard, incomplet ou rejeté | Moyenne | Élevé : admissibilité et retenue sur paie incorrectes | Valider le contrat et les cas de rejet tôt ; suivi de fraîcheur ; rapport de rapprochement ; rejouer les lots de façon idempotente ; désactiver la paie si l’état est périmé |
| Pic de commandes à 10 h 30 saturant l’API ou la base | Moyenne | Élevé : commandes perdues ou délai de service excessif | Test de charge de 1 500 commandes réalistes ; transactions courtes ; capacité par créneau ; montée en charge horizontale et alertes de contention |
| Double paiement, double débit de paie ou remboursement rejoué | Moyenne | Élevé : perte financière et réclamations | Clés d’idempotence, machine à états, outbox, rapprochement externe, tests de reprise et intervention manuelle journalisée |
| Indisponibilité du prestataire de paiement ou de notification | Moyenne | Élevé : commande ou retrait bloqué | Circuit de reprise, état explicite « en attente », délais bornés, alertes et procédure de service cuisine ; ne pas confirmer un paiement non autorisé |
| Accès indu ou conservation excessive d’habitudes alimentaires | Moyenne | Élevé : atteinte à la vie privée et conformité Loi 25 | Minimisation, rôles par site, chiffrement, journalisation, rétention approuvée, suppression/anonymisation et revue des accès |
| Capacité de livraison du pilote sous-estimée par la vélocité | Moyenne | Élevé : pilote Laval retardé | Limiter le périmètre du pilote, réserver les sprints à 20 points maximum, traiter les inconnues SAP/paiement tôt et réestimer après chaque sprint |
| QR copié ou retrait confirmé par la mauvaise personne | Faible | Moyen à élevé : repas remis au mauvais employé | Jeton non devinable à usage unique, expiration, vérification de l’état de commande et journal d’annulation/retrait |
