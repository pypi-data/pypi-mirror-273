import time
from datetime import datetime

from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Union
from decimal import Decimal
from yunxiao import YunXiao, Page


class Student(BaseModel):
    class StudentParentRelation(BaseModel):
        relation: str
        phone: str
        active: bool
        often: bool

    class FollowTeacher(BaseModel):
        followTeacherId: int
        followTeacherName: str
        tags: List[str]
        tagList: List[str]
        type: int

    class CustomField(BaseModel):
        id: Optional[int]
        companyId: Optional[int]
        customFieldId: int
        fieldClassify: Optional[str]
        fieldCode: Optional[str]
        fieldName: str
        fieldDataType: int
        sort: int
        businessType: Optional[str]
        businessId: int
        value: str
        valueList: Optional[List[str]]
        displayList: Optional[List[str]]
        display: int
        required: int
        selectItemList: Optional[List[str]]
        type: int

    id: int
    name: str
    studentParentRelation: List[StudentParentRelation]
    sex: int
    sexDesc: str
    companyId: int
    companyName: Optional[str]
    campusId: int
    campusName: str
    birthday: Optional[datetime]
    age: Optional[int]
    ageDesc: Optional[str]
    contactsWechatCode: Optional[str]
    customGradeId: Optional[int]
    customGradeName: Optional[str]
    customComeFromId: Optional[int]
    customComeFromDesc: Optional[str]
    introducerId: Optional[int]
    introducerName: Optional[str]
    active: Optional[bool]
    hasFace: Optional[bool]
    status: Optional[int]
    createTime: datetime
    createTeacherId: Optional[int]
    createTeacherName: Optional[str]
    followTeacherList: Optional[List[FollowTeacher]]
    teachFollowTeacherList: Optional[List[FollowTeacher]]
    sellFollowTeacherList: Optional[List[FollowTeacher]]
    customFieldList: Optional[List[CustomField]]
    customIdCard: Optional[Optional[str]]
    customSchool: Optional[str]

    @field_validator('createTime', 'birthday', mode='before')
    def validate_payTime(cls, v: int):
        return datetime.fromtimestamp(v / 1000) if v else None


