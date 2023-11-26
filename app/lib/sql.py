from contextlib import contextmanager
from collections import namedtuple
from typing import Optional, List

from fastapi import UploadFile

from app.models import *

from app import settings
from datetime import datetime, timedelta
import mysql.connector

from app.models.member_has_category import MemberHasCategoryOut


@contextmanager
def get_cursor(commit_on_exit=True):
    mydb = mysql.connector.connect(
        host=settings.HOST,
        user=settings.USER,
        password=settings.PASSWORD,
        database=settings.DATABASE,
        port=settings.PORT
    )

    cursor = mydb.cursor()
    try:
        yield cursor
        if commit_on_exit:
            mydb.commit()
    except Exception as e:
        mydb.rollback()
        raise e
    finally:
        cursor.close()
        mydb.close()


async def get_members():
    with get_cursor() as cursor:
        cursor.execute("SELECT member.id, member.username, member.url_portfolio, member.date_validate, "
                       "member.date_deleted, GROUP_CONCAT(category.name) FROM member, member_has_category, category WHERE "
                       "member.id=member_has_category.id_member AND member_has_category.id_category=category.id GROUP BY "
                       "member.id")
        result = cursor.fetchall()
        member_record = namedtuple("Member", ["id", "username", "url_portfolio", "date_validate", "date_deleted", "name"])
        return [MemberWithCategory(id_member=member.id, username=member.username, url_portfolio=member.url_portfolio,
                                   category_name=member.name) for member in map(member_record._make, result)
                if member.date_validate is not None and member.date_deleted is None]


async def get_member_by_id(id_member):
    with get_cursor() as cursor:
        member_record = namedtuple("Member",
                                   ["id", "username", "firstname", "lastname", "description", "mail", "url_portfolio",
                                    "date_validate", "date_deleted"])
        query = "SELECT {} FROM member WHERE id = %(id)s".format(", ".join(member_record._fields))
        cursor.execute(query, {'id': id_member})
        result = cursor.fetchone()
        if result is None:
            return None
        member = member_record._make(result)
        return MemberIn(id=member.id, username=member.username, firstname=member.firstname, lastname=member.lastname,
                        description=member.description, mail=member.mail, url_portfolio=member.url_portfolio)


async def create_member(member: MemberIn):
    with get_cursor() as cursor:
        sql = "INSERT INTO member (username, firstname, lastname, description, mail, url_portfolio) VALUES (%s, %s, %s, " \
              "%s, %s, %s)"
        val = (member.username, member.firstname, member.lastname, member.description, member.mail, member.url_portfolio)
        try:
            cursor.execute(sql, val)
        except mysql.connector.Error:
            return "ErrorSQL: the request was unsuccessful..."
        id = cursor.lastrowid
        return id


async def patch_member_update(member: MemberOut):
    with get_cursor() as cursor:
        sql = "UPDATE member SET firstname = %s, lastname = %s, description = %s, mail = %s, url_portfolio " \
              "= %s WHERE id = %s"
        val = (member.firstname, member.lastname, member.description, member.mail, member.url_portfolio, member.id)
        try:
            cursor.execute(sql, val)
        except mysql.connector.Error:
            return "ErrorSQL: the request was unsuccessful..."
        return None


async def get_categories():
    with get_cursor() as cursor:
        cursor.execute("SELECT id, name FROM category")
        result = cursor.fetchall()
        category_record = namedtuple("Category", ["id", "name"])
        return [Category(id=category.id, name=category.name) for category in
                map(category_record._make, result)]


async def post_category(category: CategoryOut):
    with get_cursor() as cursor:
        sql = "INSERT INTO category (name) VALUES (%s)"
        val = [category.name]
        try:
            cursor.execute(sql, val)
        except mysql.connector.Error as exc:
            return "ErrorSQL: the request was unsuccessful..."
        return None


