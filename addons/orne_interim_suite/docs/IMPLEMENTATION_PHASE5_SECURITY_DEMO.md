# Phase 5 - Sécurité & Données de Démo

## Sécurité

### Groupes (security_groups.xml)
3 groupes créés avec droits différenciés :
- **Manager** : CRUD complet + accès au tarif horaire
- **Commercial** : CRU (pas de suppression) + pas d'accès au tarif
- **Administratif** : RU seulement + accès au tarif

### Accès (ir.model.access.csv)
Remplacement de l'accès générique par des règles granulaires :
- Manager : 1,1,1,1
- Commercial : 1,1,1,0
- Administratif : 1,1,0,0

### Protection des données
Champ `hourly_rate` restreint aux groupes Manager et Administratif via `groups="..."`

## Données de Démo (demo.xml)
- 3 clients (2 BTP + 1 Nettoyage) avec coordonnées réalistes
- 3 missions dans différents états (received/qualified/in_progress)
- Données localisées (Orne, France) pour crédibilité

## Intégration
- Ordre des fichiers respecté pour éviter les références forward
- Demo.xml dans la clé 'demo' pour installation optionnelle
- Module reste base-only (depends=['base'])