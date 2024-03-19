from flask import Flask, render_template, request, send_file
import time
import json
import mysql.connector,sys
from pyope.ope import OPE
from phe import paillier
import json
import requests
import pickle

app = Flask(__name__)

# Définition de la fonction de connexion à la base de données
def db_connexion(user,pas,host,db):
    cnx = mysql.connector.connect(user=user, password=pas, host=host,
                                database=db)
    return cnx

# Définition de la fonction de fermeture de connexion à la base de données
def db_close(cnx):
    cnx.close()

# Définition de la fonction de génération de clé pour chiffrement OPE (relation d'ordre)
def generer_cle(key):
    return OPE(key)

# Insertion des valeurs chiffrés par OPE
def db_insert(cnx,nom,ORE_age):
    # Ecriture des requetes
    sql = "INSERT INTO age(nom,ORE_age) VALUES (%s,%s)"
    val = (nom, ORE_age)
    # Creation du curseur pour etablir la connexion
    cur = cnx.cursor()
    # Execution des requetes
    cur.execute(sql,val)
    cnx.commit()

def db_compare(cnx, nom1, nom2):
    # Selection des ages chiffres en fonction des noms
    cur = cnx.cursor()
    # Age 1
    sql_select_query1 = """SELECT ORE_age FROM age WHERE nom=%s"""
    cur.execute(sql_select_query1, (nom1,))
    try:
        personne1 = cur.fetchall()[0]
    except:
        return("ERREUR - NOM INCONNU")
    # Age 2
    sql_select_query2 = """SELECT ORE_age FROM age WHERE nom=%s"""
    cur.execute(sql_select_query2, (nom2,))
    try:
        personne2 = cur.fetchall()[0]
    except:
        return("ERREUR - NOM INCONNU")
    # Recuperation des valeurs entieres sur les tuples
    agePersonne1 =  personne1[0]
    agePersonne2 =  personne2[0]
        
    # Comparaison
    if agePersonne1 == agePersonne2:
        return("%s a le même âge que %s" % (nom1, nom2))
    elif agePersonne1 > agePersonne2:
        return("%s est plus vieux que %s" % (nom1, nom2))
    else:
        return("%s est plus vieux que %s" % (nom2, nom1))
        

cipherORE = generer_cle(b'long key' * 2)
# Paire de clés pour le chiffrement homomorphique
public_key = paillier.PaillierPublicKey(2161831391)
private_key = paillier.PaillierPrivateKey(public_key, 47147,45853)
data = request.data.decode("utf-8")
params = data.split("&")
        
          
# Inserer nouveau salaire
if(int(params[0].split("=")[1]) == 3):
    nom = params[1].split("=")[1]
    age = int(params[2].split("=")[1])
    connec = db_connexion(db_user,db_password,db_host,db_db)
    db_insert(connec,nom,cipherORE.encrypt(age))
    ageHOM = public_key.encrypt(age)
    # Decomposition de la serie composant l'objet ageHOM
    serieHOM = {'public_key': public_key.n, 'ciphertext': str(ageHOM.ciphertext()), 'exponent': ageHOM.exponent}
    # Dump de la serie pour exploitation par le serveur distant
    serialized = json.dumps(serieHOM)
    # Envoi vers l'app serveur
    payload = {'nom':str(nom), 'HOM_age':serialized}
    # Envoi du payload vers l'app serveur
    r = requests.post("http://"+server_host+":5000/encrypted", json=payload)
    db_close(connec)
    #return json.dumps({"response":"OK"})
            
# Additionner somme des salaires
elif(int(params[0].split("=")[1]) == 6):
    nom1 = params[1].split("=")[1]
    nom2 = params[2].split("=")[1]
    connec = db_connexion(db_user,db_password,db_host,db_db)
    # Generation du payload + envoi vers l'app serveur
    payload = {'nom1':str(nom1), 'nom2':str(nom2)}
    r = requests.post("http://"+server_host+":5000/sumPost", json=payload)
    # Temps d'arrêt pour que le serveur traite la demande et mette à disposition le résultat en GET 
    time.sleep(2)
    # Récupération de la réponse de l'app serveur
    r = requests.get("http://"+server_host+":5000/sumPost", json=payload).json()
    # Reconstitution et Déchiffrement du message
    cipherSomme = int(r.get('ciphertext'))
    exponentSomme = int(r.get('exponent'))
    # Regeneration de l'objet
    encryptedSommeObject = paillier.EncryptedNumber(public_key,cipherSomme,exponentSomme)
    # Dechiffrement de la somme
    somme = private_key.decrypt(encryptedSommeObject)
    result = "La somme des deux âges est : " + str(somme)
    #return json.dumps({"response":result})
            
        # Comparer ages de deux personnes
elif(int(params[0].split("=")[1]) == 7):
    nom1 = params[1].split("=")[1]
    nom2 = params[2].split("=")[1]
    connec = db_connexion(db_user,db_password,db_host,db_db)
    result = db_compare(connec, nom1, nom2)
    #return json.dumps({"response":result})
            
        

if __name__ == '__main__':

    # Variable de connexion au container mysql 
    db_user = 'lulutoto'
    db_password = 'Ensibs2022!'
    db_host = 'db'
    db_db = 'TP2022_VIDELAINE-LUBISHTANI-BIZET'
    server_host = 'server'