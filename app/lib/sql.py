from collections import namedtuple
from app.models import GetMembers, MemberIn, Category, CategoryOut, MemberWithCategory

from app import settings
import mysql.connector

mydb = mysql.connector.connect(
    host=settings.HOST,
    user=settings.USER,
    password=settings.PASSWORD,
    database=settings.DATABASE,
    port=settings.PORT
)


def get_members():
    cursor = mydb.cursor()
    cursor.execute("SELECT member.id, member.username, member.url_portfolio, member.date_validate, "
                   "member.date_deleted, category.name FROM member, member_has_category, category WHERE "
                   "member.id=member_has_category.id_member AND member_has_category.id_category=category.id")
    result = cursor.fetchall()
    member_record = namedtuple("Member", ["id", "username", "url_portfolio", "date_validate", "date_deleted", "name"])
    cursor.close()
    return [MemberWithCategory(id_member=member.id, username=member.username, url_portfolio=member.url_portfolio, category_name=member.name) for member in map(member_record._make, result)
            if member.date_validate is not None and member.date_deleted is None]


def get_member_by_id(id_member):
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
    return MemberIn(id=member.id, username=member.username, firstname=member.firstname, lastname=member.lastname, description=member.description, mail=member.mail, url_portfolio=member.url_portfolio)


def post_member(member: MemberIn):
    cursor = mydb.cursor()
    sql = "INSERT INTO member (username, firstname, lastname, description, mail, url_portfolio) VALUES (%s, %s, %s, " \
          "%s, %s, %s)"
    val = (member.username, member.firstname, member.lastname, member.description, member.mail, member.url_portfolio)
    try:
        cursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as exc:
        print(exc)
        return "ErrorSQL: the request was unsuccessful..."
    cursor.close()
    return None


def get_categories():
    cursor = mydb.cursor()
    cursor.execute("SELECT id, name FROM category")
    result = cursor.fetchall()
    category_record = namedtuple("Category", ["id", "name"])
    cursor.close()
    return [Category(id=category.id, name=category.name) for category in
            map(category_record._make, result)]


def post_category(category: CategoryOut):
    cursor = mydb.cursor()
    sql = "INSERT INTO category (name) VALUES (%s)"
    val = [category.name]
    try:
        cursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as exc:
        print(exc)
        return "ErrorSQL: the request was unsuccessful..."
    cursor.close()
    return None


def get_members_category(name_category: str):
    cursor = mydb.cursor()
    sql = "SELECT member.* FROM member, member_has_category, category WHERE member.id = member_has_category.id_member " \
          "AND member_has_category.id_category = category.id AND category.name = %(name)s"
    cursor.execute(sql, {"name": name_category})
    result = cursor.fetchall()
    member_record = namedtuple("Member", ["id", "username", "lastname", "firstname", "description", "mail", "date_validate", "date_deleted", "url_portfolio"])
    cursor.close()
    return [GetMembers(id=member.id, username=member.username, url_portfolio=member.url_portfolio) for member in
            map(member_record._make, result)
            if member.date_validate is not None and member.date_deleted is None]
