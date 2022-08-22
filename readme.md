# ExtractHelper 변수, 기능 설명

## 객체 변수
|variable name          |data type                  |default value                  |description|
|-                      |-                          |-                              |-|
|dataFrame              |pd.DataFrame               |-                              |데이터프레임|
|center                 |tuple(float, float)        |(37.5642135, 127.0016985)      |필터링할 때 기준이 되는 좌표|
|latitude_column_label  |str                        |'lat'                          |데이터프레임에서 위도를 가리키는 열의 라벨|
|longitude_column_label |str                        |'lng'                          |데이터프레임에서 경도를 가리키는 열의 라벨|
|target_column_label    |str                        |''                             |히트맵 생성시 기준값이 되는 열의 라벨|
|range                  |int                        |500                            |필터링할 때 기준이 되는 반경|
|guide_list             |list(int)                  |[]                             |지도에 시각화할 때 표시하고 싶은 반경|        
|auto_save              |bool                       |False                          |지도를 시각화할 때 html 파일 자동 저장 여부|
|save_path              |str                        |(blank)                        |html 파일을 저장할 디렉토리|       
|save_name              |str                        |yymmdd_hhmmss (current)        |저장할 html 파일의 이름|
|zoom_size              |int                        |16                             |지도의 확대 정도(반경 설정시 자동으로 변경)| 
|dist                   |pd.Series                  |None                           |입력한 중심 좌표와 데이터프레임속 매물의 간격(m)|                       
|filteredData           |pd.DataFrame               |self.dataFrame                 |필터링된 데이터프레임|
|map                    |fl.Map                     |fl.Map base on self.dataFrame  |지도 데이터|
|layers                 |dict(str, fl.map.Layer)    |[]                             |지도에 표시되는 레이어|    
   
--------------------------------------------------------
## 클래스 메서드
### 객체 변수 제어 관련 메서드
> get_df(self)
- 입력: 없음
- 반환: pd.DataFrame
- 초기에 입력한 데이터프레임 반환   
   
> get_filtered_df(self)
- 입력: 없음
- 반환: pd.DataFrame
- 필터링된 데이터프레임 반환

> set_center(self, lat: float, lng: float)
- 입력: lat = 위도 좌표, lng = 경도 좌표
- 반환: 없음
- 중심 좌표를 입력한 값으로 설정


> set_center(self, center: tuple[float])
- overload set_center
- 입력: 튜플 (위도 좌표, 경도 좌표)
- 반환: 없음
- 중심 좌표를 입력한 값으로 설정


> set_center_auto(self)
- 입력: 없음
- 반환: 없음
- 입력한 데이터를 기준으로 중심 좌표를 자동 설정


> set_axis_label(self, lat_col='', lng_col='', tar_col='')
- 입력: lat_col = 위도 열 라벨, lng_col = 경도 열 라벨, tar_col = (히트맵용) 기준 데이터 열 라벨
- 반환: 없음
- 위도, 경도, 기준값 라벨 재설정


> set_range(self, range: int)
- 입력: range = 반경
- 반환: 없음
- 필터링할 기준이 되는 반경 설정


> set_guide_list(self, guideList: list[int])
- 입력: guideList = 가이드 반경 리스트
- 반환: 없음
- 지도에 출력할 가이드 반경 설정


> add_guide_list(self, ranges: Union[list[int], int])
- 입력: ranges = 추가할 가이드 반경 또는 가이드 반경 리스트
- 반환: 없음
- 지도에 출력할 가이드 반경 추가


> able_autoshow(self)
- 입력: 없음
- 반환: 없음
- 지도 시각화 함수 사용 시 지도 자동 출력 활성화


> disable_autoshow(self)
- 입력: 없음
- 반환: 없음
- 지도 시각화 함수 사용 시 지도 자동 출력 비활성화


> able_autosave(self)
- 입력: 없음
- 반환: 없음
- 지도 시각화 함수 사용 시 지도 자동 저장 활성화


> disable_autosave(self)
- 입력: 없음
- 반환: 없음
- 지도 시각화 함수 사용 시 지도 자동 저장 비활성화


> set_save_path(self, path: str)
- 입력: path = 지도를 저장할 디렉토리 주소
- 반환: 없음
- 지도를 저장할 디렉토리 설정


