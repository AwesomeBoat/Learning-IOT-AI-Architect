# Étape 5/7 — Arborescence multi-capteurs (MicroPython)

*Voir `00_README_fil_rouge_micropython.md` à la racine du dossier pour le mode d'emploi complet.*

## Ce qui est nouveau à cette étape
Circuit complet (DHT22 + PIR + LDR). Chaque grandeur a son propre sous-topic :

```
formation/<PRENOM>/batiment/etage1/salle3/capteur/temperature
formation/<PRENOM>/batiment/etage1/salle3/capteur/humidite
formation/<PRENOM>/batiment/etage1/salle3/capteur/presence
formation/<PRENOM>/batiment/etage1/salle3/capteur/luminosite
```

**⚠️ Personnalisez `PRENOM` avant de lancer la simulation.**

## Lien avec la théorie / le planning
Wildcards MQTT `+` et `#` (Jour 2) — mêmes topics que la version Arduino, pour rester comparables.

## À essayer
- S'abonner à `.../capteur/temperature` seul, puis à `.../capteur/#` pour voir la différence.
- Déclencher le PIR (« Simulate Motion ») et observer le topic `presence` passer à `1`.
