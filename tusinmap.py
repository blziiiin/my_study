import folium as fl
from folium.plugins import HeatMap
import pandas as pd
from haversine import haversine
import imgkit


def l2m(latlng1, latlng2):
    # 좌표값 입력 시 거리로 반환
    # Input
    #   latlng1(tuple<float, float>, 첫 번째 지점의 위도와 경도)
    #   latlng2(tuple<float, float>, 두 번째 지점의 위도와 경도)
    # Return: float(두 좌표의 거리(m))

    return haversine(latlng1, latlng2, unit='m')


def search_by_xy(filepath, latlng, range, lat_col='lat', lng_col='lng'):
    # 데이터 프레임 내에서 주어진 좌표와 반경 내의 매물만 필터링하여 반환
    # Input
    #   filepath: str, 데이터프레임 파일 주소
    #   latlng: tuple<float, float>, 위도와 경도
    #   range: int, 반경 범위(m)
    #   lat_col: str, 데이터프레임에서 위도 컬럼 이름
    #   lng_col: str, 데이터프레임에서 경도 컬럼 이름
    # Return: pandas.dataFrame, 입력 좌표 기준으로 반경 내의 매물 데이터

    df = pd.read_csv(filepath, na_values = "")
    df['distance'] = df.apply(lambda x: haversine(latlng, (x['lat'], x['lng']), unit='m'), axis=1)
    return df.query('distance <= @range')


def add_building(t_map, lat, lng, mark_color='blue', icon_color='white', icon='briefcase'):
    # 입력한 좌표에 마커 표시
    # Input
    #   t_map: folium.Map, 마커를 표시할 지도
    #   lat: float, 마커의 위도
    #   lng: float, 마커의 경도
    #   mark_color: str, 마커 색상 
    #   icon_color: str, 마커 내 아이콘 색상
    #   icon: str, 마커 내 아이콘 모양(fontawesome에서 제공하는 아이콘으로 인코딩)
    # Return: None

    fl.Marker(location = (lat, lng), icon=fl.Icon(color=mark_color, icon_color=icon_color, icon=icon, prefix='fa')).add_to(t_map)


def df_to_map(df, centerxy, range, lat_col='lat', lng_col='lng'):
    # 입력받은 데이터프레임의 매물 지도에 마킹. 입력한 좌표와 반경을 기준으로 확대해서 출력한다
    # Input
    #   df: pandas.dataFrame, 사용할 데이터프레임 파일
    #   latlng: tuple<float, float>, 중심이 되는 지점의 위도와 경도
    #   range: int, 반경 범위(m)
    #   lat_col: str, 데이터프레임에서 위도 컬럼 이름
    #   lng_col: str, 데이터프레임에서 경도 컬럼 이름
    # Return: folium.Map, 매물이 표시된 지도 이미지

    # 입력한 반경에 따라 적절한 확대값 찾기
    if range <= 85:
        zoom_size = 19
    elif range <= 170:
        zoom_size = 18
    elif range <= 340:
        zoom_size = 17
    else:
        zoom_size = 16
    t_map = fl.Map(location=(centerxy[0], centerxy[1]), zoom_start=zoom_size, max_zoom = 19, 
                        zoom_control=False, scrollWheelZoom=False, dragging=False)
    df = df.transpose()
    for i in df:
        add_building(t_map, df[i][lat_col], df[i][lng_col])
    return t_map


def save_map(t_map, filename='output'):
    # folium.Map 객체를 html 파일로 저장
    # Input
    #   t_map: folium.Map, 저장할 지도 객체
    #   filename: str, 저장 파일 이름
    # Return: None

    t_map.save(filename+'.html')


def add_heatmap(df, t_map, lat_col='lat', lng_col='lng', target_col = ''):
    # 데이터 프레임에서 원하는 컬럼의 값을 히트맵으로 시각화 
    # Input
    #   df: pandas.dataFrame, 사용할 데이터프레임 파일
    #   t_map: folium.Map, 시각화에 쓰일 지도 객체
    #   lat_col: str, 데이터프레임에서 위도 컬럼 이름
    #   lng_col: str, 데이터프레임에서 경도 컬럼 이름
    #   target_col: str, 히트맵 값에서 기준이 될 컬럼 이름. 디폴트는 갯수
    # Return: folium.Map, 히트맵이 표시된 지도 이미지
    if target_col:
        t_map.add_child(HeatMap(zip(df[lat_col], df[lng_col], df[target_col]), min_opacity=0.1, radius=20, blur=10, max_zoom=10, color='red'))
    else:
        t_map.add_child(HeatMap(zip(df[lat_col], df[lng_col]), min_opacity=0.1, radius=50, blur=50, max_zoom=10, color='red'))
    return t_map


def save_map(filepath, latlng, range, lat_col='lat', lng_col='lng', filename='output', show=False):
    # 데이터 필터링, 지도에 표지, 파일로 저장 과정을 통합
    # Input
    #   filepath: str, 데이터프레임 파일 주소
    #   latlng: tuple<float, float>, 중심이 되는 지점의 위도와 경도
    #   range: int, 반경 범위(m)
    #   lat_col: str, 데이터프레임에서 위도 컬럼 이름
    #   lng_col: str, 데이터프레임에서 경도 컬럼 이름
    #   filename: str, 저장 파일 이름
    #   show: bool, 결과 화면을 현재 창에도 띄우고 싶다면 True로 변경할 것
    # Return: show가 True인 경우 folium.Map, 조건을 만족한 데이터가 표지된 지도
    #         show가 False인 경우 None
    df = search_by_xy(filepath, latlng, range, lat_col=lat_col, lng_col=lng_col)
    t_map = df_to_map(df, latlng, range, lat_col=lat_col, lng_col=lng_col)
    t_map.save(filename+'.html')
    if show:
        return t_map