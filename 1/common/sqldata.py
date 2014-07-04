#coding=utf-8
from django.db import connections, connection,transaction

def ExecuteSql(sql,db='default'):
    """
    执行SQL
    """
    if sql is None or sql == "":
        return

    cursor = connections[db].cursor()
    cursor.execute(sql)
    transaction.commit_unless_managed(using=db)
    cursor.close()
    return True


def SelectAllSql(sql,db='default'):
    """
    查询SQL多条数据
    """
    if sql is None or sql == "":
        return

    cursor = connections[db].cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    cursor.close()
    return fetchall


def SelectAllSqlByColumns(sql,columns,db='default'):
    """
    查询SQL多条数据并返回字典结果集
    """
    if sql is None or sql == "":
        return

    cursor = connections[db].cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    object_list = []
    if fetchall:
        for obj in fetchall:
            dict = {}
            for index,c in enumerate(columns):
                dict[c] = obj[index]
            object_list.append(dict)
    cursor.close()
    return object_list


def SelectOneSql(sql,db='default'):
    """
   查询SQL单条数据
    """
    if sql is None or sql == "":
        return


    cursor = connections[db].cursor()
    cursor.execute(sql)
    fetchone = cursor.fetchone()
    cursor.close()
    return fetchone


def SelectOneSqlByColumns(sql,columns,db='default'):
    """
    查询SQL单条数据并返回字典结果集
    """
    if sql is None or sql == "":
        return
    cursor = connections[db].cursor()
    cursor.execute(sql)
    fetchone = cursor.fetchone()
    object = {}
    if fetchone:
        for index, c in enumerate(columns):
            object[c] = fetchone[index]
    cursor.close()
    return object


def callProc(proname, params, db='defatul'):
    """
    功能说明：                调用存储过程
    -----------------------------------------------
    proname:    存储过程名字
    params:     输入参数元组或列表
    """
    cc = connections[db].cursor()
    cc.callproc(proname, params)
    print u'该存储[%s]过程影响的行数：%s' % (proname, cc.rowcount)
    try:
        transaction.commit_unless_managed(using=db)     # 事务提交
    except Exception, e:
        pass
    data = cc.fetchall()
    cc.close()
    return data


