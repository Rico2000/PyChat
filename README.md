# PyChat
### Verteilte-Systeme-Projekt von Rico Rauschkolb und Leonhard Stengel

Ein simpler Messengerdienst.

Get started:

1) Server starten:
    python server.py
    - gewünschten Port angeben

2) beliebig viele Clients starten
    python client.py
    - Hostname des Servers angeben
    - Port des Servers angeben
    - einen einmaligen Username angeben

Clients landen zunächst in der Lobby. Dort können sie mit allen anderen Clients in der Lobby kommunizieren.

Von dort können Clients mit dem Befehl /join Gruppen beitreten oder erstellen. In diesen Gruppen kommunizieren Clients nur mit Anderen, die in der selben Gruppe sind. Eine Gruppe kann über den Befehl /leave verlassen werden.

Wenn ein privater Chat zwischen zwei Clients gewünscht wird, so kann über den Befehl /pp und der Angabe des Usernames ein Peer-To-Peer-Chat gestartet werden. Der PP-Chat startet sobald beide Gesprächspartner einen Chat über den /pp-Befehl anfordern. Die Kommunikation läuft dann NICHT mehr über den Server sondern direkt zwischen den Clients ab. Der PP-Chat wird ebenfalls mit dem Befehl /leave verlassen.