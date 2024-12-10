import mysql.connector
while True:
    user = str(input("enter your sql user "))
    password = str(input("enter your sql password "))
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = user,
            password = password,
            database = 'flight_game',
            collation = 'utf8mb4_general_ci',
            autocommit = True
            ) #connection with database
        cursor = connection.cursor()
        sql=(
        "CREATE TABLE `list_airport` ("
            "`list_seed` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,"
            "`airport_list` VARCHAR(500) NOT NULL COLLATE 'latin1_swedish_ci',"
            "PRIMARY KEY (`list_seed`) USING BTREE)"
        "COLLATE='latin1_swedish_ci'"
        "ENGINE=InnoDB;"
        ";")
        cursor.execute(sql)
        sql2=("CREATE TABLE `player` ("
            "`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,"
            "`name` VARCHAR(50) NOT NULL DEFAULT '0' COLLATE 'latin1_swedish_ci',"
            "`score` VARCHAR(50) NOT NULL DEFAULT '0.000000' COLLATE 'latin1_swedish_ci',"
            "`airport_seed` INT(10) UNSIGNED NULL DEFAULT '0',"
            "PRIMARY KEY (`id`) USING BTREE,"
            "INDEX `airport_seed` (`airport_seed`) USING BTREE,"
            "CONSTRAINT `FK_airport_list` FOREIGN KEY (`airport_seed`) REFERENCES `list_airport` (`list_seed`) ON UPDATE RESTRICT ON DELETE CASCADE)"
        "COLLATE='latin1_swedish_ci'"
        "ENGINE=InnoDB;"
        ";")
        cursor.execute(sql2)
        break
    except mysql.connector.errors.DatabaseError:
        print("Database error")
        print("confirm if u have entered the correct username and password")
        continue
#Had to split the command into two because for some reason it only create one table when everything is in the same variable