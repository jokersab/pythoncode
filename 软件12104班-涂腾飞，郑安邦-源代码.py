import sqlite3


def getConnection():  # 连接数据库，创建三张表，用户表，图书表，图书状态表
    dbstring = "E:\SQLite\sqlite3.db"
    conn = sqlite3.connect(dbstring)
    cur = conn.cursor()
    sqlstring = "create table if not exists library(id integer," \
                "bookname varchar(30) primary key,author varchar(30),publish varchar(50),date DATE,price float)"
    sqlstring_1 = "create table if not exists user(id integer," \
                  "user_name varchar(30) primary key,s_borrow int,browwed varchar(30),s_date DATE,return date,extended varchar(20))"
    sqlstring_2 = "create table if not exists bookstatus(id integer," \
                  "bookname varchar(30) primary key,remainder integer DEFAULT 3,at varchar(10)," \
                  "foreign key(bookname) references library(bookname),foreign key (id) REFERENCES library(id))"
    cur = conn.execute(sqlstring)
    cur = conn.execute(sqlstring_1)
    cur = conn.execute(sqlstring_2)
    return conn


def input_book():  # 输入图书信息
    list = []
    id = int(input("请输入添加的图书编号:"))
    bookname = input("请输入图书名称:")
    author = input("请输入作者名:")
    publish = input("请输入出版社名:")
    date = input("请输入出版日期:")  # 格式YYYY-MM-DD
    price = float(input("请输入图书价格:"))
    list.append(id)
    list.append(bookname)
    list.append(author)
    list.append(publish)
    list.append(date)
    list.append(price)
    return list


def get_user():  # 获取数据库中的用户表的信息
    dbinfo = getConnection()
    cur = dbinfo.cursor()
    user = {}
    cur.execute("select * from user")
    records = cur.fetchall()
    for line in records:
        key = line[1]
        user[key] = line
    cur.close()
    return user


def add(book):  # 添加图书
    while True:
        list = input_book()
        name = list[1]
        book[name] = list
        print("添加成功")
        save_book(book, name)
        save_book_status(book,name)
        print("是否继续添加？0或1")
        flag = int(input())
        if flag == 0:
            break
    return book


def change(book, name):  # 修改图书信息
    list_1 = []
    new_id = int(input("请输入修改后的编号："))
    author = input("请输入修改后的作者名:")
    publish = input("请输入修改后的出版社名:")
    date = input("请输入修改后的出版日期:")  # 格式YYYY-MM-DD
    price = float(input("请输入修改后的图书价格:"))
    list_1.append(new_id)
    list_1.append(name)
    list_1.append(author)
    list_1.append(publish)
    list_1.append(date)
    list_1.append(price)
    book_1 = list(book[name])
    book_1 = list_1
    book[name] = tuple(book_1)
    save_change(book, name)
    return book


def get_book():  # 获取数据库中的图书表的信息
    dbinfo = getConnection()
    cur = dbinfo.cursor()
    book = {}
    cur.execute("select * from library")
    records = cur.fetchall()
    for line in records:
        key = line[1]
        book[key] = line
    cur.close()
    return book


def get_book_status():  # 获取数据库中的图书状态表
    dbinfo = getConnection()
    cur = dbinfo.cursor()
    book_statu = {}
    cur.execute("select * from bookstatus")
    records = cur.fetchall()
    for line in records:
        key = line[1]
        book_statu[key] = line
    cur.close()
    return book_statu


def show_data(table_name):  # 打印数据库中的表的信息
    dbinfo = getConnection()
    cur = dbinfo.cursor()
    cur.execute("select * from " + table_name)
    records = cur.fetchall()
    for line in records:
        print(line)
    cur.close()


def search_book(book, name):  # 查询图书信息
    if book[name]:
        print(book[name])
    else:
        print("图书不存在")
    print("是否需要查询所有的图书信息？0或1")
    falg = int(input())
    if falg == 1:
        show_data("library")#打印图书列表


def search_book_message(book_status, name):  # 管理员查询图书状态信息
    if book_status[name]:
        print(book_status[name])
    else:
        print("图书不存在")
    dbinfo = getConnection()#连接数据库
    cur = dbinfo.cursor()
    cur.execute("select * from user")
    records = cur.fetchall()
    for line in records:
        if name in line[3]:
            print(line)
    cur.close()
    print("是否需要查询所有的图书状态？0或1")
    falg = int(input())
    if falg == 1:
        show_data("bookstatus")


