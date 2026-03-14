# Phase 6.6 - Lisibilité Immédiate de la Fiche Mission

## Contexte de la phase

La fiche Mission disposait déjà d'un workflow sécurisé, d'une kanban stabilisée et d'un premier polissage UX. En pratique, une partie des informations critiques restait dépendante de l'onglet affiché à l'ouverture, ce qui ralentissait la lecture et compliquait la compréhension immédiate de la mission.

Cette phase vise à améliorer la lisibilité dès l'arrivée sur le formulaire, sans toucher à la logique métier existante ni tenter de forcer l'onglet actif en Python.

## Objectifs UX

- Voir les informations vitales immédiatement sous le titre de la mission
- Comprendre la mission sans changer d'onglet
- Faire ressortir l'action métier suivante dans le header
- Rendre plus explicites les champs calculés
- Améliorer la perception visuelle des états importants
- Donner un message d'erreur de clôture plus utile pour l'utilisateur

## Fichiers modifiés

- `addons/orne_interim_suite/views/mission_views.xml`
- `addons/orne_interim_suite/models/mission.py`
- `addons/orne_interim_suite/docs/PHASE6_6_MISSION_READABILITY.md`

## Choix effectués

### 1. Informations vitales hors onglets

Les champs clés ont été déplacés dans un bloc de synthèse visible juste sous le titre :

- `partner_id`
- `mission_type`
- `expected_workers`
- `date_start`
- `date_end`
- `state`

Ce choix répond directement au problème d'onglet actif : l'utilisateur n'a plus besoin d'arriver sur un onglet précis pour voir l'essentiel.

### 2. Description rendue plus lisible

La description de mission est sortie de la petite colonne initiale et affichée dans un bloc dédié sur toute la largeur, hors notebook. Le notebook reste présent pour le détail, mais ne concentre plus seul l'information utile.

### 3. Onglets recentrés sur leur rôle

- `Demande` : contexte métier et informations secondaires de la demande
- `Planification` : dates et durée calculée
- `Facturation` : taux horaire

L'objectif n'était pas de supprimer toute redondance, mais d'éviter que les onglets soient l'unique point d'accès aux données critiques.

### 4. Champ calculé plus explicite

`duration_days` reste strictement en readonly et est présenté sous le libellé `Durée calculée (jours)` avec une mention expliquant qu'il est déduit automatiquement des dates.

### 5. Hiérarchie visuelle des actions

Les actions de progression du workflow utilisent `oe_highlight` pour faire ressortir l'étape suivante :

- Qualifier
- Proposer
- Confirmer
- Démarrer
- Clôturer
- Marquer facturée

`Revenir` et `Annuler` restent visibles mais passent visuellement au second plan avec un style secondaire.

### 6. Repères visuels d'état

Les rubans ont été ajustés pour mieux distinguer les états :

- `ANNULÉE` : rouge
- `EN COURS` : bleu info
- `CLÔTURÉE` : fond sombre pour garantir le contraste
- `FACTURÉE` : vert

### 7. Mise en avant de la date de fin en cours de mission

Quand la mission est à l'état `in_progress`, un encart dédié met la date de fin en évidence hors notebook afin de rappeler immédiatement l'échéance métier qui conditionne la clôture.

### 8. Message d'erreur de clôture enrichi

Le refus de clôture prématurée conserve la règle métier existante mais affiche désormais la date de fin prévue au format `JJ/MM/AAAA`, afin que l'utilisateur sache immédiatement jusqu'à quand la mission doit rester ouverte.

## Tests manuels à faire

### 1. Lecture immédiate
- Ouvrir une mission et vérifier que client, type, effectif, dates et état sont visibles sans changer d'onglet

### 2. Description
- Vérifier que la description est lisible sur toute la largeur et reste éditable normalement

### 3. Workflow
- Parcourir le cycle `Reçue -> Qualifiée -> Proposée -> Confirmée -> En cours -> Clôturée -> Facturée`
- Vérifier que l'action suivante ressort visuellement à chaque étape

### 4. États visuels
- Contrôler l'affichage des rubans `ANNULÉE`, `EN COURS`, `CLÔTURÉE` et `FACTURÉE`
- Vérifier en particulier la lisibilité de `CLÔTURÉE`

### 5. Durée calculée
- Modifier `date_start` et `date_end`
- Vérifier que `duration_days` se recalcule et reste non modifiable

### 6. Clôture prématurée
- Tenter de clôturer une mission `En cours` avant `date_end`
- Vérifier que le message affiche bien la date de fin prévue

## Points restant éventuellement à améliorer

- Ajouter, si besoin après retour métier, une micro-aide textuelle sur les actions du workflow
- Réévaluer après usage réel le niveau de redondance entre synthèse et onglets
- Vérifier en situation réelle si une mise en avant supplémentaire de l'échéance est utile sur les missions longues
