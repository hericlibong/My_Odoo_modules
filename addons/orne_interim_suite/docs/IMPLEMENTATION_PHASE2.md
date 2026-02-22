# Implémentation Phase 2 - Modèle Principal Mission

## Fichiers Modifiés/Créés

### 1. `__manifest__.py`
**Chemin** : `addons/orne_interim_suite/__manifest__.py`

**Contenu** :
```python
{ 
    'name': 'Orne Interim Suite', 
    'version': '1.0', 
    'summary': 'Gestion des missions d\'intérim pour agences locales', 
    'description': '''Module de gestion des demandes de mission pour agences d\'intérim spécialisées BTP et Nettoyage.''', 
    'author': 'AC', 
    'website': 'https://github.com/hericlibong/My_Odoo_modules', 
    'category': 'Human Resources', 
    'depends': ['base'],  # Dépendances minimales pour le MVP
    'data': [
        'data/sequences.xml',
    ],  # Séquence pour la génération automatique des références
    'demo': [],  # Pas de données demo pour cette phase
    'installable': True, 
    'application': True, 
    'auto_install': False, 
    'license': 'LGPL-3',
}
```

**Points clés** :
- Dépendance minimale (`base` uniquement) pour respecter les contraintes
- Ajout de `data/sequences.xml` pour la séquence de référence
- Pas de dépendances à `crm`, `sale` ou `account` à ce stade
- Module marqué comme `application` pour apparition dans le menu Apps

---

### 2. `models/mission.py`
**Chemin** : `addons/orne_interim_suite/models/mission.py`

**Contenu** :
```python
from odoo import models, fields, api

class OrneInterimMission(models.Model):
    _name = 'orne_interim.mission'
    _description = 'Demande de mission d\'intérim'
    
    # Champs de base
    name = fields.Char(string='Référence', required=True, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Client', required=True, help='Entreprise cliente')
    
    # Type de mission
    mission_type = fields.Selection([
        ('btp', 'BTP'),
        ('nettoyage', 'Nettoyage/Tertiaire')
    ], string='Type de mission', required=True, default='btp')
    
    # Période
    date_start = fields.Date(string='Date de début', required=True)
    date_end = fields.Date(string='Date de fin', required=True)
    
    # Détails de la demande
    expected_workers = fields.Integer(string='Nombre de personnes', required=True, default=1)
    description = fields.Text(string='Description des besoins')
    
    # Workflow
    state = fields.Selection([
        ('received', 'Reçue'),
        ('qualified', 'Qualifiée'),
        ('proposed', 'Proposée'),
        ('confirmed', 'Confirmée'),
        ('in_progress', 'En cours'),
        ('closed', 'Clôturée'),
        ('invoiced', 'Facturée')
    ], string='État', default='received', required=True)
    
    # Détails de la demande (suite)
    hourly_rate = fields.Float(string='Taux horaire', digits=(16, 2), help='Taux horaire facturé au client')
    
    # Champs calculés
    duration_days = fields.Integer(string='Durée (jours)', compute='_compute_duration', store=True)
    
    @api.depends('date_start', 'date_end')
    def _compute_duration(self):
        for record in self:
            if record.date_start and record.date_end:
                delta = fields.Date.from_string(record.date_end) - fields.Date.from_string(record.date_start)
                record.duration_days = delta.days + 1  # Inclusif
            else:
                record.duration_days = 0
    
    # Séquence automatique
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('orne.interim.mission') or '/'
        return super(OrneInterimMission, self).create(vals)
```

**Points clés** :
- **Nommage** : Préfixe `orne_interim.` conforme aux règles
- **Champs** :
  - `partner_id` : Lien vers client (res.partner existant)
  - `mission_type` : BTP ou Nettoyage/Tertiaire
  - `date_start`/`date_end` : Période de mission
  - `expected_workers` : Nombre de personnes demandées
  - `hourly_rate` : Tarif horaire avec `digits=(16, 2)` (compatible base)
  - `state` : Workflow complet 7 états (sans tracking pour compatibilité)
- **Calculs** :
  - `duration_days` : Durée automatique en jours
  - Génération automatique de référence via séquence `orne.interim.mission`
- **Compatibilité** : Pas de dépendance à `mail` ou `product`

---

### 3. Fichiers d'import (`__init__.py`)

#### `addons/orne_interim_suite/__init__.py`
```python
from . import models
```

#### `addons/orne_interim_suite/models/__init__.py`
```python
from . import mission
```

**Rôle** : Permettre à Odoo de charger le modèle lors de l'installation

---

## Décisions Techniques

### 1. Intégrimaires (res.partner)
**Décision** : Pas implémenté dans cette phase (conforme aux règles)
**Préparation** : Champ `partner_id` déjà présent pour le lien futur

### 2. Flux Vente
**Décision** : Pas d'intégration `sale.order` ou `crm.lead` dans cette phase
**Préparation** : Champ `hourly_rate` disponible pour calculs futurs

### 3. Heures
**Décision** : Pas de modèle custom dans cette phase
**Préparation** : Champ `expected_workers` pour estimer le volume

### 4. Séquence
**Implémentation** : Génération automatique de référence via `ir.sequence`
**Fichier** : `data/sequences.xml` créé avec code `orne.interim.mission`
**Format** : `MIS-0001`, `MIS-0002`, etc.

### 5. Compatibilité Base
**Corrections appliquées** :
- Retiré `tracking=True` sur le champ `state` (évite dépendance à `mail`)
- Remplacé `digits='Product Price'` par `digits=(16, 2)` (évite dépendance à `product`)

---

## Validation

### Module Installable
Le module est conçu pour être installable immédiatement avec :
- Dépendance `base` uniquement
- Fichier XML de séquence inclus
- Structure minimale valide

### Tests Manuels Recommandés
1. Installer le module (la séquence est créée automatiquement)
2. Créer une mission via l'interface technique (Menu Développeur > Modèles)
3. Vérifier la génération automatique de la référence (format `MIS-0001`)
4. Tester le calcul de la durée
5. Vérifier les transitions d'état (sans tracking)

---

## Prochaines Étapes (Phase 3)
- [ ] Créer la séquence `orne.interim.mission`
- [ ] Ajouter les vues (formulaire, kanban)
- [ ] Implémenter les boutons d'action pour changer d'état
- [ ] Préparer l'intégration future avec `res.partner` pour les intérimaires

---

## Notes
- **Pas de vues** : Conforme à la demande (pas d'UI dans cette phase)
- **Pas de sécurité** : Pas de CSV ou groupes dans cette phase
- **Pas de données demo** : Conforme à la demande
- **Respect des règles** :
  - Préfixe `orne_interim.` utilisé
  - Pas de modèle worker créé
  - Pas d'intégration sale/crm
  - Pas de dépendance à hr_timesheet
  - Compatibilité stricte avec `base` uniquement

## Fichiers Livrés (Phase 2 + Corrections)
```
orne_interim_suite/
├── __init__.py
├── __manifest__.py            # Avec data/sequences.xml
├── models/
│   ├── __init__.py
│   └── mission.py             # Sans tracking, avec digits=(16,2)
├── data/
│   └── sequences.xml          # NOUVEAU : séquence MIS-XXXX
└── docs/
    └── IMPLEMENTATION_PHASE2.md  # Mis à jour
```