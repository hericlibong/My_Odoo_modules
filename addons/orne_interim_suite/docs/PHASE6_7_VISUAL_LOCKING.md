# Phase 6.7 - Verrouillage Visuel et Cohérence Métier

## Contexte du lot

La fiche Mission disposait déjà d'un workflow par boutons, d'un champ `state` protégé en écriture et d'une kanban stabilisée. Il restait toutefois deux écarts à corriger :

- certaines transitions métiers acceptaient encore des missions trop incomplètes ou démarrées hors calendrier ;
- le formulaire ne montrait pas assez clairement quels champs devenaient figés quand la mission avançait dans le cycle.

Cette phase renforce l'existant sans refonte de workflow, sans toucher à la logique de chatter et sans rouvrir les démos.

## Objectif du lot

- Exiger un minimum de qualité avant la qualification
- Refuser explicitement un démarrage avant `date_start` ou après `date_end`
- Rendre le readonly visible dans le formulaire selon l'état
- Consolider `invoiced` comme état terminal
- Finaliser les trois retouches UX résiduelles de la fiche mission

## Fichiers modifiés

- `addons/orne_interim_suite/models/mission.py`
- `addons/orne_interim_suite/views/mission_views.xml`
- `addons/orne_interim_suite/docs/PHASE6_7_VISUAL_LOCKING.md`

## Logique métier ajoutée

### 1. Qualification plus stricte

`action_qualify()` délègue désormais les contrôles à une vérification dédiée. La qualification est refusée si :

- le client est absent ;
- `date_start` ou `date_end` manque ;
- `date_end < date_start` ;
- `expected_workers < 1` ;
- la description est vide ou trop légère après nettoyage des espaces.

Les messages d'erreur restent courts et orientés utilisateur.

### 2. Démarrage cohérent avec le calendrier

`action_start()` refuse maintenant deux cas explicites :

- mission trop tôt : démarrage refusé tant que la date du jour est antérieure à `date_start` ;
- mission trop tard : démarrage refusé si la date du jour est postérieure à `date_end`.

Les messages affichent la date utile au format utilisateur via `format_date`.

### 3. Garde-fou léger sur les éditions en états avancés

Le `write()` conserve l'interdiction de modifier `state` manuellement et ajoute un verrou léger sur les champs métier principaux :

- à partir de `in_progress` : `partner_id`, `mission_type`, `expected_workers`, `description`, `date_start`, `date_end` ;
- en `invoiced` et `cancelled` : ajout du verrou sur `hourly_rate`.

Cela évite des modifications directes incohérentes hors interface, tout en laissant le workflow existant fonctionner par contexte.

### 4. Fin de cycle consolidée

Le comportement terminal de `invoiced` reste strict :

- pas de bouton de retour ;
- pas d'annulation ;
- pas de réactivation.

`closed` reste le dernier état opérationnel réversible, conformément au comportement déjà en place.

## Logique readonly par état dans la vue

Le formulaire expose maintenant visuellement le verrouillage avec des `attrs` simples :

- `state` reste non éditable manuellement ;
- dès `in_progress`, les champs `partner_id`, `mission_type`, `expected_workers`, `description`, `date_start`, `date_end` passent visiblement en readonly ;
- `cancel_reason` n'apparaît et n'est éditable que si `state == cancelled` ;
- `hourly_rate` conserve sa restriction de groupes et devient readonly en `invoiced` et `cancelled`.

Le résultat recherché est volontairement sobre :

- mission avancée : formulaire figé sur les données structurantes ;
- mission terminale : quasi figée, hors lecture et chatter.

## Impacts UX

### 1. Redondance réduite

L'ancien bloc très répétitif de contexte est allégé. L'onglet `Demande` ne conserve qu'un rappel sobre et le champ d'annulation si nécessaire.

### 2. Durée calculée plus claire

Le champ `duration_days` garde son readonly mais son libellé et son texte d'aide sont mieux espacés et plus explicites.

### 3. Encart bleu plus propre

L'encart d'état `En cours` utilise désormais une formulation plus propre :

`Date de fin à surveiller : <date>`

L'espacement a été revu pour éviter l'effet visuel tassé.

## Points de test manuels dans Odoo

### Qualification

- créer une mission `received` sans client et vérifier le refus de qualification ;
- créer une mission `received` sans dates et vérifier le refus ;
- saisir `expected_workers = 0` et vérifier le refus ;
- laisser une description vide ou quasi vide et vérifier le refus ;
- compléter correctement la mission et vérifier le passage à `qualified`.

### Démarrage

- créer une mission `confirmed` avec `date_start` future et vérifier le refus avec affichage de la date prévue ;
- créer une mission `confirmed` avec `date_end` passée et vérifier le refus avec affichage de la date utile ;
- créer une mission `confirmed` dont la date du jour est comprise dans l'intervalle et vérifier le passage à `in_progress`.

### Verrouillage visuel

- ouvrir une mission `in_progress` et vérifier que les champs structurants apparaissent grisés / readonly ;
- ouvrir une mission `closed` et vérifier que ces mêmes champs restent figés ;
- ouvrir une mission `invoiced` et vérifier que `hourly_rate` est aussi readonly ;
- ouvrir une mission `cancelled` et vérifier que `cancel_reason` est visible et éditable, mais pas les champs structurants.

### Fin de cycle

- vérifier qu'aucun retour arrière n'est possible depuis `invoiced` ;
- vérifier qu'aucune annulation n'est possible depuis `invoiced` ;
- vérifier que `closed` peut encore revenir à `in_progress` si le bouton était déjà prévu pour ce cas.

### Contrôles de vue

- ouvrir le formulaire mission sans erreur XML ;
- vérifier que la kanban reste inchangée ;
- vérifier que le chatter et le tracking restent présents ;
- vérifier que la restriction de groupes sur `hourly_rate` est toujours appliquée.