def borrow_book(user, name, book_status, time):  # 借书
    book_2 = list(user[name])
    if book_2[-1] == "已超期":  # 判定是否有书超期未还
        print("有书超时未还！")
        return False
    elif time > book_2[-2]  and book_2[3] != "不在库":
        print("超时还书")
        book_2[-1] = "已超期"
        print("有图书超期未还，不能借书")
        return False
    elif book_2[2] == 0:  # 剩余借书次数不足，也不可以借书
        print("剩余借书次数不足")
        return False
    else:
        book_name = input("请输入想借的书的名字：")
        print(book_status[book_name])
        book_1 = list(book_status[book_name])
        if book_status[book_name][2] > 0:
            book_1[2] -= 1  # 图书数量减一
            if book_1[2] == 0:
               book_1[-1] = "不在库"
            book_2[2] -= 1  # 剩余借书次数减一
            if book_2[3] == "未借书":
                book_2[3] = ""
            book_2[3] += " "
            book_2[3] += book_name
            print("借书时间不允许超过七天")
            book_2[4] = input("请输入借书日期：")
            book_2[5] = input("请输入还书日期：")
        else:
            book_1[-1] = "不在库"
            print("藏书数量不足")
        user[name] = tuple(book_2)
        book_status[book_name] = tuple(book_1)
        update_user(user, name)
        update_book_status(book_status, book_name)#更新图书状态信息
        list_1 = []
        list_1.append(user)
        list_1.append(book_status)
        return list_1


def return_book(user, name, book_status):  # 还书
    print(user[name])
    m_1 = list(user[name])
    if m_1[-1] == "超期":
        m_1[-1] = "未超期"
    book_name = m_1[3].split()
    for i in book_name:
        m_2 = list(book_status[i])
        m_2[2] += 1  # 图书数量加一
        m_1[2] += 1  # 剩余借书次数加一
        if m_2[-1] == "不在库":
            m_2[-1] == "在库"
        book_status[i] = tuple(m_2)
        update_book_status(book_status, i)#更新图书状态信息
    m_1[3] = "未借书"
    user[name] = tuple(m_1)
    update_user(user, name)#更新用户信息
    list_1 = []
    list_1.append(user)
    list_1.append(book_status)
    return list_1

def update_user(user, name):  # 更新用户状态信息
    link = getConnection()
    list_1 = list(user[name])
    sql = "update user set s_borrow=?,browwed=?,s_date=?,return=? where id =" + str(list_1[0])
    message = (list_1[2], list_1[3], list_1[4], list_1[5])
    link.execute(sql, message)
    link.commit()
    print(user[name])
    print("保存成功")
    link.close()


def update_book_status(book_status, name):  # 更新图书状态信息
    link = getConnection()
    list_1 = list(book_status[name])
    sql = "update bookstatus set remainder=?,at=? where id =" + str(list_1[0])
    message = (list_1[2], list_1[3])
    link.execute(sql, message)
    link.commit()
    print(book_status[name])
    print("保存成功")
    link.close()


def save_book(book, id):  # 保存图书信息到数据库
    link = getConnection()
    sql = "insert into library(id,bookname,author,publish,date,price) values(?,?,?,?,?,?)"
    message = (book[id][0], book[id][1], book[id][2], book[id][3], book[id][4], book[id][5])
    link.execute(sql, message)
    link.commit()
    print(book[id])
    print("保存成功")
    link.close()


def save_book_status(book, id):  # 保存图书信息到数据库
    link = getConnection()
    sql = "insert into bookstatus(id,bookname,remainder,at) values(?,?,?,?)"
    message = (book[id][0], book[id][1], 3,"在库")
    link.execute(sql, message)
    link.commit()
    print("图书状态保存成功")
    link.close()

def check_user(user, name):  # 检查登录用户的身份
    if user[name]:
        print(user[name])
        return True
    else:
        return False


