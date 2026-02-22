# Implémentation Phase 3 - Interface Utilisateur Minimale

## Objectif
Rendre le modèle `orne_interim.mission` utilisable dans l'interface standard Odoo (MVP), sans workflow avancé ni boutons métiers.

## Fichiers Créés/Modifiés

### 1. `views/mission_views.xml` (NOUVEAU)
**Chemin** : `addons/orne_interim_suite/views/mission_views.xml`

**Contenu complet** :
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Action Window -->
    <record id="action_orne_interim_mission" model="ir.actions.act_window">
        <field name="name">Missions d'intérim</field>
        <field name="res_model">orne_interim.mission</field>
        <field name="view_mode">tree,form</field>
        <field name="search_view_id" ref="view_orne_interim_mission_search"/>
    </record>

    <!-- Tree View -->
    <record id="view_orne_interim_mission_tree" model="ir.ui.view">
        <field name="name">orne.interim.mission.tree</field>
        <field name="model">orne_interim.mission</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name"/>
                <field name="partner_id"/>
                <field name="mission_type"/>
                <field name="date_start"/>
                <field name="date_end"/>
                <field name="expected_workers"/>
                <field name="hourly_rate"/>
                <field name="state"/>
                <field name="duration_days"/>
            </tree>
        </field>
    </record>

    <!-- Form View -->
    <record id="view_orne_interim_mission_form" model="ir.ui.view">
        <field name="name">orne.interim.mission.form</field>
        <field name="model">orne_interim.mission</field>
        <field name="arch" type="xml">
            <form>
                <header>
                    <field name="state" widget="statusbar"/>
                </header>
                <sheet>
                    <group>
                        <field name="name" readonly="1"/>
                        <field name="partner_id"/>
                        <field name="mission_type"/>
                        <field name="date_start"/>
                        <field name="date_end"/>
                        <field name="expected_workers"/>
                        <field name="hourly_rate"/>
                        <field name="duration_days" readonly="1"/>
                        <field name="description"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <!-- Search View -->
    <record id="view_orne_interim_mission_search" model="ir.ui.view">
        <field name="name">orne.interim.mission.search</field>
        <field name="model">orne_interim.mission</field>
        <field name="arch" type="xml">
            <search>
                <field name="state" string="État"/>
                <field name="mission_type" string="Type de mission"/>
                <field name="partner_id" string="Client"/>
                <filter name="filter_received" string="Reçues" domain="[('state','=','received')]"/>
                <filter name="filter_in_progress" string="En cours" domain="[('state','=','in_progress')]"/>
                <filter name="filter_closed" string="Clôturées" domain="[('state','=','closed')]"/>
                <group expand="0" string="Grouper par">
                    <filter name="group_by_state" string="État" context="{'group_by':'state'}"/>
                    <filter name="group_by_type" string="Type" context="{'group_by':'mission_type'}"/>
                    <filter name="group_by_partner" string="Client" context="{'group_by':'partner_id'}"/>
                </group>
            </search>
        </field>
    </record>
</odoo>
```

**Composants** :
- **Action Window** (`action_orne_interim_mission`) : Point d'entrée pour ouvrir les missions
- **Tree View** : Liste avec toutes les colonnes demandées
- **Form View** :
  - `name` en readonly
  - `state` affiché en statusbar (pas de boutons)
  - `duration_days` en readonly
  - Tous les autres champs éditables
- **Search View** :
  - Filtres rapides par état
  - Groupement par état/type/client

---

### 2. `views/menus.xml` (NOUVEAU)
**Chemin** : `addons/orne_interim_suite/views/menus.xml`

**Contenu complet** :
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Menu Top-Level -->
    <menuitem id="menu_orne_interim_root" name="Intérim" sequence="10"/>

    <!-- Sous-menu Missions -->
    <menuitem id="menu_orne_interim_mission" name="Missions" parent="menu_orne_interim_root"
              action="action_orne_interim_mission" sequence="10"/>
</odoo>
```

**Structure** :
- Menu racine "Intérim" (top-level)
- Sous-menu "Missions" pointant vers l'action `action_orne_interim_mission`

---

### 3. `__manifest__.py` (MIS À JOUR)
**Chemin** : `addons/orne_interim_suite/__manifest__.py`

**Modification** : Ajout des vues dans la clé `data` (ordre critique respecté)
```python
'data': [
    'security/ir.model.access.csv',
    'data/sequences.xml',
    'views/mission_views.xml',
    'views/menus.xml',
],  # Accès + séquence + vues + menus
```

---

## Décisions Techniques

### 1. Architecture des Vues
**Choix** : Tout dans `mission_views.xml` (action + vues)
**Raison** : Centralisation logique pour un modèle unique

### 2. Statusbar
**Implémentation** :
```xml
<header>
    <field name="state" widget="statusbar"/>
</header>
```
**Effet** : Affichage visuel de l'état sans boutons d'action (conforme au périmètre)

### 3. Search View
**Fonctionnalités** :
- Filtres prédéfinis pour les états courants
- Groupement par les 3 dimensions principales
- Pas de filtres complexes (MVP)

### 4. Ordre des Données
**Ordre critique** :
1. `security/ir.model.access.csv` (d'abord pour les permissions)
2. `data/sequences.xml` (ensuite pour les données)
3. `views/mission_views.xml` (puis les vues qui référencent les données)
4. `views/menus.xml` (enfin les menus qui pointent vers les actions)

---

## Validation

### Tests Recommandés
1. **Installation** :
   - Vérifier que le module s'installe sans erreur
   - Vérifier que le menu "Intérim > Missions" apparaît

2. **Création** :
   - Créer une mission via le formulaire
   - Vérifier la génération automatique de la référence (MIS-XXXX)
   - Vérifier que `duration_days` se calcule automatiquement

3. **Liste** :
   - Vérifier que toutes les colonnes s'affichent
   - Tester les filtres (Reçues, En cours, Clôturées)
   - Tester le groupement

4. **Édition** :
   - Modifier une mission et vérifier que `duration_days` se recalcule
   - Vérifier que `name` reste en readonly

5. **Sécurité** :
   - Vérifier qu'un utilisateur standard peut créer/modifier/supprimer

---

## Points Clés

✅ **Conformité au périmètre** :
- Pas de workflow avancé
- Pas de boutons métiers
- Pas de Kanban
- Pas de nouveaux modèles

✅ **Intégration standard** :
- Utilisation des widgets Odoo standards (`statusbar`)
- Respect des conventions de nommage
- Structure modulaire

✅ **Prêt pour la suite** :
- Les vues sont prêtes pour l'ajout futur des boutons d'action
- Le menu est positionné pour ajouter d'autres sous-menus

---

## Structure Finale
```
orne_interim_suite/
├── __init__.py
├── __manifest__.py            # Mis à jour avec vues + menus
├── models/
│   ├── __init__.py
│   └── mission.py             # Inchangé
├── views/
│   ├── mission_views.xml      # NOUVEAU : vues + action
│   └── menus.xml              # NOUVEAU : menus
├── security/
│   └── ir.model.access.csv    # Inchangé
├── data/
│   └── sequences.xml          # Inchangé
└── docs/
    ├── IMPLEMENTATION_PHASE2.md
    └── IMPLEMENTATION_PHASE3_UI.md  # Ce fichier
```

---

## Prochaine Phase
- Ajout des boutons d'action pour changer d'état
- Intégration avec res.partner pour les intérimaires
- Ajout des vues Kanban pour le pipeline visuel