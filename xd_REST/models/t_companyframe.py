# coding: utf-8

from sqlalchemy import Integer, Date, Unicode, Numeric, exc, Table
from sqlalchemy import Column, DateTime, String, desc
from . import Base, metadata
from xd_REST import session
from xd_REST.models.t_staff import TStaff
import copy
from flask import g

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
            Column('Reserve', String(200, 'Chinese_PRC_CI_AS')),
            Column('staff', String(1024, 'Chinese_PRC_CI_AS')))


class CompanyFrame:
    def __init__(self):
        self.T_frame = t_T_CompanyFrame.columns
        self.frame_query = session.query(self.T_frame.ID, self.T_frame.Name, self.T_frame.staff, self.T_frame.IsLeaf
                                         , self.T_frame.AllParentId).order_by(self.T_frame.ID.desc()).all()
        # 查询ID, Name, staff, AllParentId

        self.frame_dict = self.frame_dict_init()

    def frame_dict_init(self):
        frame_dict = dict()
        for frame in self.frame_query:
            frame_dict[str(frame.ID)] = frame.Name
        return frame_dict

    def get_group(self, staff_id):

        label = []
        for frame in self.frame_query:  # 遍历查询结果
            staff_li = frame.staff.strip(',').split(',') if frame.staff else []  # 如果有staff 就分割成列表
            if str(staff_id) in staff_li:  # 如果目标id在这个列表中
                if frame.Name not in label:
                    label.append(frame.Name)  # 将这个记录的Name追加到其中
                parent_li = frame.AllParentId.strip(',').split(',')  # 获取它的全部父级id组成的的列表
                for parent_id in parent_li:  # 遍历这些父级
                    if parent_id in self.frame_dict and self.frame_dict[parent_id] not in label:
                        label.append(self.frame_dict[parent_id])
        label.reverse()
        return label[1:]

    def get_staff_li(self, frame_id):
        staff = session.query(self.T_frame.staff) \
            .filter(self.T_frame.ID == frame_id).first()
        staff_str = staff[0] if staff else ""
        staff_li = staff_str.strip(',').split(',')
        return staff_li


class FrameTree:
    def __init__(self, pattern):
        self.t_frame = t_T_CompanyFrame
        self.node = {  # 定义结点
            "ID": -1,
            "Name": "",
            "children": [],
            "children_li": [],
            "staff_li": [],
            "level": -1,
        }
        self.staff = {
            "ID": -1,
            "Name": "",
        }
        self.node_li = self.get_node_li()
        self.root = None
        self.pattern = pattern
        self.staff_record = dict()
        self.staff_record_init()

    def staff_record_init(self):
        staff = TStaff.get_all_staff()
        for stf in staff:
            self.staff_record[str(stf["id"])] = stf["name"]

    def get_node_li(self):
        """
        获取结点列表
        :return:
        """
        node_li = []
        frams = session.query(self.t_frame).all()
        for fram in frams:
            new_code = copy.deepcopy(self.node)
            new_code["ID"] = fram.ID
            new_code["Name"] = fram.Name
            new_code["children_li"] = fram.ChildId.strip(',').split(',') if fram.ChildId else []
            new_code["staff_li"] = fram.staff.strip(',').split(',') if fram.staff else []
            new_code["level"] = fram.Level
            node_li.append(new_code)
        return node_li

    def build_tree(self):
        """
        构造树
        :return:
        """
        self.root = self.node_li[0]
        self.build_sub_tree(self.root)
        return self.root

    def build_sub_tree(self, node):
        """
        递归构建子树
        :param node:
        :return:
        """
        self.add_staff(node)
        if node["children_li"] == []:
            return
        for i in range(0, len(self.node_li)):
            if str(self.node_li[i]["ID"]) in node["children_li"]:
                node["children"].append(self.node_li[i])  # 将字典添加进集合中
                self.build_sub_tree(node["children"][-1])

    def add_staff(self, node):
        if node["staff_li"] is not []:
            for staff_id in node["staff_li"]:
                staff = copy.deepcopy(self.staff)
                staff["ID"] = int(staff_id)
                # name_ob = session.query(TStaff.StaffName).filter_by(ID=staff["ID"]).first()
                # staff["Name"] = name_ob[0] if name_ob else ""
                staff["Name"] = self.staff_record[staff_id]
                node["children"].append(staff)







