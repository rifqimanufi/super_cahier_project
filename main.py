from random import randint
from tabulate import tabulate
import mysql.connector
from mysql.connector.dbapi import DATETIME

mydb = mysql.connector.connect(
    host = "localhost", 
    user = "root",
    password = "123456qq", 
    database = "super_cashier" 
)

def transaction():
    trc_id = randint(1,1000000)
    return trc_id


def addItem(trc_id):
    transaction_id = trc_id

    print("----------------- Berikut daftar produk ------------------")

    sql = "select * from super_cashier.data_produk"
    c = mydb.cursor()
    c.execute(sql)
    
    myresult = c.fetchall()

    headers = ['item_id', 'nama_item', 'harga']
    print(tabulate(myresult,headers))


    #menambahkan item
    nama_item = input("masukan nama item : ")
    jumlah_item = int(input("masukan jumlah item : "))

    #item_id
    sql_item_it = "SELECT item_id from data_produk where nama_item = '{}'".format(nama_item)
    c = mydb.cursor()
    c.execute(sql_item_it)
    item_id = c.fetchone()
    item_id = item_id[0]

    #harga
    sql_harga = "SELECT harga from data_produk where nama_item = '{}'".format(nama_item)
    c = mydb.cursor()
    c.execute(sql_harga)
    harga = c.fetchone()
    harga = harga[0]

    #total
    total_harga = harga*jumlah_item

    data = (transaction_id, item_id, nama_item, jumlah_item, harga, total_harga)

    sql_add_item = "INSERT INTO transaction_detail_table VALUES(%s,%s,%s,%s,%s,%s, CURDATE())"

    c = mydb.cursor()
    c.execute(sql_add_item,data)
    mydb.commit()

    

def updateQtyItem(trc_id):
    
    transaction_id = trc_id

    
    nama_item = input("masukan nama item : ")
    jumlah_item = int(input("masukan jumlah item : "))


    #harga
    sql_harga = "SELECT harga FROM transaction_detail_table where trc_id = '{}' AND nama_item = '{}'".format(transaction_id, nama_item)
    c = mydb.cursor()
    c.execute(sql_harga)
    harga = c.fetchone()
    harga = harga[0]

    #total
    total_harga = harga*jumlah_item

    sql_add_item = "UPDATE transaction_detail_table SET jumlah_item = '{}', total_harga = {} WHERE trc_id = '{}' AND nama_item = '{}'".format(jumlah_item, total_harga, transaction_id, nama_item)
    c = mydb.cursor()
    c.execute(sql_add_item)
    mydb.commit()


def deleteItem(trc_id):
    
    transaction_id = trc_id

    
    nama_item = input("masukan nama item : ")

    sql_del_item = "DELETE FROM transaction_detail_table WHERE trc_id = '{}' AND nama_item = '{}'".format(transaction_id, nama_item)
    c = mydb.cursor()
    c.execute(sql_del_item)
    mydb.commit()

def resetTransaction(trc_id):
    
    transaction_id = trc_id

    sql_reset = "DELETE FROM transaction_detail_table WHERE trc_id = '{}'".format(transaction_id)
    c = mydb.cursor()
    c.execute(sql_reset)
    mydb.commit()

def checkItemDetail(trc_id):
    
    transaction_id = trc_id

    sql = "SELECT * FROM transaction_detail_table WHERE trc_id = '{}'".format(transaction_id)
    c = mydb.cursor()
    c.execute(sql)
    
    myresult = c.fetchall()

    headers = ['trc_id', 'item_id', 'nama_item', 'jumlah_item', 'harga', 'total_harga', 'tanggal']
    print(tabulate(myresult,headers))

def checkOut(trc_id):
    
    transaction_id = trc_id

    #jumlah
    sql_jml_item = "SELECT SUM(jumlah_item) from transaction_detail_table where trc_id = '{}'".format(transaction_id)
    c = mydb.cursor()
    c.execute(sql_jml_item)
    jumlah_item = c.fetchone()
    jumlah_item = jumlah_item[0]

    #harga
    sql_harga = "SELECT SUM(harga) from transaction_detail_table where trc_id = '{}'".format(transaction_id)
    c = mydb.cursor()
    c.execute(sql_harga)
    harga = c.fetchone()
    harga = int(harga[0])
    print("ini adalah harga nya =====> {}", harga)

    if harga>=200000 and harga<300000:
        diskon = 5
        diskon_str = '5%'
    elif harga>=300000 and harga<500000:
        diskon = 6
        diskon_str = '6%'
    elif harga>=500000:
        diskon = 7
        diskon_str = '7%'
    else:
        diskon = 0
        diskon_str = '0%'

    total_harga = harga - (harga*(diskon/100))

    data = (transaction_id, jumlah_item, harga, diskon_str, total_harga)

    sql = "INSERT INTO transaction_table VALUES(%s,%s,%s,%s,%s, CURDATE())"

    c = mydb.cursor()
    c.execute(sql,data)
    mydb.commit()


    sql = "SELECT * FROM transaction_table WHERE trc_id = '{}'".format(transaction_id)
    c = mydb.cursor()
    c.execute(sql)
    
    myresult = c.fetchall()

    headers = ['trc_id', 'jumlah_item', 'harga', 'diskon', 'total_harga', 'tanggal']
    print(tabulate(myresult,headers))


def purchase(trc_id):
    
    transaction_id = trc_id

    sql = "SELECT total_harga from transaction_table where trc_id = '{}'".format(transaction_id)
    c = mydb.cursor()
    c.execute(sql)
    harga = c.fetchone()
    total_harga = int(harga[0])

    while True :
        print('Total yang harus dibayar = {}'. format(total_harga))
        uang_anda = int(input('Masukan jumlah uang : '))
        if(uang_anda > total_harga) :
            kembali = uang_anda - total_harga
            print('Terima kasih \n\nUang kembali anda : {}'. format(kembali))
            break
        elif(uang_anda == total_harga) :
            print('Terima kasih')
            break
        else :
            kekurangan = total_harga - uang_anda
            print('uang anda kurang sebesar {}, mohon masukan uang pas'.format(kekurangan))

    print("---------------------------------------------")

    love = [    "..##....##...",    ".##..##..##..",    ".##.......##.",    "..##.....##..",    "...##...##...",    "....##.##....",    "......#......"]

    for line in love:
        print(line)

    print("""
    Thank you. See you next time ~
    ------------------------------------------------------
    Terima Kasih
    """)



def main_menu():
    # User interface layout
    print("""---------------- Welcome to Super Cashier System  ----------------
    1. Start program
    """)

    option = int(input("Enter option no: "))
    
    transaction_id = transaction()


    while option == 1 :
        print("""---------------- please choice the task  ----------------
        1. Add item
        2. update quantity item
        3. delete item
        4. reset transaction
        5. check item detail
        6. check out
        7. purchase
        """)
        choice = int(input("Enter task no: "))
        if(choice==1):
            addItem(transaction_id)
        elif(choice==2):
            updateQtyItem(transaction_id)
        elif(choice==3):
            deleteItem(transaction_id)
        elif(choice==4):
            resetTransaction(transaction_id)
        elif(choice==5):
            checkItemDetail(transaction_id)
        elif(choice==6):
            checkOut(transaction_id)
        elif(choice==7):
            purchase(transaction_id)
            break
        else:
            print("---------------------- Please put the correct number -----------------------")
    else:
        print("---------------------- Please put the correct number -----------------------")

start_program = main_menu()