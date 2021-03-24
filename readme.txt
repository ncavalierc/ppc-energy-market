Monsieur,

Vous trouverez les schémas de l'architecture de notre projet.

Point sur ce qui a déjà été fait:
Actuellement, nous avons mis en place la message queue entre le home et le market ce qui nous permet de faire des demandes d'énergie au market. Le market est multi threadé : il crée un thread par requête home. Nous devons modifier le code pour mettre en place un pool de thread.

Du côté du home, pour l'instant nous avons la possibilité de créer un seul processus fils. Nous chercherons à améliorer le programme afin d'avoir plusieurs processus fils client en même temps.

Ainsi, vous pourrez consulter notre code via ce lien git : https://github.com/ncavalierc/ppc-energy-market.git

Bien cordialement

CAVALIER Nicolas
ISSARNI Titouan
