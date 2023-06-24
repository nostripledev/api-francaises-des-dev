from collections import namedtuple
from app.models import GetMembers, MemberIn

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
    cursor.execute("SELECT id, username, url_portfolio, date_validate, date_deleted FROM member")
    result = cursor.fetchall()
    member_record = namedtuple("Member", ["id", "username", "url_portfolio", "date_validate", "date_deleted"])
    cursor.close()
    return [GetMembers(id=member.id, username=member.username, url_portfolio=member.url_portfolio) for member in map(member_record._make, result)
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
    sql = "INSERT INTO member (username, firstname, lastname, description, mail, url_portfolio) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (member.username, member.firstname, member.lastname, member.description, member.mail, member.url_portfolio)
    try:
        cursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as exc:
        print(exc)
        return "ErrorSQL: the request was unsuccessful..."
    cursor.close()
    return None
