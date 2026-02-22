# Cadrage Projet : Orne Interim Suite

## Intitulé
**Orne Interim Suite** — Solution ERP/CRM pour agences d'intérim spécialisées BTP & Nettoyage

## Résumé (10 lignes)
Module Odoo sur-mesure pour centraliser la gestion des missions d'intérim :
1. Capture des demandes clients en 1 écran unique
2. Pipeline visuel de qualification → facturation
3. Génération automatique de devis depuis les demandes
4. Affectation multiple d'intérimaires par mission
5. Contrôle simplifié de conformité documentaire
6. Saisie des heures par jour/personne
7. Facturation automatique (heures ou forfait)
8. Intégration native avec Contacts, CRM et Facturation Odoo
9. Interface optimisée pour un workflow en 10 minutes
10. Conçu pour les PME locales (simplicité > complexité)

## Scénario Démo (7 étapes)
1. **Création demande** : Formulaire unique avec client, type (BTP/Nettoyage), période, besoins
2. **Pipeline** : Glisser-déposer entre états (Reçue → Qualifiée → Proposée → Confirmée → En cours → Clôturée → Facturée)
3. **Devis 1-clic** : Bouton "Générer devis" pré-rempli depuis la demande
4. **Affectation** : Sélection multiple d'intérimaires avec indicateur de conformité (🟢/🟡/🔴)
5. **Contrôle docs** : Vue kanban des intérimaires avec statut documentaire
6. **Saisie heures** : Grille hebdomadaire par intérimaire
7. **Facturation** : Bouton "Générer facture" avec calcul automatique

## MVP (5 fonctionnalités clés)
1. **Modèle "Demande de Mission"**
   - Champs : Client, Type (BTP/Nettoyage), Période, Nb personnes, Tarif, Description
   - Workflow 7 états + kanban coloré

2. **Intégration CRM/Ventes**
   - Bouton "Créer devis" → génère une opportunité CRM + devis pré-rempli
   - Lien automatique avec le contact client

3. **Gestion Intérimaires**
   - Modèle simplifié : Nom, Compétences, Documents (3 types max), Dates validité
   - Vue "Disponibilité" avec filtre par compétences

4. **Affectation & Suivi**
   - Relation N-N entre Mission et Intérimaires
   - Grille de saisie heures (jour/semaine)
   - Indicateur visuel de conformité

5. **Facturation Automatique**
   - Bouton "Générer facture" → crée une facture Odoo avec :
     - Lignes pré-remplies (heures × tarif ou forfait)
     - Lien vers la mission et le devis

## Tâches par Phases

### Phase 1 : Cadrage (2j)
- [ ] Définir les modèles de données (ERD simple)
- [ ] Lister les champs obligatoires vs optionnels
- [ ] Designer le workflow des états
- [ ] Identifier les points d'intégration Odoo standard

### Phase 2 : Modèles (3j)
- [ ] Créer `interim.mission` (demande principale)
- [ ] Créer `interim.worker` (intérimaires)
- [ ] Créer `interim.document` (documents)
- [ ] Ajouter champs calculés (heures totales, statut conformité)
- [ ] Implémenter le workflow

### Phase 3 : Vues & UI (4j)
- [ ] Formulaire "Demande de mission" (1 écran)
- [ ] Vue Kanban du pipeline
- [ ] Vue liste des intérimaires avec indicateurs
- [ ] Grille de saisie des heures
- [ ] Boutons d'action (Devis, Facture)

### Phase 4 : Automatisations (3j)
- [ ] Bouton "Générer devis" → création opportunité CRM
- [ ] Bouton "Générer facture" → calcul automatique
- [ ] Calcul du statut de conformité
- [ ] Mise à jour automatique des heures totales

### Phase 5 : Sécurité & Données (2j)
- [ ] Groups : Manager, Commercial, Administratif
- [ ] Règles d'accès (ex: seul Manager voit les tarifs)
- [ ] Données de démo (3 clients, 5 intérimaires, 2 missions)
- [ ] Menu principal "Intérim"

