import mysql.connector 

##Coté client

## Insérer un nouveau salaire
function put(id,val,connec):
    # Ecriture des requetes
    sql = "INSERT INTO salaire_employe(id,salaire) VALUES (%s,%s)"
    val = (id, val)
    # Creation du curseur pour etablir la connexion
    cur = connec.cursor()
    # Execution des requetes
    cur.execute(sql,val)
    connec.commit()


#function compare(id1,id2)

#function sum()


##Coté serveur

#function put(id,val)

#function compare(id1,id2)

#function sum()



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

    