import mysql.connector 

##Implémentation ORE



##Coté client
## Insérer un nouveau salaire coté client
def client_put(id,val,connec):
    
    ## Implementation de l'Order Reavealing Encryption
    valc = generer_cle(b'long key' * 2)
    
    server_put(id,valc,connec)
## Comparer deux salaires entre eux
def client_compare(id1,id2):
    ida = server_compare(id1,id2)
    return ida

## Additionner la somme des salaires
def client_sum():
    encrypted_sum = server_sum()
    ## Coté dechiffré client et affichage


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
def server_compare(id1,id2):
    pass

def server_sum():
    connec = db_connexion(db_user,db_password,db_host,db_db)
    cur = connec.cursor()
    query = "SELECT salaire FROM salaire_employe"
    cur.execute(query)


if __name__ == '__main__':

    db_user = 'root'
    db_password = 'root'
    db_host = 'localhost'
    db_db = 'poc_question31'
    server_host = 'server'
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
        client_put(nom,salaire,connec)
        print("Salaire inséré avec succès")
    if choice == "2":
        nom1 = input("Entrez le premier id : ")
        nom2 = input("Entrez le deuxième id : ")
        print(f'le salaire le plus important est : {client_compare(nom1,nom2)}')
    if choice == "3":
        print(client_sum())
    if choice == "4":
        exit()