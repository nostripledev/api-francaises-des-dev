from collections import namedtuple

from fastapi import UploadFile

from app.models import GetMembers, MemberIn, Category, CategoryOut, MemberWithCategory, MemberHasCategoryIn, \
    GetMemberHasNetwork, Network, MemberHasNetwork, MemberHasCategory, MemberHasNetworkIn, MemberOut

from app import settings
import mysql.connector

mydb = mysql.connector.connect(
    host=settings.HOST,
    user=settings.USER,
    password=settings.PASSWORD,
    database=settings.DATABASE,
    port=settings.PORT
)


async def get_members():
    cursor = mydb.cursor()
    cursor.execute("SELECT member.id, member.username, member.url_portfolio, member.date_validate, "
                   "member.date_deleted, GROUP_CONCAT(category.name) FROM member, member_has_category, category WHERE "
                   "member.id=member_has_category.id_member AND member_has_category.id_category=category.id GROUP BY "
                   "member.id")
    result = cursor.fetchall()
    member_record = namedtuple("Member", ["id", "username", "url_portfolio", "date_validate", "date_deleted", "name"])
    cursor.close()
    return [MemberWithCategory(id_member=member.id, username=member.username, url_portfolio=member.url_portfolio,
                               category_name=member.name) for member in map(member_record._make, result)
            if member.date_validate is not None and member.date_deleted is None]


async def get_member_by_id(id_member):
    member_record = namedtuple("Member",
                               ["id", "username", "firstname", "lastname", "description", "mail", "url_portfolio",
                                "date_validate", "date_deleted"])
    cursor = mydb.cursor()
    query = "SELECT {} FROM member WHERE id = %(id)s".format(", ".join(member_record._fields))
    cursor.execute(query, {'id': id_member})
    result = cursor.fetchone()
    cursor.close()
    if result is None:
        return None
    member = member_record._make(result)
    return MemberIn(id=member.id, username=member.username, firstname=member.firstname, lastname=member.lastname,
                    description=member.description, mail=member.mail, url_portfolio=member.url_portfolio)


async def create_member(member: MemberIn):
    cursor = mydb.cursor()
    sql = "INSERT INTO member (username, firstname, lastname, description, mail, url_portfolio) VALUES (%s, %s, %s, " \
          "%s, %s, %s)"
    val = (member.username, member.firstname, member.lastname, member.description, member.mail, member.url_portfolio)
    try:
        cursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error:
        return "ErrorSQL: the request was unsuccessful..."
    id = cursor.lastrowid
    cursor.close()
    return id


async def patch_member_update(member: MemberOut):
    cursor = mydb.cursor()
    sql = "UPDATE member SET firstname = %s, lastname = %s, description = %s, mail = %s, url_portfolio " \
          "= %s WHERE id = %s"
    val = (member.firstname, member.lastname, member.description, member.mail, member.url_portfolio, member.id)
    try:
        cursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error:
        return "ErrorSQL: the request was unsuccessful..."
    cursor.close()
    return None


async def get_categories():
    cursor = mydb.cursor()
    cursor.execute("SELECT id, name FROM category")
    result = cursor.fetchall()
    category_record = namedtuple("Category", ["id", "name"])
    cursor.close()
    return [Category(id=category.id, name=category.name) for category in
            map(category_record._make, result)]


async def post_category(category: CategoryOut):
    cursor = mydb.cursor()
    sql = "INSERT INTO category (name) VALUES (%s)"
    val = [category.name]
    try:
        cursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as exc:
        return "ErrorSQL: the request was unsuccessful..."
    cursor.close()
    return None


async def get_members_category(name_category: str):
    cursor = mydb.cursor()
    sql = "SELECT member.* FROM member, member_has_category, category WHERE member.id = member_has_category.id_member " \
          "AND member_has_category.id_category = category.id AND category.name = %(name)s"
    cursor.execute(sql, {"name": name_category})
    result = cursor.fetchall()
    member_record = namedtuple("Member",
                               ["id", "username", "lastname", "firstname", "description", "mail", "date_validate",
                                "date_deleted", "url_portfolio"])
    cursor.close()
    return [GetMembers(id=member.id, username=member.username, url_portfolio=member.url_portfolio) for member in
            map(member_record._make, result)
            if member.date_validate is not None and member.date_deleted is None]


async def return_id_category_by_name(name: str):
    cursor = mydb.cursor()
    sql = "SELECT id FROM category WHERE name = %(name)s"
    try:
        cursor.execute(sql, {"name": name})
        result = cursor.fetchone()
        return result[0]
    except TypeError:
        return "ErrorSQL : the request was unsuccessful"


async def post_add_category_on_member(member: MemberHasCategoryIn):
    cursor = mydb.cursor()
    sql = "INSERT INTO member_has_category (id_member, id_category) SELECT %s, %s FROM DUAL WHERE NOT EXISTS (SELECT " \
          "1 FROM member_has_category WHERE id_member = %s AND id_category = %s);"
    id_category = return_id_category_by_name(member.name)
    try:
        cursor.execute(sql, (member.id_member, id_category, member.id_member, id_category))
        mydb.commit()
    except mysql.connector.Error:
        return "ErrorSQL: the request was unsuccessful..."
    cursor.close()
    return None


