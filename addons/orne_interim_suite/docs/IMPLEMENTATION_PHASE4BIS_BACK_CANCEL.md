# Phase 4bis - Retour et Annulation

## Modifications

### Modèle (mission.py)
- Ajout état 'cancelled' dans le workflow
- Champ `cancel_reason` (Text) pour documenter les annulations
- 3 nouvelles méthodes :
  - `action_back_step()` : retour d'un cran (mapping qualifié → reçu, etc.)
  - `action_cancel()` : passage à état 'cancelled'
  - `action_reactivate()` : réactivation (cancelled → received)

### Vue (mission_views.xml)
- Boutons ajoutés dans header :
  - "Revenir" (btn-secondary) visible pour qualified/proposed/confirmed/in_progress/closed
  - "Annuler" (btn-danger) visible pour tous états sauf cancelled/invoiced
  - "Réactiver" (btn-success) visible uniquement pour cancelled
- Champ `cancel_reason` visible uniquement quand state=cancelled
- Filtre "Annulées" ajouté dans la search view

## Règles
- Retour interdit depuis received/cancelled/invoiced
- Annulation interdite pour les missions facturées
- Réactivation vide le champ cancel_reason

## Intégration
- Pas de nouvelles dépendances (toujours depends=['base'])
- Pas de modification des menus ou du manifest
- Compatible avec le workflow existant