async def get_members_category(name_category: str):
    with get_cursor() as cursor:
        sql = "SELECT member.* FROM member, member_has_category, category WHERE member.id = member_has_category.id_member " \
              "AND member_has_category.id_category = category.id AND category.name = %(name)s"
        cursor.execute(sql, {"name": name_category})
        result = cursor.fetchall()
        member_record = namedtuple("Member",
                                   ["id", "username", "lastname", "firstname", "description", "mail", "date_validate",
                                    "date_deleted", "url_portfolio"])
        return [GetMembers(id=member.id, username=member.username, url_portfolio=member.url_portfolio) for member in
                map(member_record._make, result)
                if member.date_validate is not None and member.date_deleted is None]


async def return_id_category_by_name(name: str):
    with get_cursor() as cursor:
        sql = "SELECT id FROM category WHERE name = %(name)s"
        try:
            cursor.execute(sql, {"name": name})
            result = cursor.fetchone()
            return result[0]
        except TypeError:
            return "ErrorSQL : the request was unsuccessful"


async def post_add_category_on_member(member: MemberHasCategory):
    with get_cursor() as cursor:
        sql = """
        INSERT INTO member_has_category (id_member, id_category) VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE id_member=id_member 
        """
        try:
            values = []
            for cate in member.id_category:
                values.append([member.id_member, cate])
            cursor.executemany(sql, values)
        except mysql.connector.Error:
            return "ErrorSQL: the request was unsuccessful..."
        return None


async def get_network_of_member_by_id(id_member: int):
    with get_cursor() as cursor:
        sql = "SELECT network.name, member_has_network.url, member_has_network.id_network FROM network, member_has_network, member WHERE member.id = " \
              "member_has_network.id_member AND member_has_network.id_network = network.id AND member.id = %(id)s"
        cursor.execute(sql, {'id': id_member})
        result = cursor.fetchall()
        network_record = namedtuple("Network", ["name", "url", "id_network"])
        return [GetMemberHasNetwork(name=network.name, url=network.url, id_network=network.id_network) for network in map(network_record._make, result)]


async def get_category_of_member_by_id(id_member: int):
    with get_cursor() as cursor:
        sql = "SELECT category.name FROM category, member, member_has_category WHERE member.id = " \
              "member_has_category.id_member AND member_has_category.id_category = category.id AND member.id = %(id)s"
        cursor.execute(sql, {'id': id_member})
        result = cursor.fetchall()
        category_record = namedtuple("Category", ["name"])
        return [CategoryOut(name=category.name) for category in map(category_record._make, result)]


async def get_member_has_category_by_id_member(id_member: int):
    with get_cursor() as cursor:
        sql = "SELECT member_has_category.id_member, category.name, member_has_category.id_category FROM " \
              "member, member_has_category, category WHERE member.id = member_has_category.id_member AND " \
              "member_has_category.id_category = category.id AND member.id = %(id)s"
        cursor.execute(sql, {'id': id_member})
        result = cursor.fetchall()
        category_record = namedtuple("MemberHasCategory", ["id_member","name","id_category"])
        return [MemberHasCategoryOut(id_member=category.id_member, name=category.name, id_category=category.id_category) for category in map(category_record._make, result)]


async def get_network():
    with get_cursor() as cursor:
        sql = "SELECT * FROM network"
        cursor.execute(sql)
        result = cursor.fetchall()
        network_record = namedtuple("Network", ["id", "name"])
        return [Network(id=network.id, name=network.name) for network in map(network_record._make, result)]


async def post_network_on_member(member: MemberHasNetwork):
    with get_cursor() as cursor:
        sql = "INSERT INTO member_has_network (id_member, id_network, url) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE " \
              "url = VALUES(url)"
        try:
            values = []
            for url, network in zip(member.url, member.id_network):
                if url != "" and url is not None:
                    values.append([member.id_member, network, url])
            cursor.executemany(sql, values)
        except mysql.connector.Error as e:
            return "ErrorSQL: the request was unsuccessful..."
        return None


