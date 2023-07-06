import mysql.connector as mysql



def DBinit():
        con=mysql.connect(host='localhost',
                              port ='3306',
                              user='root',
                              password='1234',
                              database ='products')
        query = 'create table if not exists user(userID varchar(100) primary key,password varchar(100))'
        query1 = 'create table if not exists admins(userID varchar(100) primary key,password varchar(100))'
        query2 = 'create table if not exists product(name varchar(100) primary key,price int)'
        cur=con.cursor()
        cur.execute(query)
        cur.execute(query1)
        cur.execute(query2)
        print('connected')
        return con


def login(conn,userID,password):
        query = 'select * from admins where userID=%s  and password=%s'
        query1 = 'select * from user where userID=%s  and password=%s'
        cur=conn.cursor()
        cur.execute(query,(userID,password))
        admin=cur.fetchone()
        if admin!=None:
            AdminloggedIn(conn)
        else:
            cur.execute(query1,(userID,password)) 
            user=cur.fetchone()
            if user!=None:
                UserloggedIn(conn)
            else:
                query2 = "insert into user (userID,password) values('%s','%s')"
                cur.execute(query2)
                print('\nNew user added successfully!!')
                UserloggedIn(conn)
                

def addProduct(conn):
        name = input('\nEnter product name->')
        price = int(input('Enter product price->'))
        query = 'insert into product(name,price) values(%s,%s)'
        cur=conn.cursor()
        cur.execute(query,(name,price))
        conn.commit()
        print('Product added')

def deleteProduct(conn):
        name = input(' Enter product name->')
        query = 'delete from product where name=%s'
        cur=conn.cursor()
        cur.execute(query,(name,))
        conn.commit()
        print('Product deleted')
    
def viewProduct(conn):
        query = 'select * from product'
        cur=conn.cursor()
        cur.execute(query)
        row=cur.fetchall()
        for r in row:
            print(r)

def sortProduct(conn):
        query = 'select * from product order by name'
        cur=conn.cursor()
        cur.execute(query)
        row=cur.fetchall()
        for r in row:
            print(r)
    
def searchProduct(conn):
        name=input('Enter product name->')
        query = 'select * from product where name=%s'
        cur=conn.cursor()
        cur.execute(query,(name,))
        row=cur.fetchall()
        for r in row:
            print(r)

def checkout(conn):
    query = 'select * from product'
    cur=conn.cursor()
    cur.execute(query)
    row=cur.fetchall()
    for r in row:
        print(r)
    print("To exit and bill press 0")
    total = 0
    while(1):
        prod = input("Enter product Name->")
        if(prod == '0' ):
            break
        else:
            try:
                query = 'select price from product where name=%s'
            except:
                print("Product not found")
            cur=conn.cursor()
            cur.execute(query,(prod,))
            row=int(cur.fetchone()[0])
            total = total + row
    print("Total price is",total)
            

            

def AdminloggedIn(conn):
        print(' admin logged in')
        while(1):
            print('''What do you wanna do
            1. Add product
            2. View product
            3. Delete product
            4. Sort products
            5. Search products
            6. Exit''')
            choice=int(input('Enter your choice->'))
            if choice==1:
                addProduct(conn)
            elif choice==2:
                viewProduct(conn)
            elif choice==3:
                deleteProduct(conn)
            elif choice==4:
                sortProduct(conn)
            elif choice==5:
                searchProduct(conn)
            elif choice==6:
                print("Thank you for using e-comm")
                break
            else:
                print('Invalid choice')

def UserloggedIn(conn):
        print('user logged in')
        while(1):
            print('''What do you wanna do
            1. View product
            2. Sort products
            3. Search products
            4. Checkout
            5. Exit''')
            choice=int(input('Enter your choice->'))
            if choice==1:
                viewProduct(conn)
            elif choice==2:
                sortProduct(conn)
            elif choice==3:
                searchProduct(conn)
            elif choice==4:
                checkout(conn)
            elif choice==5:
                print("Thank you for shopping")
                break
            else:
                print('Invalid choice')

    
if __name__=='__main__':
        conn = DBinit()
        user=input('enter user name-> ')
        password=input('Enter your password-> ')
        login(conn,user,password)