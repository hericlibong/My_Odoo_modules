# Phase 5.1 - Règles Strictes & Désactivation Démo

## Décision : Désactivation des Données de Démo

### Pourquoi ?
- Incohérences visibles (références dupliquées, dates/statuts incohérents)
- Besoin de tester en conditions réelles avec création manuelle
- Validation des règles strictes avant réintroduction des démos

### Modifications

#### 1. Manifest (`__manifest__.py`)
```python
'demo': [],  # DÉMO DÉSACTIVÉE - Tests en création manuelle uniquement
```

#### 2. Fichier demo.xml
- Contenu commenté et conservé pour référence
- En-tête explicite avec procédure de réactivation
- À réactiver uniquement après validation complète

## Règles Strictes Dates ↔ Statut

### 1. Règle Absolue (dans `@api.constrains`)
```python
@api.constrains('date_start', 'date_end')
def _check_dates(self):
    # Toujours : date_end >= date_start
    if record.date_end < record.date_start:
        raise ValidationError("La date de fin doit être postérieure ou égale à la date de début.")
```
**Note** : Pas de comparaison avec `today()` pour éviter les erreurs futures sur write()

### 2. Règles Contextuelles (dans les méthodes de transition)

**Démarrage (→ in_progress)** :
```python
today = fields.Date.context_today(self)
if today > rec.date_end:
    raise UserError("On ne peut pas démarrer une mission dont la date de fin est déjà dépassée.")
```

**Clôture (→ closed)** :
```python
if today < rec.date_end:
    raise UserError("Impossible de clôturer une mission qui n'est pas encore terminée dans le temps.")
```

**Facturation (→ invoiced)** :
```python
if today < rec.date_end:
    raise UserError("Impossible de facturer une mission qui n'est pas encore terminée dans le temps.")
```

**Note** : Utilisation de `context_today()` pour éviter les problèmes de timezone

## Sécurité des Références

### Séquence (`data/sequences.xml`)
```xml
<odoo noupdate="1">
    <!-- number_next non forcé pour éviter les régressions -->
</odoo>
```

**Garanties** :
- `noupdate="1"` : Pas de réinitialisation à l'upgrade
- Pas de `number_next` forcé : Conservation du compteur actuel
- Génération automatique dans `create()` si name == '/'

## Tests Manuels Recommandés

### 1. Création Valide
```
- Créer une mission avec date_start <= date_end
- Vérifier la référence automatique (MIS-XXXX)
- Calcul de duration_days correct
```

### 2. Invalide (doit échouer)
```
- date_end < date_start → ValidationError
- Démarrer une mission avec date_end passée → UserError
- Clôturer avant date_end → UserError
```

### 3. Transitions
```
- Créer une mission (state=received)
- Qualifier → Proposer → Confirmer → Démarrer (vérifier blocage si date_end passée)
- Clôturer (vérifier blocage si today < date_end)
- Annuler → Réactiver
```

## Commande d'Upgrade
```bash
docker-compose exec odoo odoo -u orne_interim_suite -d <votre_base> --stop-after-init
```

## Prochaines Étapes
- Tests exhaustifs des règles dates/statuts
- Validation du workflow complet
- Réintroduction des démos uniquement après stabilisation