### Phase 6 : Tests & Validation (2j)
- [ ] Test du scénario complet
- [ ] Vérification des intégrations CRM/Facturation
- [ ] Validation des calculs (heures, montants)
- [ ] Documentation minimale (README + capture workflow)

## Livrables Attendus
1. **Module installable** :
   - Dossier `orne_interim_suite/` complet
   - `__manifest__.py` avec dépendances (`crm`, `sale`, `account`)
   - Tous les modèles, vues et sécurité

2. **Données de démo** :
   - Fichier `data/demo.xml` avec :
     - 3 entreprises clientes (2 BTP, 1 Nettoyage)
     - 5 intérimaires (documents variés)
     - 2 missions en cours (1 BTP, 1 Nettoyage)
     - 1 mission clôturée avec facture

3. **Documentation** :
   - `README.md` avec :
     - Installation
     - Scénario de démo pas-à-pas
     - Capture d'écran du pipeline
     - Limites connues (MVP)

4. **Tests basiques** (optionnel) :
   - Vérification des calculs de facturation
   - Validation du workflow

## Critères d'Acceptation
✅ **Fonctionnel** :
- Le scénario de 7 étapes s'exécute sans erreur
- Temps de démo < 10 minutes
- Pas de ressaisie entre étapes

✅ **Technique** :
- Module s'installe sans erreur
- Intégration CRM/Ventes/Facturation fonctionnelle
- Performances acceptables (<2s par action)

✅ **UX** :
- Pipeline visuel et intuitif
- Indicateurs de conformité clairs (couleurs)
- Boutons d'action bien placés

✅ **Qualité** :
- Code commenté (docstrings sur modèles)
- Nommage cohérent (ex: `interim_` prefix)
- Pas de warnings à l'installation

## Risques & Options

### Risques Identifiés
1. **Suivi des heures** :
   - *Risque* : Module `hr_timesheet` limité en Community
   - *Option 1* : Grille custom simple (MVP)
   - *Option 2* : Utiliser `project` + tâches (plus standard)

2. **Documents intérimaires** :
   - *Risque* : Gestion complexe des validités
   - *Solution* : 3 types max (CACES, Médical, Formation) + champs date

3. **Facturation** :
   - *Risque* : Calculs différents BTP vs Nettoyage
   - *Solution* : Champ "Type de facturation" (Heures/Forfait) + règles métiers simples

4. **Dépendances** :
   - *Risque* : Modules `sale` et `account` requis
   - *Solution* : Vérifier dans `__manifest__.py` + message d'erreur clair

### Options d'Évolution
- **V1.1** : Ajout de rapports (CA par client, taux de remplissage)
- **V1.2** : Intégration avec module Paie (si disponible)
- **V1.3** : Mobile : saisie heures via app (hors scope MVP)

## Structure du Module Proposée
```
orne_interim_suite/
├── __init__.py
├── __manifest__.py          # dépends: ['base', 'crm', 'sale', 'account']
├── models/
│   ├── __init__.py
│   ├── mission.py           # Demande de mission (core)
│   ├── worker.py            # Intérimaires
│   ├── document.py          # Documents
│   └── res_partner.py       # Extension pour champs spécifiques clients
├── views/
│   ├── mission_views.xml    # Formulaire + kanban pipeline
│   ├── worker_views.xml     # Liste intérimaires + conformité
│   ├── document_views.xml   # Gestion documents
│   └── menus.xml            # Menu principal
├── security/
│   ├── ir.model.access.csv  # Permissions
│   └── security_groups.xml  # Groups (Manager, Commercial...)
├── data/
│   ├── demo.xml             # Données de démo
│   └── sequences.xml        # Séquences (numéros missions)
└── README.md                # Documentation
```

## Prochaines Étapes Recommandées
1. **Valider le cadrage** avec le client (priorités MVP)
2. **Créer le manifest** avec les dépendances
3. **Implémenter les modèles** dans l'ordre : Mission → Worker → Document
4. **Prototyper les vues** avec des maquettes simples