def save_change(book, name):  # 保存修改后的图书的信息
    link = getConnection()
    sql = "update library set id=?,author=?,publish=?,date=?,price=? where bookname="+"'"+name+"'"
    message = (book[name][0], book[name][2], book[name][3], book[name][4], book[name][5])
    link.execute(sql, message)
    link.commit()
    show_data("library")
    print("保存成功")
    link.close()


def deletebook(book,name):
    save_delete_book_status(book, name)
    save_delete(book,name)
    book.pop(name)
    return book

def save_delete(book, name):  # 保存删除后的图书的信息
    link = getConnection()
    sql = "delete from library where id="+str(book[name][0])
    link.execute(sql)
    link.commit()
    show_data("library")
    print("保存成功")
    link.close()

def save_delete_book_status(book, name):  # 保存删除后的图书的信息
    link = getConnection()
    sql = "delete from bookstatus where id="+str(book[name][0])
    link.execute(sql)
    link.commit()
    show_data("bookstatus")
    print("保存成功")
    link.close()

def user_search(user, user_name,flag):  # 查询用户表的信息
    print(user[user_name])
    if flag == "admin":
        print("是否需要打印全部用户信息？0或1")
        point = input()
        if point == "1":
            print(user)



def loading(num, user):  # 登录菜单，判定使用系统的人是否为管理员
    if num == '1':
        print("--------管理员登录--------")
        admin_name = input("管理员账号：")
        password = input("密码：")
        if admin_name == "1234567" and password == "admin123":
            print("登录成功！")
            return "admin"
        else:
            return  False
    elif num == '2':
        print("--------用户登录-------")
        user_name = input("请输入用户名：")
        if check_user(user, user_name):
            print("--------欢迎使用图书管理系统-------")
            print("登录成功！")
            return user_name
        else:
            return False
    else:
        return False

def menu():
    print("————————欢迎使用图书管理系统——————————")
    print("1.管理员登录")
    print("2.用户登录")


def admin_menu():
    print("1.增加图书\t   2.修改图书\t")
    print("3.查询图书信息\t 4.查询图书状态\t")
    print("5.用户状态查询\t 6.打印图书列表\t")
    print("7.打印用户列表\t 8.删除图书\t")
    print("9.退出系统\t")


def user_menu():
    print("1.借书\t   2.还书\t")
    print("3.查询用户状态\t 4.退出系统\t")


# 程序入口
if __name__ == "__main__":
    getConnection()#连接数据库
    book = get_book()#获取book表的信息
    user = get_user()#获取user表的信息
    book_status = get_book_status()#获取book_status表的信息
    menu()#打印功能菜单
    num = input("请输入选项：")
    flag = loading(num, user)#登录，选择管理员或用户
if flag == 'admin':
    while True:
        admin_menu()#管理员界面
        select = int(input("请输入你的选择："))
        if select == 1:
            book = add(book)#添加图书
        elif select == 2:
            name = input("请输入要修改的图书名称:")
            book = change(book, name)#修改图书
        elif select == 3:
            name = input("请输入要查询的图书名称:")
            search_book(book, name)#查询图书
        elif select == 4:
            book_status = get_book_status()
            name = input("请输入要查询的图书名称:")
            search_book_message(book_status, name)#查询图书状态
        elif select == 5:
            user_name = input("请输入要查询的用户名称：")
            user_search(user, user_name,flag)#查询用户状态
        elif select == 6:
            show_data("library")#打印图书列表
        elif select == 7:
            show_data("user")#打印用户列表
        elif select == 8:
            name = input("请输入要删除的图书名称:")
            book = deletebook(book,name)#删除图书
        else:
            break
elif flag != False:
    print("····假定借书的当天的时间为6月3号····")
    time = input("请输入当天时间（不要超过2023 06 03，不然会有很多超期）：")
    user_name = flag
    while True:
        user_menu()
        select = int(input("请输入你的选择："))
        if select == 1:
            list1 = borrow_book(user, user_name, book_status, time)#借书
            if list1 != False:
                user = list1[0]
                book_status = list1[1]
        elif select == 2:
            list1 = return_book(user, user_name, book_status)#还书
            user = list1[0]
            book_status = list1[1]
        elif select == 3:
            user_search(user, user_name,flag)#拥护状态查询
        else:
            break
else:
    print("非法登录")