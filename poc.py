import mysql.connector 
from pyope.ope import OPE
##Implémentation ORE



##Coté client
## Insérer un nouveau salaire coté client
def client_put(id,val,connec,cipher):
    
    ## Implementation de l'Order Reavealing Encryption
    valc = cipher.encrypt(int(val))
    server_put(id,valc,connec)
    
## Comparer deux salaires entre eux
def client_compare(id1,id2,connec):
    ida = server_compare(id1,id2)
    return ida

## Additionner la somme des salaires
def client_sum(connec, cipher):
    encrypted_sum = server_sum(connec)
    ## Coté dechiffré client et affichage
    valdc = cipher.decrypt(encrypted_sum)
    return valdc
    
##Coté serveur
## Insérer un nouveau salaire coté serveur
def server_put(id,valc,connec):
# Ecriture des requetes
    sql = "INSERT INTO salaire_employe(id,salaire) VALUES (%s,%s)"
      # Creation du curseur pour etablir la connexion
    cur = connec.cursor()
    # Execution des requetes
    val = (id, valc)
    cur.execute(sql,val)
    connec.commit()
    
def server_compare(id1,id2,connec):
    ## Comparaison avec ORE et retour du resultat
    cur = connec.cursor()
    query = "SELECT salaire FROM salaire_employe WHERE nom = %s"
    cur.execute(query, (id1,))
    val1 = curseur.fetchone()
    cur.execute(query, (id2,))
    val2 = curseur.fetchone()
    if val1 == val2 :
        return id1 + " a le même salaire que " + id2
    elif val1 <= val2:
        return id2 + " a le plus grand salaire"
    else:
        return id1 + " a le plus grand salaire"

def server_sum(connec):
    cur = connec.cursor()
    query = "SELECT salaire FROM salaire_employe"
    cur.execute(query)


if __name__ == '__main__':

    db_user = 'root'
    db_password = 'root'
    db_host = 'localhost'
    db_db = 'poc_question31'
    server_host = 'server'

    cle = b"*v0jTYiU$aLydY3!P/OcEC7A&97P6+&XH#UIHvHQptFt4$*j5t!cRt3N74tYJDte"
    cipher = OPE(cle)
    
    #Fonction de connexion à la base de données
    def db_connexion(user,pas,host,db):
        cnx = mysql.connector.connect(user=user, password=pas, host=host,
                                    database=db)
        return cnx
    connec = db_connexion(db_user,db_password,db_host,db_db)
    # Afficher un menu dans le terminal permettant de choisir entre les différentes opérations à savoir, insérer un nouveau salaire, comparer deux salaires entre eux et additionner la somme des salaires
    print("1. Insérer un nouveau salaire")
    print("2. Comparer deux salaires")
    print("3. Additionner la somme des salaires")
    print("4. Quitter")
    choice = input("Entrez votre choix : ")
    #Demander la valeur du salaire à insérer pour le choix 1
    if choice == "1":
        nom = input("Entrez l'id de l'employé : ")
        salaire = input("Entrez le salaire de l'employé : ")
        client_put(nom,salaire,connec,cipher)
        print("Salaire inséré avec succès")
    if choice == "2":
        nom1 = input("Entrez le premier id : ")
        nom2 = input("Entrez le deuxième id : ")
        print(f'{client_compare(nom1,nom2,connec)}')
    if choice == "3":
        print(client_sum(connec, cipher))
    if choice == "4":
        exit()
