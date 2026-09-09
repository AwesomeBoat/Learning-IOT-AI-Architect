# Étape 6/7 — Un actionneur piloté à distance (MicroPython)

*Voir `00_README_fil_rouge_micropython.md` à la racine du dossier pour le mode d'emploi complet.*

## Ce qui est nouveau à cette étape
Circuit PIR + LED. Deux logiques coexistent : automatique (PIR local) et pilotage à distance via `.../actionneur/eclairage/commande` (`ON` / `OFF` / `AUTO`). L'état est publié en **retained** sur `.../actionneur/eclairage/etat`.

**⚠️ Personnalisez `PRENOM` avant de lancer la simulation.**

## Différence avec la version Arduino/C++
En MicroPython, on utilise `client.set_callback(...)` + `client.subscribe(...)` puis `client.check_msg()` **non bloquant** dans la boucle principale — l'équivalent du couple `setCallback()`/`clientMqtt.loop()` côté Arduino/PubSubClient. `check_msg()` doit être appelé très régulièrement pour ne pas rater de message.

## À essayer
- Publier `ON`, `OFF`, puis `AUTO` sur le topic de commande depuis MQTTX Web.
- Se déconnecter/reconnecter à `.../etat` avec un client MQTT pour vérifier le comportement retained.