async def delete_category_delete_by_member(member: MemberHasCategory):
    with get_cursor() as cursor:
        sql = "DELETE FROM member_has_category WHERE id_member = %s AND id_category = %s"
        try:
            values = []
            for cate in member.id_category:
                values.append([member.id_member, cate])
            cursor.executemany(sql, values)
        except mysql.connector.Error:
            return "ErrorSQL: the request was unsuccessful..."
        return None


async def delete_network_delete_by_member(member: MemberHasNetworkIn):
    with get_cursor() as cursor:
        sql = "DELETE FROM member_has_network WHERE id_member = %s AND id_network = %s"
        try:
            values = []
            for network in member.id_network:
                values.append([member.id_member, network])
            cursor.executemany(sql, values)
        except mysql.connector.Error:
            return "ErrorSQL : the request was unsuccessful..."
        return None


async def add_new_network(name: NetworkOut):
    with get_cursor() as cursor:
        sql = "INSERT INTO network (name) VALUES (%s)"
        val = [name.name]
        try:
            cursor.execute(sql, val)
        except mysql.connector.Error:
            cursor.close()
            return "ErrorSQL: the request was unsuccessful..."
        return True


async def add_image_portfolio(file: UploadFile, id_member: int):
    with get_cursor() as cursor:
        sql = "UPDATE member SET image_portfolio = %s WHERE id = %s"
        try:
            cursor.execute(sql, (file.file.read(), id_member))
        except mysql.connector.Error:
            return "ErrorSQL : the request was unsuccessful..."
        file.file.close()
        return None


async def get_image_by_id_member(id: int):
    with get_cursor() as cursor:
        try:
            sql = "SELECT image_portfolio FROM member WHERE id = %(id)s"
            cursor.execute(sql, {'id': id})
            result = cursor.fetchone()
            image = result[0]
            return image
        except mysql.connector.Error as e:
            print(e)


async def register_new_member(name: str):
    with get_cursor() as cursor:
        sql = "INSERT INTO member (username) VALUES (%s)"
        try:
            cursor.execute(sql, (name,))
            id = cursor.lastrowid
        except mysql.connector.Error as exc:
            return "ErrorSQL: the request was unsuccessful..."
        return id


async def get_member_by_username(username: str):
    with get_cursor() as cursor:
        member_record = namedtuple("Member",
                                   ["id", "username", "firstname", "lastname", "description", "mail", "url_portfolio",
                                    "date_validate", "date_deleted"])
        query = "SELECT {} FROM member WHERE username = %(username)s".format(", ".join(member_record._fields))
        cursor.execute(query, {'username': username})
        result = cursor.fetchone()
        if result is None:
            return None
        member = member_record._make(result)
        return MemberIn(id=member.id, username=member.username, firstname=member.firstname, lastname=member.lastname,
                        description=member.description, mail=member.mail, url_portfolio=member.url_portfolio)


async def register_token(access_token: str, refresh_token: str, id_user: int):
    with get_cursor() as cursor:
        query = "INSERT INTO session (token_session, token_refresh, id_member) VALUES (%s, %s, %s)"
        val = (access_token, refresh_token, id_user)
        try:
            cursor.execute(query, val)
        except mysql.connector.Error:
            return "Error SQL : the request was unsuccessfully..."
        return None


async def get_session(id_user: int):
    with get_cursor() as cursor:
        session_record = namedtuple("Session",["access_token","refresh_token","id_member","date_created"])
        query = "SELECT * FROM session WHERE id_member = %(id_member)s"
        try:
            cursor.execute(query, {'id_member': id_user})
            result = cursor.fetchone()
            if not result:
                return None
            else:
                session = session_record._make(result)
                return session
        except mysql.connector.Error:
            return None


async def delete_session(id_user: int):
    with get_cursor() as cursor:
        query = "DELETE FROM session WHERE id_member = %(id_member)s"
        try:
            cursor.execute(query, {"id_member": id_user})
        except mysql.connector.Error:
            return "Error SQL"
        return None


