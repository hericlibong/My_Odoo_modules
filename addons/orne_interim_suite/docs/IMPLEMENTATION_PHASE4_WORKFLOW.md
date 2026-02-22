# Phase 4 - Workflow Utilisable

## Modifications

### models/mission.py
Ajout de 6 méthodes de transition (type="object") :
- `action_qualify()` : received → qualified (avec validation des champs obligatoires)
- `action_propose()` : qualified → proposed
- `action_confirm()` : proposed → confirmed
- `action_start()` : confirmed → in_progress
- `action_close()` : in_progress → closed
- `action_invoice_mark()` : closed → invoiced

Chaque méthode :
- Fonctionne en multi-record (for rec in self)
- Vérifie l'état courant (UserError si invalide)
- Valide les prérequis pour la première transition (qualify)

### views/mission_views.xml
Ajout dans le header du formulaire :
- 6 boutons type="object" correspondant aux méthodes
- Chaque bouton visible uniquement pour l'état pertinent (states="...")
- Statusbar non cliquable (statusbar_clickable="false")
- Boutons en btn-primary pour visibilité

## Corrections Post-Implémentation

### 1. Import UserError
**Problème** : Les méthodes utilisaient `UserError` sans import
**Correction** : Ajout de `from odoo.exceptions import UserError`
**Impact** : Évite NameError lors des transitions d'état

### 2. Champ hourly_rate
**Problème** :
- Déclaration dupliquée (digits='Product Price' puis digits=(16,2))
- `digits='Product Price'` crée une dépendance implicite au module `product`
**Correction** :
- Suppression de la première déclaration
- Conservation unique avec `digits=(16, 2)` pour compatibilité base-only
**Impact** : Module reste strictement compatible avec `depends=['base']`

### 3. Optimisation _compute_duration
**Problème** : `fields.Date.from_string()` inutile sur des champs déjà de type Date
**Correction** : Simplification en `(date_end - date_start).days + 1`
**Impact** : Code plus propre sans changement fonctionnel

## Résumé
Workflow maintenant utilisable via l'UI existante, sans nouvelles dépendances, en respectant les contraintes initiales. Toutes les corrections garantissent la compatibilité base-only et évitent les erreurs d'exécution.