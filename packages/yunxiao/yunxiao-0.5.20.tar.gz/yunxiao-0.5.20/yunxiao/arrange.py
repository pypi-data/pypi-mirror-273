import time

from pydantic import BaseModel, field_validator, computed_field
from typing import List, Optional
from datetime import datetime
from yunxiao import YunXiao, Page
from decimal import Decimal


class ArrangeRecord(BaseModel):
    class Teacher(BaseModel):
        id: Optional[int]
        companyId: Optional[int]
        courseArrangeId: Optional[int]
        teacherId: Optional[int]
        teacherName: Optional[str]
        teacherRule: Optional[int]

    class Student(BaseModel):
        studentId: Optional[int]
        studentName: Optional[str]

    id: Optional[int]
    num: Optional[int]
    companyId: Optional[int]
    classId: Optional[int]
    classStatus: Optional[int]
    campusId: Optional[int]
    className: Optional[str]
    courseArrangePlanId: Optional[int]
    classRoomId: Optional[int]
    classRoomName: Optional[str]
    startTime: Optional[datetime]
    endTime: Optional[datetime]
    weekDay: Optional[int]
    courseStatus: Optional[int]
    timeOut: Optional[int]
    courseType: Optional[int]
    operationTime: Optional[datetime]
    operationTeacherId: Optional[int]
    reason: Optional[str]
    courseAmount: Optional[Decimal]
    courseArrangeTeacherVoList: Optional[List[Teacher]]
    signNum: Optional[int]
    signTotalNum: Optional[int]
    allSign: Optional[int]
    curriculumId: Optional[int]
    curriculumName: Optional[str]
    coursePlanType: Optional[int]
    teacherSetting: Optional[int]
    enableReserve: Optional[int]
    firstSignTime: Optional[datetime]
    lastSignTime: Optional[datetime]
    courseContent: Optional[str]
    remark: Optional[str]
    campusName: Optional[str]
    identity: Optional[int]
    studentId: Optional[int]
    studentName: Optional[str]
    studentIds: Optional[List[int]]
    students: Optional[List[Student]]
    teacherIds: Optional[List[int]]
    courseSignVoList: Optional[List[dict]]
    commentStudentCount: Optional[int]
    totalStudentCount: Optional[int]
    totalCommentStudentCount: Optional[int]
    haveCourseReserve: Optional[bool]
    courseReserve: Optional[dict]
    haveLeave: Optional[bool]
    chargeTypes: Optional[List[int]]
    fullClassNum: Optional[int]

    @field_validator('startTime', 'endTime', 'operationTime', 'firstSignTime', 'lastSignTime', mode='before')
    def timestamp(cls, v: int):
        return datetime.fromtimestamp(v / 1000) if v else None

    @staticmethod
    def filter_teachers_by_rule(teachers, rule):
        filtered_teachers = [teacher for teacher in teachers if teacher.teacherRule == rule]
        return filtered_teachers

    @computed_field
    def teacherVoList(self) -> List[Teacher]:
        return self.filter_teachers_by_rule(self.courseArrangeTeacherVoList, 0)

    @computed_field
    def assistentVoList(self) -> List[Teacher]:
        return self.filter_teachers_by_rule(self.courseArrangeTeacherVoList, 1)


class ArrangeRecords(BaseModel):
    data: Optional[List[ArrangeRecord]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()


class ArrangeRecordsQueryPayload(BaseModel):
    """
    Attributes:
        campusIds: List[int] = []  # 校区
        startDate: str = ""  # 开始时间
        endDate: str = ""  # 截至时间
        curriculumIds: List[int] = []  # 课程id
        teacherIds: List[int] = []  # 老师id
        assistantTeacherIds: List[int] = []  # 助教id
        classRoomIds: List[int] = []  # 教室id
        studentIds: List[int] = []  # 学生id
        reserve: int = 0  # 只看约课：0-否 1-是
        displayCompletedClass: bool = True  # 展示已结班班级
        courseStatusList: List[int] = []  # 排课状态：0-未点名 1-已点名 2-已取消
        sortType: int = 2  # 按时间排序：1-正向 2-反向
    """
    _t_: int = int(time.time() * 1000)
    page: Page = Page()
    campusIds: List[int] = []  # 校区
    startDate: str = ""  # 开始时间
    endDate: str = ""  # 截至时间
    curriculumIds: List[int] = []  # 课程id
    teacherIds: List[int] = []  # 老师id
    assistantTeacherIds: List[int] = []  # 助教id
    classRoomIds: List[int] = []  # 教室id
    studentIds: List[int] = []  # 学生id
    reserve: int = 0  # 只看约课：0-否 1-是
    displayCompletedClass: bool = True  # 展示已结班班级
    courseStatusList: List[int] = []  # 排课状态：0-未点名 1-已点名 2-已取消
    sortType: int = 2  # 按时间排序：1-正向 2-反向


def query_records(auth: YunXiao, payload: ArrangeRecordsQueryPayload) -> ArrangeRecords:
    endpoint = f"https://{auth.host}/api/cs-pc-edu/arrange/page"
    result_type = ArrangeRecords
    return auth.pages_looper(endpoint, payload, result_type)
