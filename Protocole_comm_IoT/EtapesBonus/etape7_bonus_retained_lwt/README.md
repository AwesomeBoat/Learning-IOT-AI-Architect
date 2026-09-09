# Étape 7/7 (BONUS) — Retained + Last Will and Testament (MicroPython)

*Voir `00_README_fil_rouge_micropython.md` à la racine du dossier pour le mode d'emploi complet.*

## Ce qui est nouveau à cette étape
Circuit DHT22 seul. Un Last Will and Testament est configuré via `client.set_last_will(topic, "hors-ligne", retain=True, qos=1)` **avant** `client.connect()`. À la connexion, on publie nous-mêmes `"en-ligne"` (retained) sur le même topic `.../status`.

**⚠️ Personnalisez `PRENOM` avant de lancer la simulation.**

## Différence avec la version Arduino/C++
`umqtt.simple` expose `set_last_will()` comme méthode dédiée (à appeler avant `connect()`), équivalent à la signature étendue `connect(id, topicLWT, qos, retain, message)` de PubSubClient côté Arduino.

## À essayer (la démo la plus parlante du fil rouge)
1. Lancez la simulation, vérifiez sur MQTTX Web que `.../status` passe à `en-ligne`.
2. **Arrêtez brutalement** la simulation (bouton Stop).
3. Observez `.../status` passer à `hors-ligne` après quelques dizaines de secondes — sans que l'objet ait rien publié lui-même : c'est le broker qui a tenu sa promesse.
