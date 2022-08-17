import folium as fl
from folium.plugins import HeatMap
import pandas as pd
from haversine import haversine
import imgkit


# def repeat(message: str, times: int = 2) -> list:
#     return [message] * times


# 데이터프레임을 저장하고 관리하는 클래스
class Data:
# 객체 변수
# 데이터프레임: pd.dataFrame
# 기준 좌표: tuple(float)
# 위도 라벨: str
# 경도 라벨: str
# 반경: int
# 히트맵용 값 라벨: str


    def __init__(self, *args):
        if isinstance(args[0], str):
            df = pd.read_csv(args[0], na_values = "")
            self.dataFrame = df
        else:
            self.dataFrame = args[0]
        self.center = (.0, .0)
        self.latitude_column_label = 'lat'
        self.longitude_column_label = 'lng'
        self.range = 500
        self.target_column_label = ''


# 메서드
# 객체 변수를 반환하는 함수들
# 객체 변수를 변경하는 함수들 -> None
# 안내선 생성용 반경 리스트 추가(list(int)) -> None
# 필터링한 데이터프레임 반환(혹은 변경) -> pd.dataFrame


    def get_center(self) -> tuple(float):
        return self.latitude_column_label


    def get_lng_col(self) -> str:
        return self.longitude_column_label


    def set_axis_label(self, lat: str, lng: str) -> None:
        self.latitude_column_label = lat
        self.longitude_column_label = lng

    
    def set_target_label(self, tar: str) -> None:
        self.target_column_label = tar

    
    def filter_data(self, center, lat, lng, range) -> None:
        self.dataFrame['distance'] = self.dataFrame.apply(lambda x: haversine(center, (x[lat], x[lng]), unit='m'), axis=1)
        self.filteredData = self.dataFrame.query('distance <= @range')



# 지도를 저장하고 관리하는 클래스
class MapT:
    def __init__(self, center: tuple(float), range: int) -> None:
        self.center = center
        self.range = range
        self.guide_range = []


    def get_center(self) -> tuple(float):
        return self.center
    

    def get_range(self) -> int:
        return self.range

    
    def get_guide_range(self) -> list(int):
        return self.guide_range


    def set_center(self, center: tuple(float)) -> None:
        self.center = center


    def set_range(self, range: int) -> None:
        self.range = range


    def append_guide_range(self, range: int) -> None:
        self.guide_range.append(range)
        self.guide_range.sort()

    
    def append_guide_ranges(self, ranges: list(int)) -> None:
        self.guide_range += ranges
        self.guide_range.sort()





# 전체 컨트롤 클래스
class MappingHelper:
    def __init__(self):
        self.dataClass = None
        self.mapClass = None
    

    def put_by_path(self, filepath: str) -> None:
        df = pd.read_csv(filepath, na_values = "")
        self.dataClass = Data(df)

    
    def put_by_df(self, df: pd.DataFrame) -> None:
        self.dataClass = Data(df)
        
    
    def set_column_name(self, lat: str, lng: str, tar: str='') -> None:
        self.dataClass.set_axis_label(lat, lng)
        self.dataClass.set_target_label(tar)


    def change_target(self, tar: str) -> None:
        self.dataClass.set_target_label(tar)


    def map_initialize(self, center: tuple(float), range: int, filter: bool) -> None:
        if filter:
            self.dataClass.filter_data(self.mapClass.center, lat, lng, self.mapClass.get_range())
        self.mapClass = MapT(center, range)

    
    def add_guide_range(self, range: int) -> None:
        self.mapClass.append_guide_range(range)


    def add_guide_ranges(self, ranges: list(int)) -> None:
        self.mapClass.append_guide_ranges(ranges)


    # 데이터 필터링
    def filter_data(self) -> None:
        
        pass