from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from sqlalchemy import or_, between
import pymssql
from xd_REST.models.t_work_introduction import TWorkIntroduction as Intro
from xd_REST.models.t_daily_record import TDailyRecord as Daily
import xml.etree.ElementTree as ET

# 主库
SQLALCHEMY_DATABASE_URI0 = 'mssql+pymssql://sa:wVYV7denNPOJntZ@47.106.83.135:1433/workdailyformalCopy?charset=utf8'
engine0 = create_engine(SQLALCHEMY_DATABASE_URI0)
DBsession0 = sessionmaker(bind=engine0)
session0 = DBsession0()

# 副库
SQLALCHEMY_DATABASE_URI1 = 'mssql+pymssql://sa:wVYV7denNPOJntZ@47.106.83.135:1433/workdailyformal?charset=utf8'
engine1 = create_engine(SQLALCHEMY_DATABASE_URI1)
DBsession1 = sessionmaker(bind=engine1)
session1 = DBsession1()

tree = ET.parse('record.xml')
root = tree.getroot()


# 新旧数据界限============================================================================================================
def add_blank_id(intro, daily):
    blank = ET.Element('blank')
    intro_blank_id = ET.SubElement(blank, 'intro_id')
    intro_blank_id.text = str(intro)
    daily_blank_id = ET.SubElement(blank, 'daily_id')
    daily_blank_id.text = str(daily)
    date_blank_time = ET.SubElement(blank, 'date_time')
    date_blank_time.text = str(datetime.now())
    root.append(blank)
    tree.write('record.xml')
    return True


def get_blank_id():
    last_blank = root.findall('blank')[-1]
    intro_blank_id = last_blank.find('intro_id').text
    daily_blank_id = last_blank.find('daily_id').text
    date_blank_time = last_blank.find('date_time').text
    return intro_blank_id, daily_blank_id, date_blank_time


# 数据同步===============================================================================================================
def query_intro_synchro_date():
    """
    查询副库中需要同步的intro数据
    :return:
    """
    end_time = datetime.now()
    end_time_str = str(end_time)[:22]
    start_time = end_time - timedelta(days=7)
    start_time_str = str(start_time)[:22]
    sql_0 = """
            SELECT *
            FROM T_WorkIntroduction
            WHERE update_date BETWEEN '{0}' AND '{1}';
        """.format(start_time_str, end_time_str)
    # 在副库中查询新纪录
    intros = session1.execute(sql_0).fetchall()
    return intros


def new_intro_synchro(intros):
    """
    新增副库中的新intro记录到主库
    :return: 新增后的id的前后变化 [{"pre": 212, "new": 113141}, ]
    """
    ids = []
    # 新增副库中的新intro记录到主库
    for intro in intros:
        id = {}
        id["pre"] = intro[0]  # 记住原id值
        intro = intro[1:]  # 丢掉id值
        args = {}
        args["snumber"] = intro[0]
        args["workaddress"] = intro[1]
        args["workproperty"] = intro[2]
        args["projectid"] = intro[3]
        args["workintro"] = intro[4]
        args["create_date"] = intro[5]
        args["create_user"] = intro[6]
        args["update_date"] = intro[7]
        args["remarks"] = intro[8]
        args["userid"] = intro[9]
        args["username"] = intro[10]
        new_intro = Intro(**args)
        session0.add(new_intro)  # 将数据添加到目的表
        session0.flush()  # flush一下 获取id
        id["new"] = new_intro.id  # 记住新id值
        session0.commit()
        ids.append(id)  # 将id添加到ids中
    return ids  # [{"pre": 212, "new": 113141}, ]


def new_modify_add_daily(ids):
    """
    修改副库中新daily记录
    新增这些记录到主库
    :return:
    """
    pre_ids = [id["pre"] for id in ids]
    new_ids = [id["new"] for id in ids]
    # 查询需要修改工作简介id的记录
    dailies = session1.query(Daily).filter(Daily.workintroId.in_(pre_ids)).all()
    for daily in dailies:
        pre_daily = session1.query(Daily).filter_by(ID=daily.ID).first()
        del daily.ID
        daily.workintroId = new_ids[pre_ids.index(daily.workintroId)]  # 将这个工作简介id修改成对应的id
        session0.add(daily)  # 将数据添加到主库
        session0.flush()  # flush一下 获取id
        pre_daily.ID = daily.id  # 更新副库记录中的id值 与主库一致
        pre_daily.workintroId = daily.id  # 更新副库记录中的workintroid值 与主库一致
        session1.commit()  # 更新副库记录






def new_daily_synchro():
    """
    修改副库中的新daily记录的工作简介id
    新增上述daily到主库
    :return:
    """
    pass





intro_id, daily_id, date_time = get_blank_id()

if __name__ == "__main__":
    add_blank_id(1, 20)
    intros_data = query_intro_synchro_date()  # 查询副库中需要同步的intro数据
    ids_record = new_intro_synchro(intros_data)
    new_modify_add_daily(ids_record)
    # ids = intro_synchro()
