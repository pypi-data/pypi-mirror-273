import time

from pydantic import BaseModel, computed_field
from typing import List, Optional
from decimal import Decimal
from yunxiao import YunXiao, Page


class Curriculum(BaseModel):
    class PriceItem(BaseModel):
        class PriceItemDetail(BaseModel):
            id: Optional[int]
            companyId: Optional[int]
            price: Optional[float]
            priceName: Optional[str]
            priceNum: Optional[int]
            audition: Optional[bool]
            priceTypeName: Optional[str]
            chargeType: Optional[int]
            priceUnitName: Optional[str]
            originalPrice: Optional[bool]
            shelfStatus: Optional[str]
            commodityPriceType: Optional[str]
            dayType: Optional[int]

        id: Optional[int]
        companyId: Optional[int]
        curriculumId: Optional[int]
        priceItemName: Optional[str]
        chargeType: Optional[int]
        chargeTypeName: Optional[str]
        priceItemDetailList: Optional[List[PriceItemDetail]]

    id: Optional[int]
    companyId: Optional[int]
    curriculumName: Optional[str]
    haltSale: Optional[int]
    dimensionNameText: Optional[str]
    commodityCurriculumCampusList: Optional[List]
    priceItemVoList: Optional[List[PriceItem]]
    courseRelation: Optional[str]
    cardInfoId: Optional[str]
    suspendDate: Optional[str]

    @computed_field
    def season(self) -> str | None:
        for dimension in self.dimensionNameText.split('·'):
            if dimension in ['春季', '暑假', '秋季', '寒假']:
                return dimension
        return None

    @computed_field
    def type(self) -> str | None:
        for dimension in self.dimensionNameText.split('·'):
            if dimension in ['班课', '一对一', '自习', '其他']:
                return dimension
        return None

    @computed_field
    def subject(self) -> str | None:
        for dimension in self.dimensionNameText.split('·'):
            if dimension in ['语文', '数学', '英语', '物理', '化学', '生物', '物理', '地理', '历史', '道法']:
                return dimension
        return None

    @computed_field
    def size(self) -> str | None:
        for dimension in self.dimensionNameText.split('·'):
            if dimension in ['小班', '常规', '大班']:
                return dimension
        return None

    @computed_field
    def grade(self) -> str | None:
        for dimension in self.dimensionNameText.split('·'):
            if dimension[0] in ['小', '初', '高'] and dimension[1] != '班':
                return dimension
        return None


class Curriculums(BaseModel):
    data: List[Curriculum] = []
    currentTimeMillis: int = 0
    code: int = 200
    msg: str = ""
    page: Page = Page()


class CurriculumsQueryPayload(BaseModel):
    """
    Attributes:
        curriculumName: str = ""
        dimensionDetailIdList: List[int] = []
        _t_: int = int(time.time() * 1000)
        page: Page = Page(pageNum=1, pageSize=100)
    """
    curriculumName: str = ""
    dimensionDetailIdList: List[int] = []
    _t_: int = int(time.time() * 1000)
    page: Page = Page()


def query_records(auth: YunXiao, payload: CurriculumsQueryPayload) -> Curriculums:
    endpoint = f"https://{auth.host}/api/cs-pc-edu/curriculum/page"
    result_type = Curriculums
    return auth.pages_looper(endpoint, payload, result_type)
