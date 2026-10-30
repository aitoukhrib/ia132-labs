# Architecture proposée — Cantine+

## Questions de cadrage classées par impact

1. **Allergènes — responsabilité et validation :** qui fournit les données, qui les vérifie avant publication et quelle preuve doit être conservée ?
2. **Paie SAP — contrat d’intégration :** quels champs, volumes, délais, rejets et accusés de réception sont disponibles dans les traitements SOAP nocturnes ?
3. **Paiement — prestataires :** quel fournisseur traite les cartes et quelles garanties d’idempotence et de remboursement offre-t-il ?
4. **Caisse — exploitation :** les cafétérias utilisent-elles un logiciel de caisse qui doit être intégré au pilote ?
5. **Employés — admissibilité :** les contractuels peuvent-ils commander, ou le pilote est-il limité aux employés permanents présents dans SAP ?
6. **Charge — objectif mesurable :** les 1 500 commandes représentent-elles des tentatives, des commandes payées ou des utilisateurs concurrents, et quel temps de réponse est attendu ?
7. **Notifications — canaux et coûts :** courriel, SMS ou notification web, et quels délais de livraison sont requis ?
8. **Loi 25 — conservation :** quelles durées de conservation, règles de suppression et responsabilités de traitement ont été approuvées ?

## Réponses de cadrage du PO

Pour établir une première architecture sans inventer des intégrations, le PO retient les décisions provisoires suivantes :

- **Caisse :** aucune intégration au logiciel de caisse n’est requise pour le pilote Laval. Les commandes Cantine+ constituent la liste de préparation ; les ventes sont rapprochées dans le rapport hebdomadaire.
- **Contractuels :** ils ne sont pas admissibles au pilote. L’accès et la retenue sur paie sont limités aux employés permanents confirmés par le fichier nocturne SAP.
- **Allergènes :** la personne responsable du menu de chaque site saisit et confirme les allergènes ; un gestionnaire désigné effectue une seconde vérification avant publication. Toute modification est auditée. Cette règle doit être confirmée par le responsable légal avant production.

Les autres réponses (fournisseurs de paiement et de notification, contrat SAP détaillé, objectifs de latence et calendrier de conservation) restent des décisions à obtenir avant le pilote.

## Options comparées

| Option | Compromis face aux contraintes |
| --- | --- |
| **A — Monolithe modulaire, retenu** | Un déploiement web/API avec modules séparés pour menu, commandes, paiements, cuisine et rapports. Une équipe de quatre peut livrer et exploiter cette solution simplement. Le pic de 10 h 30 est absorbé par plusieurs instances sans état, une base de données transactionnelle et un traitement asynchrone des notifications et lots. L’adaptateur SAP SOAP reste isolé dans un module et exécute les échanges nocturnes. Les validations d’allergènes et leur journal sont centralisés. Le couplage et la montée en charge indépendante des modules sont moins bons qu’avec des services séparés. |
| **B — Microservices** | Les commandes, menus, paiements et intégrations pourraient évoluer et se mettre à l’échelle séparément lors du pic. Les frontières faciliteraient l’isolation de certains incidents et des changements fournisseurs SAP/paiement. En contrepartie, l’équipe devrait opérer plusieurs déploiements, communications réseau, cohérence distribuée, observabilité et contrats de données. Le workflow de commande avec paiement et contrôle d’allergènes serait plus complexe ; ce coût compromet le pilote en trois sprints. Cette option ne se justifie que si les volumes ou équipes augmentent nettement. |

## Décision de conception

Adopter l’option A : une application web responsive et un **monolithe modulaire**, avec une base relationnelle transactionnelle. Le serveur applicatif reste sans état et peut être répliqué derrière un répartiteur. Un worker séparé, livré avec le même code, traite l’import SAP nocturne, les notifications et les remboursements différés à partir d’une boîte d’envoi transactionnelle (outbox). Cela évite de perdre un événement entre l’enregistrement d’une commande et son traitement.

### Diagramme

```mermaid
flowchart LR
    employe[Employé - navigateur responsive] --> entra[Microsoft Entra ID - SSO]
    employe --> web[HTTPS - répartiteur]
    cuisine[Équipe cuisine] --> web
    gestion[Gestionnaire de menu] --> web
    web --> app[Monolithe modulaire Cantine+]
    app --> modules[Menu et allergènes | Commandes et créneaux | Paiement | Cuisine et retrait QR | Rapports]
    modules --> db[(Base relationnelle)]
    modules --> outbox[(Outbox et tâches)]
    worker[Worker de tâches] --> outbox
    worker --> sap[SAP - SOAP - lot nocturne]
    worker --> carte[Prestataire carte - API]
    worker --> notif[Prestataire de notification - à choisir]
    app --> db
```

### Composants

| Composant | Responsabilité | Contrôle important |
| --- | --- | --- |
| Interface web responsive | Menu, commande, paiement, suivi, cuisine et gestion | SSO Entra ID ; autorisations par rôle et site |
| Module identité et employés | Associer l’identité Entra à un employé et à son admissibilité | SAP demeure la source de vérité ; absence ou fraîcheur invalide = paie désactivée |
| Module menu et allergènes | Publier menus, prix, calories et allergènes par site | Double validation, historisation, audit et blocage de publication incomplète |
| Module commandes | Vérifier le cutoff de 10 h 30, créneaux de 15 minutes et capacité | Transaction atomique, unicité/idempotence et heure serveur |
| Module paiement | Paiement carte et demande de retenue sur paie | Ne jamais stocker de données de carte ; journal et rapprochement des lots |
| Module cuisine et retrait | Vue par créneau, quantités, état « prêt » et validation QR | QR à usage contrôlé ; accès limité au site |
| Worker et outbox | Import SOAP SAP nocturne, notifications, remboursements et reprises | Idempotence, tentatives bornées, alertes et file d’échec |
| Base relationnelle | Données opérationnelles, commandes, rôles, audit et outbox | Chiffrement, sauvegardes, accès minimal et règles de conservation Loi 25 |
| Rapports | Ventes, gaspillage et popularité par semaine/site | Données agrégées autant que possible ; accès gestion restreint |

### Exigences de mise en œuvre et de mise en service

- **Pic :** mesurer au minimum le scénario de 1 500 commandes concentrées dans la fenêtre 9 h 45–10 h 30 ; vérifier la capacité des créneaux, la contention en base, le paiement et les reprises. Les consultations de menu à 8 h 30 peuvent être servies en lecture/cache, sans jamais mettre en cache une décision d’allergène périmée.
- **Paie SAP :** importer les employés et leur statut à partir du lot SOAP nocturne. Rendre visibles la date de dernière synchronisation et les rejets. Déduire uniquement pour un employé permanent confirmé ; produire un lot idempotent et rapprochable.
- **Allergènes :** ne jamais déduire une absence d’allergène d’une donnée manquante. Refuser la publication d’un plat incomplet ; conserver auteur, approbateur, horodatage et versions.
- **Loi 25 :** documenter les finalités et durées avant lancement, minimiser les renseignements, restreindre les accès, chiffrer en transit et au repos, journaliser les accès sensibles et prévoir suppression/export selon la politique approuvée.
- **Pilote Laval :** activer un seul site par configuration ; tester la paie, les remboursements, le QR, le plan de repli cuisine et les procédures en cas de panne avant l’ouverture aux trois sites.
