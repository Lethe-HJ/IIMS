# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Integer, LargeBinary, Numeric, String, Table, Unicode, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TBusinessUnit(Base):
    __tablename__ = 'T_BusinessUnit'

    ID = Column(Integer, primary_key=True)
    BusinessUnit = Column(Unicode(20), nullable=False)
    SubDepartment = Column(Unicode(50))
    Createdate = Column(DateTime)
    Updatedate = Column(DateTime)


t_T_CompanyFrame = Table(
    'T_CompanyFrame', metadata,
    Column('ID', Integer),
    Column('Level', Integer),
    Column('Name', String(30, 'Chinese_PRC_CI_AS')),
    Column('ParentId', Integer),
    Column('AllParentId', String(1024, 'Chinese_PRC_CI_AS')),
    Column('IsLeaf', Integer),
    Column('ChildId', String(1024, 'Chinese_PRC_CI_AS')),
    Column('AllChildId', String(1024, 'Chinese_PRC_CI_AS')),
    Column('TreeNodeName', String(30, 'Chinese_PRC_CI_AS')),
    Column('IsShow', Integer),
    Column('Reserve', String(200, 'Chinese_PRC_CI_AS'))
)


class TConcernStaff(Base):
    __tablename__ = 'T_ConcernStaff'

    StaffID = Column(Integer, primary_key=True)
    ConcernIDGroup = Column(Unicode(1000))


class TDailyRecord(Base):
    __tablename__ = 'T_DailyRecord'

    ID = Column(Integer, primary_key=True)
    WorkDate = Column(Date)
    Weeks = Column(Integer)
    DayInWeek = Column(Unicode(50))
    JobDescription = Column(Unicode(1000))
    WorkHours = Column(Numeric(18, 1))
    WorkMatters = Column(String(3000, 'Chinese_PRC_CI_AS'))
    StaffName = Column(Unicode(20), nullable=False)
    ProjectName = Column(Unicode(100))
    DescripNumber = Column(Integer)
    ProjectID = Column(Unicode(50))
    isdelete = Column(Integer)
    createdate = Column(DateTime)
    createuser = Column(Integer)
    updatedate = Column(DateTime)
    updateuser = Column(Integer)
    workintroId = Column(Integer)
    userid = Column(Integer)


class TOnBusinessDailyRecord(Base):
    __tablename__ = 'T_OnBusinessDailyRecord'

    ID = Column(Integer, primary_key=True)
    WorkDate = Column(Date)
    StaffName = Column(Unicode(20), nullable=False)
    Weeks = Column(Integer)
    DayInWeek = Column(Unicode(50))
    Department = Column(Unicode(10))
    OnBusinessPlace = Column(Unicode(20))
    ProjectAlias = Column(Unicode(100))
    ProjectID = Column(Unicode(50))
    WorkMatters = Column(Unicode(1000))
    Isdelete = Column(Integer)
    Createdate = Column(DateTime)
    Updatedate = Column(DateTime)
    Staffid = Column(Integer)


class TOnBusinessDailyRecordNew(Base):
    __tablename__ = 'T_OnBusinessDailyRecordNew'

    ID = Column(Integer, primary_key=True)
    WorkDate = Column(DateTime, nullable=False)
    StartDate = Column(DateTime)
    Weeks = Column(Integer)
    StaffName = Column(Unicode(20), nullable=False)
    ClientName = Column(Unicode(100))
    Department = Column(Unicode(10))
    OnBusinessPlace = Column(Unicode(20))
    WorkMatters = Column(String(3000, 'Chinese_PRC_CI_AS'))
    NewDemand = Column(Unicode(1000))
    MatterRecords = Column(String(2000, 'Chinese_PRC_CI_AS'))
    Staffid = Column(Integer)
    Isdelete = Column(Integer)
    Createdate = Column(DateTime)
    Updatedate = Column(DateTime)
    BusinessUnit = Column(Unicode(20))


class TProjectSummary(Base):
    __tablename__ = 'T_ProjectSummary'

    ID = Column(Unicode(50), primary_key=True)
    ProductType = Column(Unicode(50))
    SNumber = Column(Integer)
    ProjectNumber = Column(Unicode(50))
    ProjectName = Column(Unicode(100))
    ProductModel = Column(Unicode(100))
    ProjectManager = Column(Unicode(50))
    Classifiation = Column(Unicode(50))
    ProjectAlias = Column(Unicode(100), index=True)
    OAOder = Column(Unicode(100))
    isdelete = Column(Integer, server_default=text("((0))"))
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    create_user = Column(Unicode(50))
    update_user = Column(Unicode(50))
    ProjectStatus = Column(Integer, server_default=text("((0))"))
    ProjectTypeID = Column(Integer)
    remarks = Column(Unicode(200))
    enteringdate = Column(Date)
    Status = Column(Unicode(10))
    leadparty = Column(Unicode(50))
    EndTime = Column(DateTime)
    ErpID = Column(Unicode(50))
    NewOrOldID = Column(Integer, server_default=text("((1))"))


class TProjectSummaryCopy(Base):
    __tablename__ = 'T_ProjectSummary_copy'

    ID = Column(Unicode(50), primary_key=True)
    ProductType = Column(Unicode(50))
    SNumber = Column(Integer)
    ProjectNumber = Column(Unicode(50))
    ProjectName = Column(Unicode(100))
    ProductModel = Column(Unicode(100))
    ProjectManager = Column(Unicode(50))
    Classifiation = Column(Unicode(50))
    ProjectAlias = Column(Unicode(100), index=True)
    OAOder = Column(Unicode(100))
    isdelete = Column(Integer, server_default=text("((0))"))
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    create_user = Column(Unicode(50))
    update_user = Column(Unicode(50))
    ProjectStatus = Column(Integer, server_default=text("((0))"))
    ProjectTypeID = Column(Integer)
    remarks = Column(Unicode(200))
    enteringdate = Column(Date)
    Status = Column(Unicode(10))
    leadparty = Column(Unicode(50))
    EndTime = Column(DateTime)
    ErpID = Column(Unicode(50))


