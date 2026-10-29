# Cahier des charges · Cantine+ (projet fictif)

## Contexte

L’entreprise **Boréalis** (2 000 employés, 3 sites : Montréal, Laval, Longueuil) veut une application de **précommande de repas** pour ses 3 cafétérias. Aujourd’hui : files d’attente de 25 minutes entre 11 h 45 et 12 h 30, 18 % de repas jetés chaque jour.

## Besoins fonctionnels

1. Consulter le menu de la semaine par site (plats, prix, **allergènes**, calories).
2. Précommander un repas jusqu’à **10 h 30** le jour même, choisir un créneau de retrait de 15 minutes.
3. Payer par **carte** ou par **retenue sur la paie** (employés permanents seulement).
4. Recevoir une notification quand le repas est prêt ; retrait par code QR.
5. Côté cuisine : tableau des commandes par créneau, quantités à préparer, marquage « prêt ».
6. Côté gestion : rapport hebdomadaire (ventes, gaspillage, plats populaires).
7. Annuler une commande jusqu’à 10 h 30, avec remboursement automatique.

## Contraintes et exigences non fonctionnelles

- **Pic de charge** : 1 500 commandes entre 9 h 45 et 10 h 30 ; consultations du menu à 8 h 30.
- **Intégration paie** : le système de paie existant (SAP, interface SOAP, traitement par lot chaque nuit) est la seule source de vérité des employés.
- **Authentification** : comptes Microsoft Entra ID de l’entreprise (SSO).
- **Allergènes** : obligation légale d’affichage exact ; une erreur peut avoir des conséquences graves.
- **Données personnelles** : Loi 25 (Québec) — habitudes alimentaires = renseignements personnels.
- Application **web responsive** d’abord, applications mobiles « plus tard ».
- Équipe : 4 développeurs, 1 PO, 1 designer à mi-temps. Vélocité estimée : **20 points par sprint de 2 semaines**.
- Lancement souhaité : site pilote (Laval) dans **3 sprints**, les 3 sites dans 5 sprints.

## Questions encore ouvertes

- Le prestataire de la cafétéria a-t-il déjà un logiciel de caisse à intégrer ?
- Les employés contractuels ont-ils accès à l’application ?
- Qui met à jour les allergènes, et qui en est responsable ?
