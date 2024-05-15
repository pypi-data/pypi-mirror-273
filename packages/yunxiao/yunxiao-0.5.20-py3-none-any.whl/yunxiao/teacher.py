import time

from pydantic import BaseModel
from typing import List, Optional
from yunxiao import YunXiao, Page


class Teacher(BaseModel):
    class orgStructureList(BaseModel):
        id: int
        orgStructureId: int
        orgStructureName: str
        leaderStatus: int

    class teacherCampusDtos(BaseModel):
        id: int
        companyId: int
        teacherId: int
        campusId: int
        campusName: str

    class teacherRoleDtos(BaseModel):
        companyId: int
        productCode: int
        terminalType: int
        teacherId: int
        roleId: int
        roleParentId: int
        roleName: str
        roleIds: Optional[list]

    class Photo(BaseModel):
        ext: Optional[str] = None
        fileKey: Optional[str] = None
        mimeType: Optional[str] = None
        type: Optional[str] = None
        url: Optional[str] = None
        duration: Optional[int] = None
        bucket: Optional[str] = None
        fileSize: Optional[int] = None
        width: Optional[int] = None
        height: Optional[int] = None
        name: Optional[str] = None
        etag: Optional[str] = None
        fileId: Optional[str] = None

    id: int
    name: str
    phone: str
    sex: int
    photo: Photo
    superAdmin: bool
    admin: Optional[bool]
    activation: bool
    companyId: int
    companyName: Optional[str]
    roleIds: Optional[List[int]]
    campusIds: Optional[List[int]]
    roleList: list
    campusList: Optional[list]
    teacherCampusDtos: Optional[List[teacherCampusDtos]]
    teacherRoleDtos: Optional[List[teacherRoleDtos]]
    orgStructureList: Optional[List[orgStructureList]]
    dataRole: int
    status: int
    leaveOffInfo: Optional[str]
    activated: bool


class TeacherLite(BaseModel):
    """
    Attributes:
        name: str
        sex: int = 1
        phone: str
        campusIds: Optional[List[int]] = [26118412, 32654752, 33447580, 34961723]
        roleIds: Optional[List[int]] = [26168011]
        orgStructureList: Optional[List[dict]] = [{
            "orgStructureName": "兼职",
            "leaderStatus": 0,
            "orgStructureId": 49186449
        }]
        dataRole: int = 2
        id: int = None
    """
    _t_: int = int(time.time() * 1000)
    name: str
    sex: int = 1
    phone: str
    campusIds: Optional[List[int]] = [26118412, 32654752, 33447580, 34961723]
    roleIds: Optional[List[int]] = [26168011]
    orgStructureList: Optional[List[dict]] = [{
        "orgStructureName": "兼职",
        "leaderStatus": 0,
        "orgStructureId": 49186449
    }]
    dataRole: int = 2
    id: int = None


class Teschers(BaseModel):
    data: List[Teacher] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()


class TeschersQueryPayload(BaseModel):
    """
    Attributes:
        campusIds: List[int] = []
        queryKey: str = ""
        roleIds: List[int] = []
        statusIds: List[int] = []
        _t_: int = int(time.time() * 1000)
        page: Page = Page(pageNum=1, pageSize=100)
    """
    campusIds: List[int] = []
    queryKey: str = ""
    roleIds: List[int] = []
    statusIds: List[int] = []
    _t_: int = int(time.time() * 1000)
    page: Page = Page()


def query_records(client: YunXiao, payload: TeschersQueryPayload) -> Teschers:
    endpoint = f"https://{client.host}/api/cs-pc-crm/teacher/pageList"
    result_type = Teschers
    return client.pages_looper(endpoint, payload, result_type)


def op_edit(client: YunXiao, teacher: TeacherLite):
    res = client.request(
        method="POST",
        url=f"https://{client.host}/api/cs-pc-crm/teacher/editTeacher",
        json=teacher.model_dump()
    )["data"]
    return res


def op_create(client: YunXiao, teacher: TeacherLite):
    data = teacher.model_dump()
    data.pop("id")
    res = client.request(
        method="POST",
        url=f"https://{client.host}/api/cs-pc-crm/teacher/create",
        json=data
    )["data"]
    return res


def op_leave(client: YunXiao, teache_id: int):
    res = client.request(
        method="POST",
        url=f"https://{client.host}/api/cs-pc-crm/teacher/leaveOffice",
        json={
            "_t_": int(time.time() * 1000),
            "teacherId": teache_id
        }
    )["data"]
    return res


def op_back(client: YunXiao, teache_id: int):
    res = client.request(
        method="POST",
        url=f"https://{client.host}/api/cs-pc-crm/teacher/backOffice",
        json={
            "_t_": int(time.time() * 1000),
            "teacherId": teache_id
        }
    )["data"]
    return res