class Students(BaseModel):
    data: Optional[List[Student]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()


class StudentsQueryPayload(BaseModel):
    """
    Attributes:
    """

    class CustomFieldValueQueryDto(BaseModel):
        label: str
        businessType: str
        customFieldId: int
        fieldDataType: int
        textValue: str

    _t_: int = int(time.time() * 1000)
    campusIds: List[int] = []
    classIds: List[int] = []
    classStudentStatus: int = 0
    curriculumIds: List[int] = []
    customComeFromIds: List[int] = []
    customSchool: str = ""
    customIdCard: str = ""
    customGradeIds: List[int] = []
    customFieldValueQueryDtoList: Optional[List[CustomFieldValueQueryDto]] = []
    startCreateTime: str = ""
    endCreateTime: str = ""
    followTeacherIdsMap: Dict[int, List[int]] = {}
    introducerIds: List[int] = []
    onlyQueryRegisterCampus: bool = False
    page: Page = Page()
    sexList: List[int] = []
    statusList: List[int] = []
    queryKey: str = ""


class Card(BaseModel):
    cardCourseTradedId: int
    companyId: int
    campusId: int
    campusName: str
    studentId: int
    studentName: str
    parentPhone: str
    curriculumId: int
    curriculumName: str
    cardInfoId: int
    cardInfoName: str
    cardType: int
    chargeType: int
    priceUnitName: str
    feeWarnStatus: int
    buyAmount: Decimal
    freeAmount: Decimal
    totalAmount: Decimal
    consumeAmount: Decimal
    consumeFreeAmount: Decimal
    totalConsumeAmount: Decimal
    refundBuyAmount: Decimal
    refundFreeAmount: Decimal
    totalRefundAmount: Decimal
    transferAmount: Decimal
    transferFreeAmount: Decimal
    totalTransferAmount: Decimal
    totalRefundTransferAmount: Decimal
    expireAmount: Decimal
    expireFreeAmount: Decimal
    totalExpireAmount: Decimal
    remainAmount: Decimal
    remainFreeAmount: Decimal
    totalRemainAmount: Decimal
    totalRemainBuyAmount: Decimal
    totalRemainFreeAmount: Decimal
    totalAvailableRemainAmount: Decimal
    oweAmount: Decimal
    totalMoney: Decimal
    consumeMoney: Decimal
    remainMoney: Decimal
    expireMoney: Decimal
    oweMoney: Decimal


class Cards(BaseModel):
    data: Optional[List[Card]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()


class CardsQueryPayload(BaseModel):
    _t_: Optional[int] = int(time.time() * 1000)
    page: Page = Page()
    campusIds: List[int] = []  # 校区
    studentClassIds: List[int] = []  # 班级
    studentStatusList: List[int] = []  # 学员状态：0-未收费 1-在读 7-停课
    studentIds: List[int] = []  # 学生
    displayHistory: bool = True  # 曾就读学员：True-展示 False-不展示
    cardType: Optional[int] = None  # 上课卡：None-不限 0-课程 1-课时包
    feeWarnStatus: int = 0  # 上课卡状态：0-不限 1-正常 2-不再费用预警
    curriculumIds: List[int] = []  # 课程
    cardInfoIds: List[int] = []  # 课程卡
    remainAmountMin: Optional[str] = ""  # 最小剩余数量
    remainAmountMax: Optional[str] = ""  # 最大剩余数量
    sort: Optional[str] = None
    sortField: Optional[str] = None


class Course(BaseModel):
    class ClassStudent(BaseModel):
        id: Optional[int]
        companyId: Optional[int]
        campusId: Optional[int]
        classId: Optional[int]
        className: Optional[str]
        curriculumId: Optional[int]
        transferClassId: Optional[int]
        studentId: Optional[int]
        studentName: Optional[str]
        studentIds: Optional[List[int]]
        inDate: Optional[int]
        outDate: Optional[int]
        courseTime: Optional[int]
        outReason: Optional[str]
        outMemo: Optional[str]
        outType: Optional[int]
        sameDay: Optional[bool]
        oversold: Optional[bool]
        operatorId: Optional[int]
        isInClass: Optional[int]
        student: Optional[str]

    curriculumId: Optional[int]
    curriculumName: Optional[str]
    priceItemId: Optional[int]
    priceItemName: Optional[str]
    campusId: Optional[int]
    campusName: Optional[str]
    attendanceCount: Optional[int]
    lateCount: Optional[int]
    askForLeaveCount: Optional[int]
    notArrivedCount: Optional[int]
    absentAmount: Optional[int]
    courseConsumeAmount: Optional[int]
    courseAmount: Optional[int]
    classStudentList: Optional[List[ClassStudent]]
    courseStatus: Optional[int]
    chargeType: Optional[int]
    totalRemainAmount: Optional[int]
    cardCourseTradedId: Optional[int]
    studentName: Optional[str]
    status: Optional[int]
    existAutoCharge: Optional[bool]
    cardNameList: Optional[List[str]]
    courseArrangeAmount: Optional[int]
    alreadyAttendedAmount: Optional[int]
    studentId: Optional[int]


class Courses(BaseModel):
    data: Optional[List[Course]] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()

    @field_validator('data', mode='before')
    def validate_data(cls, v: dict):
        class data(BaseModel):
            studentAttendCourseList: List[Course] = []
            noLongerCourseCount: Decimal
        return data(**v).studentAttendCourseList


class StudentCoursesQueryPayload(BaseModel):
    page: Page = Page()
    _t_: int = int(time.time() * 1000)
    studentId: int


def query_records(
        auth: YunXiao,
        payload: Union[StudentsQueryPayload, CardsQueryPayload, StudentCoursesQueryPayload]
) -> Union[Students, Cards, Courses]:
    if isinstance(payload, StudentsQueryPayload):
        result_type = Students
        endpoint = f"https://{auth.host}/api/cs-pc-crm/student/extendList"
    elif isinstance(payload, CardsQueryPayload):
        result_type = Cards
        endpoint = f"https://{auth.host}/api/cs-pc-report/cs-report/reports/studentCourseCard/report"
    else:
        result_type = Courses
        endpoint = f"https://{auth.host}/api/cs-pc-edu/courseStudent/findStudentAttendCourse"
    return auth.pages_looper(endpoint, payload, result_type)


def become_history(auth: YunXiao, studentIds: List[int]):
    return auth.request(
        method="post",
        url=f"https://{auth.host}/api/cs-pc-edu/student/becomeHistory",
        json={"_t_": int(time.time() * 1000), "studentIds": studentIds}
    )


def become_study(auth: YunXiao, studentIds: List[int]):
    return auth.request(
        method="post",
        url=f"https://{auth.host}/api/cs-pc-edu/student/becomeStudy",
        json={"_t_": int(time.time() * 1000), "studentIds": studentIds}
    )