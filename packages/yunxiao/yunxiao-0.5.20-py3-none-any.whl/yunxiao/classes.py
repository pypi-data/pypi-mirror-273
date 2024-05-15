import time
from datetime import datetime

from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Union, Literal
from decimal import Decimal
from yunxiao import YunXiao, Page


class Class(BaseModel):
    class Teacher(BaseModel):
        id: Optional[int]
        companyId: Optional[int]
        classId: Optional[int]
        teacherId: Optional[int]
        teacherName: Optional[str]
        teacherPhoto: Optional[str]
        teacherRule: Optional[int]

    class ClassTimeVo(BaseModel):
        id: Optional[int]
        companyId: Optional[int]
        classId: Optional[int]
        weekday: Optional[int]
        weekdayName: Optional[str]
        startTime: Optional[str]
        endTime: Optional[str]
        date: Optional[str]
        deleted: Optional[bool]
        inserted: Optional[bool]

    id: Optional[int]
    className: Optional[str]
    companyId: Optional[int]
    companyName: Optional[str]
    campusId: Optional[int]
    campusName: Optional[str]
    classType: Optional[int]
    fullClassNum: Optional[int]
    currentClassNum: Optional[int]
    # studentVoList: Optional[List[dict]]
    coverMap: Optional[dict]
    detailContent: Optional[str]
    planOpenClassTime: Optional[datetime]
    attendClassTeachers: Optional[List[Teacher]]
    classTeachers: Optional[List[Teacher]]
    classAssistants: Optional[List[Teacher]]
    classRoomId: Optional[int]
    classRoomName: Optional[str]
    classTime: Optional[datetime]
    createTime: Optional[datetime]
    updateTime: Optional[datetime]
    shelfStatus: Optional[str]
    classRoom: Optional[dict]
    chargeSetting: Optional[bool]
    classStatus: Optional[int]
    remark: Optional[str]
    classPriceItems: Optional[List[dict]]
    auditionStudents: Optional[List[dict]]
    unAuditionStudents: Optional[List[dict]]
    classTimeVoList: Optional[List[ClassTimeVo]]
    inserted: Optional[bool]
    stopCourseDate: Optional[datetime]
    # courseArrangeVoList: Optional[List[dict]]
    totalArrange: Optional[int]
    alreadyArrange: Optional[int]
    surplusArrange: Optional[int]
    auditionStudentNum: Optional[int]
    unAuditionStudentNum: Optional[int]
    currentTimeMillis: Optional[datetime]
    totalCourseAmount: Optional[Decimal]
    curriculumId: Optional[int]
    curriculumName: Optional[str]
    curriculumDeleted: Optional[bool]
    priceItem: Optional[dict]
    haveOrder: Optional[bool]
    chargeType: Optional[int]
    lastArrangeDate: Optional[str]
    priceItemVoList: Optional[List[dict]]

    @field_validator('planOpenClassTime', 'createTime', 'updateTime', 'classTime', 'currentTimeMillis', 'stopCourseDate', mode='before')
    def timestamp(cls, v: int):
        return datetime.fromtimestamp(v / 1000) if v else None


class Classes(BaseModel):
    data: List[Class] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()


class ClassesQueryPayload(BaseModel):
    """
    Attributes:
        campusIds: List[int] = []  # 校区
        classIds: List[int] = []  # 班级id
        curriculumIds: List[int] = []  # 课程id
        assistantIds: List[int] = []  # 助教id
        classStatusList: List[int] = []  # 班级状态：0-未结班 1-已结班
        nowTeacherIds: List[int] = []  # 上课老师
    """
    _t_: int = int(time.time() * 1000)
    queryClassTime: int = 1
    campusIds: List[int] = []
    classIds: List[int] = []
    curriculumIds: List[int] = []
    assistantIds: List[int] = []
    page: Page = Page()
    classStatusList: List[int] = []
    nowTeacherIds: List[int] = []


def query_records(auth: YunXiao, payload: ClassesQueryPayload) -> Classes:
    endpoint = f"https://{auth.host}/api/cs-pc-edu/classInfo/page"
    result_type = Classes
    return auth.pages_looper(endpoint, payload, result_type)


def query_classmates(auth: YunXiao, classids: List[int], inout: Literal[1, 2] = 1) -> List[dict]:
    classlist = []
    for classid in classids:
        datas = auth.request(
            method="post",
            url=f"https://{auth.host}/api/cs-pc-edu/classStudent/queryClassStudentList",
            json={"_t_": time.time() * 1000, "classId": classid,
                  "page": {"pageNum": 1, "pageSize": 999, "count": True}, "inOut": inout}

        )["data"]
        classlist.append({"id": classid, "studentVoList": datas})
    return classlist
