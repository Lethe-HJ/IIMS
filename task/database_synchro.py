from sqlalchemy import or_, between
from xd_REST.models.t_work_introduction import TWorkIntroduction as Intro
from xd_REST.models.t_daily_record import TDailyRecord as Daily
import xml.etree.ElementTree as ET
from .models import IntroId, DailyId, BlankIdHistory, session0, session1, session2
from datetime import datetime, timedelta

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


# intro数据同步==========================================================================================================


def query_intro_synchro_date():
    """
    查询副库中需要同步的intro数据
    :return:
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    intros = session1.query(Intro).filter(Intro.update_date.between(start_time, end_time)).all()
    return intros


def intro_old_new_filter(these_intros):
    """
    分离新旧intro数据
    :param these_intros:
    :return:
    """
    new_intros = []
    old_intros = []
    for intro in these_intros:
        blank_id = session2.query(BlankIdHistory.blank_id).order_by(BlankIdHistory.createdate.desc()).first()
        if intro.id > blank_id:
            new_intros.append(intro)
        else:
            old_intros.append(intro)
    return new_intros, old_intros


# 新intro数据同步----------------------------------------------------------------------------------------------------
def new_intro_synchro(intros):
    """
    新增副库中的新intro记录到主库
    :return: 新增后的id的前后变化 [{"pre": 212, "new": 113141}, ]
    """
    ids = []
    args = {}
    # 新增副库中的新intro记录到主库

    for intro in intros:
        id = {}
        id["vice_id"] = intro.id  # 记住副库的id值

        args["snumber"] = intro.snumber
        args["workaddress"] = intro.workaddress
        args["workproperty"] = intro.workproperty
        args["projectid"] = intro.projectid
        args["workintro"] = intro.workintro
        args["create_date"] = intro.create_date
        args["create_user"] = intro.create_user
        args["update_date"] = intro.update_date
        args["remarks"] = intro.remarks
        args["userid"] = intro.userid
        args["username"] = intro.username

        new_intro = Intro(**args)
        session0.add(new_intro)  # 将数据添加到目的表
        session0.flush()  # flush一下 获取id
        id["main_id"] = new_intro.id  # 记住主库id值
        session0.commit()
        session0.close()
        ids.append(id)  # 将id添加到ids中
    IntroId.edit_intro_ids(ids)  # 将ids保存到intro差异对照表
    return ids  # [{"main_id": 113141, "vice_id": 212}, ]


# 旧intro数据同步--------------------------------------------------------------------------------------------------------
def old_intro_synchro(intros):
    args = {}
    for intro in intros:
        main_id = IntroId.query_main_id(intro.id)
        the_intro = session0.query(Intro).filter_by(id=main_id)
        args["snumber"] = intro.snumber
        args["workaddress"] = intro.workaddress
        args["workproperty"] = intro.workproperty
        args["projectid"] = intro.projectid
        args["workintro"] = intro.workintro
        args["create_date"] = intro.create_date
        args["create_user"] = intro.create_user
        args["update_date"] = intro.update_date
        args["remarks"] = intro.remarks
        args["userid"] = intro.userid
        args["username"] = intro.username
        the_intro.update(args)
        session0.commit()


# daily数据同步==========================================================================================================

# 新daily数据同步----------------------------------------------------------------------------------------------------
def new_daily_synchro(dailies):
    args = dict()
    ids = []
    for daily in dailies:
        id = {}
        main_id = DailyId.query_main_id(dailies.workintroId)  # 根据日报的简介id从intro_id对照表中获取主库中的对应的intro_id
        args["WorkDate"] = daily.WorkDate
        args["Weeks"] = daily.Weeks
        args["DayInWeek"] = daily.DayInWeek
        args["JobDescription"] = daily.JobDescription
        args["WorkHours"] = daily.WorkHours
        args["WorkMatters"] = daily.WorkMatters
        args["StaffName"] = daily.StaffName
        args["ProjectName"] = daily.ProjectName
        args["DescripNumber"] = daily.DescripNumber
        new_daily = Daily(**args)
        session0.add(new_daily)
        session0.flush()
        id["main_id"] = new_daily.ID
        id["vice_id"] = daily.ID
        ids.append(id)
    DailyId.edit_daily_ids(ids)










def new_modify_add_daily(ids):
    """
    修改副库中新daily记录
    新增这些记录到主库
    :return:
    """
    intro_vice_id = [id0["vice_id"] for id0 in ids]
    intro_main_id = [id1["main_id"] for id1 in ids]
    ids = []
    # 查询需要修改工作简介id的日报记录
    dailies = session1.query(Daily).filter(Daily.workintroId.in_(intro_vice_id)).all()
    for daily in dailies:
        id = {}

        daily.workintroId = intro_main_id[intro_vice_id.index(daily.workintroId)]  # 将这个日报记录的工作简介id修改成主库中对应的id

        args = dict()
        args["WorkDate"] = daily.WorkDate
        args["Weeks"] = daily.Weeks
        args["DayInWeek"] = daily.DayInWeek
        args["JobDescription"] = daily.JobDescription
        args["WorkHours"] = daily.WorkHours
        args["WorkMatters"] = daily.WorkMatters
        args["StaffName"] = daily.StaffName
        args["ProjectName"] = daily.ProjectName
        args["DescripNumber"] = daily.DescripNumber
        args["ProjectID"] = daily.ProjectID
        args["isdelete"] = daily.isdelete
        args["createdate"] = daily.createdate
        args["createuser"] = daily.createuser
        args["updatedate"] = daily.updatedate
        args["updateuser"] = daily.updateuser
        args["workintroId"] = daily.workintroId
        args["userid"] = daily.userid

        the_daily = Daily(**args)
        session0.add(the_daily)  # 将数据添加到主库
        session0.flush()  # flush一下 获取id
        id["daily_main_id"] = the_daily.ID
        id["daily_vice_id"] = daily.ID
        ids.append(id)

        session0.commit()
        session0.close()
    DailyId.edit_daily_ids(ids)
    return ids


def new_daily_synchro():
    """
    修改副库中的新daily记录的工作简介id
    新增上述daily到主库
    :return:
    """
    pass





intro_id, daily_id, date_time = get_blank_id()

if __name__ == "__main__":

    intros_data = query_intro_synchro_date()  # 查询副库中需要同步的intro数据
    new_intro, old_intro = intro_old_new_filter(intros_data)
    intro_ids = new_intro_synchro(new_intro)
    daily_ids = new_modify_add_daily(intro_ids)

    # ids = intro_synchro()