> set_save_name(self, name: str)
- 입력: name = 지도를 저장할 때 사용할 이름
- 반환: 없음
- 지도 이름 설정


> set_filtered_df(self, fd)
- 입력: fd = 지도 시각화에 사용할 필터링된 데이터프레임
- 반환: 없음
- 필터링된 데이터프레임 설정

--------------------------------------------------------
### 데이터 프레임 필터링 관련 메서드
> filter(self, ret=False)
- 입력: ret = 필터링한 데이터의 반환 여부
- 반환: 없음 또는 필터링한 데이터
- 데이터프레임을 설정한 중심 좌표와 반경을 기준으로 필터링한다
- ret값을 True로 하면 필터링된 데이터프레임을 반환한다

--------------------------------------------------------
### 지도 시각화 관련 메서드
> draw_marker(self, layername='markers', mark_color='blue', icon_color='white', icon='briefcase')
- 입력: layername = 마커 표시할 레이어 이름, mark_color = 마커 색상, icon_color = 아이콘 색상, icon = 아이콘 모양(fontawesome 인코딩)
- 반환: (self.auto_show = True인 경우) fl.map
- 지도에 매물 마커 추가
- auto_save 변수가 True인 경우 지도가 출력된다
- 동일한 이름의 레이어가 있는 경우 합쳐진다


> draw_heatmap(self, layername='heatmap', tar_label='')
- 입력: layername = 히트맵 표시할 레이어 이름, tar_label = 히트맵 표시할 때 기준이 되는 값
- 반환: (self.auto_show = True인 경우) fl.map
- 지도에 히트맵 추가, tar_name 입력이 있는 경우 객체변수 target_column_label의 값도 변경한다.
- auto_save 변수가 True인 경우 지도가 출력된다
- 동일한 이름의 레이어가 있는 경우 합쳐진다


> draw_guide_line(self, layername = 'guide_ranges', color='red', width=1)
- 입력: layername = 가이드 반경 선을 표시할 레이어 이름, color = 선 색상, width = 선 두께
- 반환: (self.auto_show = True인 경우) fl.map
- 실선 가이드 반경 추가
- auto_save 변수가 True인 경우 지도가 출력된다
- 동일한 이름의 레이어가 있는 경우 합쳐진다


> draw_guide_color(self, layername = 'range_area', color='yellow', opacity=0.2)
- 입력: layername = 가이드 반경 영역을 표시할 레이어 이름, color = 영역 색상, opacity = 영역 투명도
- 반환: (self.auto_show = True인 경우) fl.map
- 영역 가이드 반경 추가
- auto_save 변수가 True인 경우 지도가 출력된다
- 동일한 이름의 레이어가 있는 경우 합쳐진다


> initialize(self)
- 입력: 없음
- 반환: 없음
- 맵과 필터링 모두 초기화


> show(self, controller=False)
- 입력: controller = 레이어 컨트롤러 출력 여부
- 반환: fl.map
- 현재 지도 화면에 출력
- **controller를 생성한 이후에는 레이어 추가 시 지도 초기화 필요**


> visualize_all(self)
- 입력: 없음
- 반환: fl.map
- 데이터 전체 시각화 및 지도 출력
- **이후 지도 변경시 지도 초기화 필요**

--------------------------------------------------------
### 지도 저장 관련 메서드
> save(self, name='', show=False):
- 입력: name = 저장할 파일 이름, show = 지도 화면 출력 여부
- 반환: 없음 또는 최종 지도
- 지도를 파일로 저장

--------------------------------------------------------
## 사용 예제
### EDA 진행 시
1. 데이터프레임 또는 데이터파일의 주소를 입력
```python
eh = extracthelper.ExtractHelper('example_data.csv')
```
1. 중심 좌표 및 반경을 설정
```python
eh.set_center()
eh.set_range(500)
```
1. 안내선 반경을 추가해야 하는 경우
```python
eh = extracthelper.ExtractHelper('example_data.csv')
```
1. filter()로 데이터를 필터링
```python
eh = extracthelper.ExtractHelper('example_data.csv')
```
1. visualize_all()로 지도를 시각화
```python
eh = extracthelper.ExtractHelper('example_data.csv')
```