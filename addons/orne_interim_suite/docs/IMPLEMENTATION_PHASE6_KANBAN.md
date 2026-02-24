# Phase 6 - Vue Kanban & Transitions Sécurisées

## Vue Kanban

### Implémentation
- Vue Kanban ajoutée dans `mission_views.xml`
- Groupement par état (`default_group_by="state"`)
- Drag & drop désactivé (`records_draggable="0"`)
- Affichage des informations clés :
  - Référence (name) en gras
  - Client (partner_id)
  - Type (badge BTP/Nettoyage)
  - Période (date_start → date_end)
  - Nombre de personnes (expected_workers)

### Intégration
- Kanban comme première vue (`view_mode="kanban,tree,form"`)
- Conservation de la search view existante
- Pas de modification des menus

## Sécurité des Transitions

### Protection du write()
```python
def write(self, vals):
    if 'state' in vals and not self.env.context.get('allow_state_write'):
        raise UserError("Changement d’état manuel non autorisé. Veuillez utiliser les boutons du workflow.")
    return super().write(vals)
```

### Méthodes de Transition
Toutes les méthodes `action_*` utilisent maintenant :
```python
self.with_context(allow_state_write=True).write({'state': 'nouveau_statut'})
```

## Tests Manuels

### 1. Vue Kanban
- Créer une mission via le formulaire
- Vérifier qu'elle apparaît dans la colonne "Reçues"
- Tester les filtres (Reçues, En cours, etc.)

### 2. Transitions Sécurisées
- Qualifier la mission via le bouton
- Vérifier qu'elle passe dans la colonne "Qualifiées"
- Essayer de modifier manuellement l'état via le formulaire → doit bloquer avec UserError

### 3. Workflow Complet
- Créer → Qualifier → Proposer → Confirmer → Démarrer → Clôturer
- Vérifier que chaque transition fonctionne
- Vérifier que les règles de dates sont toujours appliquées

## Commande d'Upgrade
```bash
docker-compose exec odoo odoo -u orne_interim_suite -d <votre_base> --stop-after-init
```