async def get_network_of_member_by_id(id_member: int):
    cursor = mydb.cursor()
    sql = "SELECT network.name, member_has_network.url FROM network, member_has_network, member WHERE member.id = " \
          "member_has_network.id_member AND member_has_network.id_network = network.id AND member.id = %(id)s"
    cursor.execute(sql, {'id': id_member})
    result = cursor.fetchall()
    network_record = namedtuple("Network", ["name", "url"])
    cursor.close()
    return [GetMemberHasNetwork(name=network.name, url=network.url) for network in map(network_record._make, result)]


async def get_category_of_member_by_id(id_member: int):
    cursor = mydb.cursor()
    sql = "SELECT category.name FROM category, member, member_has_category WHERE member.id = " \
          "member_has_category.id_member AND member_has_category.id_category = category.id AND member.id = %(id)s"
    cursor.execute(sql, {'id': id_member})
    result = cursor.fetchall()
    category_record = namedtuple("Category", ["name"])
    cursor.close()
    return [CategoryOut(name=category.name) for category in map(category_record._make, result)]


async def get_network():
    cursor = mydb.cursor()
    sql = "SELECT * FROM network"
    cursor.execute(sql)
    result = cursor.fetchall()
    network_record = namedtuple("Network", ["id", "name"])
    cursor.close()
    return [Network(id=network.id, name=network.name) for network in map(network_record._make, result)]


async def post_network_on_member(member: MemberHasNetwork):
    cursor = mydb.cursor()
    sql = "INSERT INTO member_has_network (id_member, id_network, url) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE " \
          "url = %s"
    try:
        cursor.execute(sql, (member.id_member, member.id_network, member.url, member.url))
        mydb.commit()
    except mysql.connector.Error:
        return "ErrorSQL: the request was unsuccessful..."
    cursor.close()
    return None


async def delete_category_delete_by_member(member: MemberHasCategory):
    cursor = mydb.cursor()
    sql = "DELETE FROM member_has_category WHERE id_member = %s AND id_category = %s"
    try:
        cursor.execute(sql, (member.id_member, member.id_category))
        mydb.commit()
    except mysql.connector.Error:
        return "ErrorSQL: the request was unsuccessful..."
    cursor.close()
    return None


async def delete_network_delete_by_member(member: MemberHasNetworkIn):
    cursor = mydb.cursor()
    sql = "DELETE FROM member_has_network WHERE id_member = %s AND id_network = %s"
    try:
        cursor.execute(sql, (member.id_member, member.id_network))
        mydb.commit()
    except mysql.connector.Error:
        return "ErrorSQL : the request was unsuccessful..."
    cursor.close()
    return None


async def add_image_portfolio(file: UploadFile, id_member: int):
    cursor = mydb.cursor()
    sql = "UPDATE member SET image_portfolio = %s WHERE id = %s"
    try:
        cursor.execute(sql, (file.file.read(), id_member))
        mydb.commit()
    except mysql.connector.Error:
        return "ErrorSQL : the request was unsuccessful..."
    cursor.close()
    file.file.close()
    return None


async def get_image_by_id_member(id: int):
    try:
        cursor = mydb.cursor()
        sql = "SELECT image_portfolio FROM member WHERE id = %(id)s"
        cursor.execute(sql, {'id': id})
        result = cursor.fetchone()
        cursor.close()
        image = result[0]
        return image
    except mysql.connector.Error as e:
        print(e)


async def register_new_member(name: str):
    cursor = mydb.cursor()
    sql = "INSERT INTO member (username) VALUES (%s)"
    try:
        cursor.execute(sql, (name,))
        mydb.commit()
        id = cursor.lastrowid
    except mysql.connector.Error as exc:
        print(exc)
        return "ErrorSQL: the request was unsuccessful..."
    cursor.close()
    return id


async def get_member_by_username(username: str):
    member_record = namedtuple("Member",
                               ["id", "username", "firstname", "lastname", "description", "mail", "url_portfolio",
                                "date_validate", "date_deleted"])
    cursor = mydb.cursor()
    query = "SELECT {} FROM member WHERE username = %(username)s".format(", ".join(member_record._fields))
    cursor.execute(query, {'username': username})
    result = cursor.fetchone()
    cursor.close()
    if result is None:
        return None
    member = member_record._make(result)
    return MemberIn(id=member.id, username=member.username, firstname=member.firstname, lastname=member.lastname,
                    description=member.description, mail=member.mail, url_portfolio=member.url_portfolio)


async def register_token(access_token: str, refresh_token: str, id_user: int):
    cursor = mydb.cursor()
    query = "INSERT INTO session (token_session, token_refresh, id_member) VALUES (%s, %s, %s)"
    val = (access_token, refresh_token, id_user)
    try:
        cursor.execute(query, val)
        mydb.commit()
    except mysql.connector.Error:
        return "Error SQL : the request was unsuccessfully..."
    cursor.close()
    return None