async def verif_session(session: Session):
    with get_cursor() as cursor:
        session_record = namedtuple("Session", ["access_token", "refresh_token", "id_member","date_created"])
        query = "SELECT * FROM session WHERE id_member = %(id_member)s"
        try:
            cursor.execute(query, {'id_member': session["user_id"]})
            result = cursor.fetchone()
            if not result:
                return None
            else:
                session_verif = session_record._make(result)
                print(session_verif)
                if session_verif.access_token == session["access_token"] and session_verif.refresh_token == session["refresh_token"]:
                    temps_date = timedelta(minutes=60)
                    if session_verif.date_created + temps_date > datetime.now():
                        return True
                    else:
                        return None
                else:
                    return None
        except mysql.connector.Error:
            return None


async def is_admin(id_user: int):
    with get_cursor() as cursor:
        query = "SELECT is_admin FROM member WHERE id = %(id)s"
        try:
            cursor.execute(query, {"id": id_user})
            result = cursor.fetchone()
            if result and result[0] == 1:
                return True
            else:
                return False
        except mysql.connector.Error:
            return False


async def delete_table_member_has_category(name: str):
    with get_cursor() as cursor:
        sql = "DELETE FROM member_has_category WHERE id_category = (" \
              "SELECT id FROM category WHERE name = %(name)s)"
        try:
            cursor.execute(sql, {"name": name})
        except mysql.connector.Error:
            return "ErrorSQL : ..."
        return None


async def delete_category(name: str):
    with get_cursor() as cursor:
        await delete_table_member_has_category(name)
        sql = "DELETE FROM category WHERE name = %(name)s"
        try:
            cursor.execute(sql, {"name": name})
        except mysql.connector.Error:
            return "ErrorSQL : the request was unsuccessful..."
        return None


async def delete_table_member_has_network(name: str):
    with get_cursor() as cursor:
        sql = "DELETE FROM member_has_network WHERE id_network = (" \
              "SELECT id FROM network WHERE name = %(name)s)"
        try:
            cursor.execute(sql, {"name": name})
        except mysql.connector.Error:
            return "ErrorSQL : ..."
        return None


async def delete_network(name: str):
    with get_cursor() as cursor:
        await delete_table_member_has_network(name)
        sql = "DELETE FROM network WHERE name = %(name)s"
        try:
            cursor.execute(sql, {"name": name})
        except mysql.connector.Error:
            return "ErrorSQL : the request was unsuccessful..."
        return None


async def get_all_member_admin() -> List[MemberOut]:
    with get_cursor() as cursor:
        cursor.execute("SELECT id, username, firstname, lastname, description, mail, url_portfolio, date_validate, "
                       "date_deleted FROM member")
        column_names = cursor.column_names
        MemberTuple = namedtuple("Member", column_names)
        return [MemberOut(id=member.id, username=member.username, firstname=member.firstname, lastname=member.lastname,
                          description=member.description, mail=member.mail, url_portfolio=member.url_portfolio,
                          date_activated=member.date_validate, date_deleted=member.date_deleted)
                for member in map(MemberTuple._make, cursor.fetchall())]


async def validate_member(id_member: int):
    with get_cursor() as cursor:
        sql = "UPDATE member SET date_validate = NOW() WHERE id = %(id)s"
        try:
            cursor.execute(sql, {"id": id_member})
        except mysql.connector.Error:
            return "ErrorSQL: the request was unsuccessful..."
        return None
        

async def ban_member(id_member: int):
    with get_cursor() as cursor:
        sql = "UPDATE member SET date_deleted = NOW() WHERE id = %(id)s"
        try:
            cursor.execute(sql, {"id": id_member})
        except mysql.connector.Error:
            return "ErrorSQL: the request was unsuccessful..."
        return None


async def unban_member(id_member: int):
    with get_cursor() as cursor:
        sql = "UPDATE member SET date_deleted = null WHERE id = %(id)s"
        try:
            cursor.execute(sql, {"id": id_member})
        except mysql.connector.Error:
            return "ErrorSQL: the request was unsuccessful..."
        return None
