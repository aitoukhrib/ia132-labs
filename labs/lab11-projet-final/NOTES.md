# Rétrospective — lab 11

- **Temps passé :** environ 8 minutes de travail dans cette session, du plan validé aux tests et aux exemples documentés.
- **Ce que l’agent a bien fait :** attendre la validation du plan, découper le travail en modèle/dépôt/CLI et livrer chaque commande en incrément avec tests et commit dédié.
- **Erreur 1 :** le premier formatage séparait les étiquettes par deux espaces ; le test d’acceptation sur les filtres a échoué. Le test a permis de corriger l’espacement sans modifier son attendu.
- **Erreur 2 :** le répartiteur CLI est devenu trop complexe pour la limite Ruff C901 lors de l’ajout de `terminer` et `supprimer`. Ruff l’a détecté ; les commandes ont été extraites en fonctions dédiées avant le commit de l’incrément.
- **Vérification finale :** 28 tests passent, Ruff passe et chaque exemple du README a été exécuté dans un répertoire temporaire, y compris les codes de sortie 1 et 2.
