import mysql.connector 

##Coté client

## Insérer un nouveau salaire
def client_put(id,val,connec):
    
    ## Implementation de l'Order Reavealing Encryption
    #valc = generer_cle(b'long key' * 2)
    val = (id, val)
    
#def client_compare(id1,id2)

#def client_sum()


##Coté serveur

def server_put(id,val,connec)
# Ecriture des requetes
    sql = "INSERT INTO salaire_employe(id,salaire) VALUES (%s,%s)"
      # Creation du curseur pour etablir la connexion
    cur = connec.cursor()
    # Execution des requetes
    cur.execute(sql,val)
    connec.commit()
#def server_compare(id1,id2)

#def server_sum()



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
        put(nom,salaire,connec)
    