class TProjectType(Base):
    __tablename__ = 'T_ProjectType'

    id = Column(Integer, primary_key=True)
    TypeName = Column(Unicode(50))
    remarks = Column(Unicode(200))
    create_date = Column(DateTime)
    create_user = Column(Integer)


class TProjectTypeCopy(Base):
    __tablename__ = 'T_ProjectType_copy'

    id = Column(Integer, primary_key=True)
    TypeName = Column(Unicode(50))
    remarks = Column(Unicode(200))
    create_date = Column(DateTime)
    create_user = Column(Integer)


class TSex(Base):
    __tablename__ = 'T_Sex'

    id = Column(Integer, primary_key=True)
    sex = Column(Unicode(20))
    remarks = Column(Unicode(200))
    create_date = Column(DateTime)
    create_user = Column(Integer)


class TSexCopy(Base):
    __tablename__ = 'T_Sex_copy'

    id = Column(Integer, primary_key=True)
    sex = Column(Unicode(20))
    remarks = Column(Unicode(200))
    create_date = Column(DateTime)
    create_user = Column(Integer)
    Image = Column(LargeBinary)


class TStaff(Base):
    __tablename__ = 'T_Staff'

    ID = Column(Integer, primary_key=True)
    StaffName = Column(Unicode(20))
    Department = Column(Unicode(20))
    SerialNum = Column(Integer)
    LoginPassword = Column(Unicode(50))
    Classifiation = Column(Unicode(50))
    sex = Column(Integer)
    StaffCode = Column(Unicode(50))
    StaffPhone = Column(Unicode(20))
    position = Column(Unicode(20))
    staffrole = Column(Integer)
    isdelete = Column(Integer)
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    create_user = Column(Integer)
    update_user = Column(Integer)
    StaffStatus = Column(Integer)
    remarks = Column(Unicode(200))
    isUpdate = Column(Integer)
    BusinessUnit = Column(Integer)
    DepartMentId = Column(Integer)
    StaffAuth = Column(Integer)
    ManageDepartmentId = Column(String(4096, 'Chinese_PRC_CI_AS'))
    ManageStaffId = Column(String(4096, 'Chinese_PRC_CI_AS'))


class TStaffAuth(Base):
    __tablename__ = 'T_StaffAuth'

    id = Column(Integer, primary_key=True, unique=True)
    AuthName = Column(Unicode(50))
    Level = Column(Integer)
    Auth = Column(Integer)


class TStaffStatu(Base):
    __tablename__ = 'T_StaffStatus'

    id = Column(Integer, primary_key=True)
    StatusName = Column(Unicode(50))
    remarks = Column(Unicode(200))
    create_date = Column(DateTime)
    create_user = Column(Integer)


t_T_TmpManageGrp = Table(
    'T_TmpManageGrp', metadata,
    Column('ID', Integer, nullable=False),
    Column('ManagerID', Integer, nullable=False),
    Column('GroupMember', Unicode(1000)),
    Column('Reamrk', Unicode(100)),
    Column('Createdate', DateTime),
    Column('Updatedate', DateTime)
)


class TVersionInfo(Base):
    __tablename__ = 'T_VersionInfo'

    Version = Column(Unicode(50), primary_key=True)
    VersionInfo = Column(Unicode(500))


class TWorkAddres(Base):
    __tablename__ = 'T_WorkAddress'

    id = Column(Integer, primary_key=True)
    AddressName = Column(Unicode(50))
    remarks = Column(Unicode(200))
    create_date = Column(DateTime)
    create_user = Column(Integer)


class TWorkIntroduction(Base):
    __tablename__ = 'T_WorkIntroduction'

    id = Column(Integer, primary_key=True)
    snumber = Column(Integer)
    workaddress = Column(Integer, server_default=text("((0))"))
    workproperty = Column(Integer)
    projectid = Column(Unicode(50))
    workintro = Column(Unicode(100))
    create_date = Column(DateTime)
    create_user = Column(Integer)
    update_date = Column(DateTime)
    remarks = Column(Unicode(100))
    userid = Column(Integer)
    username = Column(Unicode(50))


class TWorkIntroductionCopy(Base):
    __tablename__ = 'T_WorkIntroduction_copy'

    id = Column(Integer, primary_key=True)
    snumber = Column(Integer)
    workaddress = Column(Integer, server_default=text("((0))"))
    workproperty = Column(Integer)
    projectid = Column(Unicode(50))
    workintro = Column(Unicode(100))
    create_date = Column(DateTime)
    create_user = Column(Integer)
    update_date = Column(DateTime)
    remarks = Column(Unicode(100))
    userid = Column(Integer)
    username = Column(Unicode(50))


class TWorkProperty(Base):
    __tablename__ = 'T_WorkProperty'

    id = Column(Integer, primary_key=True)
    workpropertyname = Column(Unicode(50))
    remarks = Column(Unicode(200))
    create_date = Column(DateTime)
    create_user = Column(Integer)


class TFollow(Base):
    __tablename__ = 'T_follow'

    id = Column(Integer, primary_key=True)
    Projectid = Column(Unicode(50))
    userid = Column(Integer)
    create_date = Column(DateTime)


class TRole(Base):
    __tablename__ = 'T_role'

    id = Column(Integer, primary_key=True)
    role = Column(Unicode(50))
    remarks = Column(Unicode(200))
    create_date = Column(DateTime)
    create_user = Column(Integer)
