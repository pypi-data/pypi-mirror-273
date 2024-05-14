#mqttdatalogger

Enregistrement des données issues d'un serveur MQTT dans un fichier csv.<br />

Exemple d'utilisation : <br />


import getpass<br />
import mqttthreaddatalogger as MQTT<br />

Username = input('Entrez votre identifiant MQTT : ') <br />
pwd = getpass.getpass('Entrez votre mot de passe MQTT :')<br />

auth = {<br />
    'username':Username,<br />
    'password':pwd<br />
}
# crée le thread transport tcp ou websockets <br />
m = MQTT.mqttthreaddatalogger("url_mqtt",portmqtt,auth["username"],auth["password"],"tcp")   <br /> 
# topics auquel on s'abonne<br />
m.selectTopic(["node_iot2020/arduino/out/"])  <br />
# selection des clés des données voulues , les données seront dans m.data[0], m.data[1],... <br />
m.selectKey(["['ecl']","['temps']"])<br />
# ou pour Lorawan, après le # se trouve le nom du champ qui sera utilisé dans le fichier csv,... <br />
m.selectKey(["['uplink_message']['decoded_payload']['temperature']#temp","['uplink_message']['rx_metadata'][0]['gateway_ids']['gateway_id']#Id_gateway","['end_device_ids']['device_id']#ID_device"])
<br />Après le # on rajoute le nom de la 1ère ligne du fichier de données</br>>
 
m.selectNomFichier("testdonnees.csv")<br />
# pour afficher ou non les info sur la console <br />
m.affichage_console(True) <br />
# démarre le thread, (exécution indépendante du programme principal)<br />
m.start()   <br />               
time.sleep(1)<br />
#publication d'un message vers MQTT  <br />
#m.client.publish("votretopic/test/in/",payload="{\"pression\":1024}",qos=0)<br />
<br />



