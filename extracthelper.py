"""tusinEX.py

Module for data extraction or visulization

Jaewon Jeong

"""

import folium as fl
from folium.map import Layer
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
import pandas as pd
from haversine import haversine
from datetime import datetime
from typing import Union


class ExtractHelper:
    def __init__(self, file: Union[str, pd.DataFrame], 
                lat_col='lat', lng_col='lng', tar_col='', 
                center=(.0, .0), range=500,
                guide_list = [],
                auto_show = True, auto_save = False,
                save_path = '', save_name = datetime.now().strftime('%Y%m%d_%H%M%S')[2:]
                ):
        if isinstance(file, str):
            df = pd.read_csv(file, na_values = "")
            self.dataFrame = df
        else:
            self.dataFrame = file

        self.latitude_column_label = lat_col
        self.longitude_column_label = lng_col
        self.target_column_label = tar_col

        if center == (.0, .0):
            self.center = (self.dataFrame[self.latitude_column_label].mean(), self.dataFrame[self.longitude_column_label].mean())
        else:
            self.center = center
        self.range = range

        self.guide_list = guide_list

        self.auto_show = auto_show
        self.auto_save = auto_save

        self.save_path = save_path
        self.save_name = save_name

        self.zoom_size = 16

        self.dist = None
        self.filteredData = self.dataFrame
        self.map = fl.Map(location=(self.center[0], self.center[1]), zoom_start=self.zoom_size, max_zoom = 19, tiles = None,
                                    scrollWheelZoom=False, dragging=False)
        fl.TileLayer(tiles='openstreetmap', name='basemap').add_to(self.map)
        self.layers = dict()


    #########################################################################

    def get_df(self) -> pd.DataFrame:
        return self.dataFrame


    def get_filtered_df(self) -> pd.DataFrame:
        return self.filteredData


    def set_center(self, lat: float, lng: float):
        if lat != self.center[0] or lng != self.center[1]:
            self.dist = None
        self.center = (lat, lng)


    def set_center(self, center: tuple[float]): # overload set_center
        if center != self.center:
            self.dist = None
        self.center = center


    def set_axis_label(self, lat_col='', lng_col='', tar_col=''):
        if lat_col:
            self.latitude_column_label = lat_col

        if lng_col:
            self.longitude_column_label = lng_col

        if tar_col:
            self.target_column_label = tar_col

    
    def set_range(self, range: int):
        self.range = range


    def set_guide_list(self, guideList: list[int]):
        self.guide_list = guideList
        self.guide_list.sort()
 
        
    def add_guide_list(self, ranges: Union[int, list[int]]):
        # 반경 리스트 추가
        if isinstance(ranges, int):
            if ranges in self.guide_list:
                # 중복 반경 경고 메시지
                pass
            self.guide_list.append(ranges)
            self.guide_list.sort()
        else:
            for r in ranges:
                if r in self.guide_list:
                    # 중복 반경 경고 메시지
                    pass
                else:
                    self.guide_list.append(r)
        self.guide_list.sort()


    def able_autoshow(self):
        self.auto_show = True


    def disable_autoshow(self):
        self.auto_show = False


    def able_autosave(self):
        self.auto_save = True


    def disable_autosave(self):
        self.auto_save = False


    def set_save_path(self, path: str):
        self.save_path = path


    def set_save_name(self, name: str):
        self.save_name = name


    def set_filtered_df(self, fd):
        self.filteredData = fd

    #########################################################################

    def filter(self, ret=False) -> pd.DataFrame:
        # 데이터프레임 필터링
        lat = self.latitude_column_label
        lng = self.longitude_column_label

        if not isinstance(self.dist, pd.Series):
            self.dist = pd.Series(self.dataFrame.apply(lambda x: haversine(self.center, (x[lat], x[lng]), unit='m'), axis=1))
        self.filteredData = self.dataFrame[self.dist <= self.range]

        if self.range <= 85:
            self.zoom_size = 19
        elif self.range <= 170:
            self.zoom_size = 18
        elif self.range <= 340:
            self.zoom_size = 17

        self.map = fl.Map(location=(self.center[0], self.center[1]), zoom_start=self.zoom_size, max_zoom = 19, tiles = None,
                            scrollWheelZoom=False, dragging=False)
        fl.TileLayer(tiles='openstreetmap', name='basemap').add_to(self.map)
        
        if ret:
            return self.filteredData

    
    #########################################################################

    def draw_marker(self, layername='markers', mark_color='blue', icon_color='white', icon='briefcase'):
        # 지도에 매물 마커 추가 후 출력
        lat = self.latitude_column_label
        lng = self.longitude_column_label

        if layername in self.layers:
            # 레이어가 겹쳐질 수 있음을 경고
            pass
        else:
            self.layers[layername] = fl.FeatureGroup(name=layername).add_to(self.map)

        df = self.filteredData.transpose()
        for i in df:
            fl.Marker(location=(df[i][lat], df[i][lng]), 
                                    icon=fl.Icon(color=mark_color, icon_color=icon_color, icon=icon, prefix='fa')).add_to(self.layers[layername])
        
        if self.auto_show:
            return self.map


    def draw_heatmap(self, layername='heatmap', tar_label=''):
        # 지도에 히트맵 추가 후 출력
        lat = self.latitude_column_label
        lng = self.longitude_column_label
        if tar_label:
            self.target_column_label = tar_label
        tar = self.target_column_label

        if layername in self.layers:
            # 레이어가 겹쳐질 수 있음을 경고
            pass
        else:
            self.layers[layername] = fl.FeatureGroup(name=layername).add_to(self.map)

        if tar:
            HeatMap(zip(self.filteredData[lat], self.filteredData[lng], self.filteredData[tar]),
                                min_opacity=0.1, radius=20, blur=10, max_zoom=10, color='red').add_to(self.layers[layername])
        else:
            HeatMap(zip(self.filteredData[lat], self.filteredData[lng]),
                                min_opacity=0.1, radius=50, blur=50, max_zoom=10, color='red').add_to(self.layers[layername])
        
        if self.auto_show:
            return self.map


    def draw_guide_line(self, layername='guide_ranges', color='red', width=1):
        # 실선 가이드 반경 추가
        if layername in self.layers:
            # 레이어가 겹쳐질 수 있음을 경고
            pass
        else:
            self.layers[layername] = fl.FeatureGroup(name=layername).add_to(self.map)

        for l in self.guide_list:
            fl.Circle(location=self.center, radius=l, color=color, weight=width).add_to(self.layers[layername])
        
        if self.auto_show:
            return self.map


    def draw_guide_color(self, layername='range_area', color='yellow', opacity=0.2) -> fl.Map:
        # 영역 가이드 반경 추가
        if layername in self.layers:
            # 레이어가 겹쳐질 수 있음을 경고
            pass
        else:
            self.layers[layername] = fl.FeatureGroup(name=layername).add_to(self.map)

        fl.Circle(location=self.center, radius=self.range, stroke=False,
                    fill=True, fill_color=color, fill_opacity=opacity).add_to(self.layers[layername])
        
        if self.auto_show:
            return self.map


    def initialize(self):
        # 맵과 필터링 초기화
        self.filteredData = self.dataFrame
        self.map = fl.Map(location=(self.center[0], self.center[1]), zoom_start=self.zoom_size, max_zoom = 19, tiles = None,
                            scrollWheelZoom=False, dragging=False)
        fl.TileLayer(tiles='openstreetmap', name='basemap').add_to(self.map)
        self.layers = dict()


    def show(self, controller=False):
        # 현재 지도 화면에 출력, 저장 안 함
        if controller:
            fl.LayerControl().add_to(self.map)

        return self.map


    def visualize_all(self):
        # 데이터 전체 시각화 및 지도 출력
        self.initialize()
        self.filter()
        self.draw_marker()
        self.draw_heatmap()
        self.draw_guide_line()
        self.draw_guide_color()

        return self.show(controller=True)


    #########################################################################

    def save(self, name='', show=False):
        # 지도 저장
        if name:
            self.map.save(self.save_path+name+'.html')
        else:
            self.map.save(self.save_path+self.save_name+'.html')

        if show:
            return self.map()