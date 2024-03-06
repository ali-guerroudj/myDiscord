import mysql.connector as MC 

try:
    conn = MC.connect(host = 'localhost', database = 'mydiscord', user = 'root', password ='wxop45az')
    cursor = conn.cursor()


    req ='SELECT * FROM mydiscord'
    cursor.execute(req)

    discordlist = cursor.fetchall( 

    )for discord in discordlist:
    print('')

except MC.Error as err:
    print(err)
finally:
    if(conn.is_connected()):
        cursor.close()
        conn.close()