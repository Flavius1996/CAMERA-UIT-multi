# CAMERA UIT multi
Script thực hiện capture các frames từ các camera của UIT

Ngôn ngữ: Python 2.7

## Thư viện cần thiết

Có thể sử dụng pip để cài đặt các lib cần thiết sau cho python:
```Shell
opencv-python (Capture video): https://pypi.python.org/pypi/opencv-python
schedule (Hẹn lịch chạy): https://pypi.python.org/pypi/schedule
```

## Hướng dẫn sử dụng script

1. Clone github này
```Shell
git clone https://github.com/Flavius1996/CAMERA-UIT-multi.git
```

2. Truy cập VPN tới một máy server UIT Cloud.

3. Cách 1: Chạy bằng **file python**. Run CameraUIT_v2.py trên máy server đó:
    ```Shell
    cd CAMERA-UIT-multi
    python CameraUIT_v2.py --cfg <config_path> --camera <camera_info_path>
    ```
   Với cách này, logs của chương trình sẽ được lưu thành các file txt thống kê cho từng ngày và cho từng camera trong thư mục ./logs (có thể chọn lại vị trí lưu logs ở config).
   
   *Trong đó:*
   
   *<config_path>: đường dẫn đến config file .yml*
   
   *<camera_info_path>: đường dẫn đến file .xml chứa thông tin các camera cần capture.*
   
   Cách 2: Chạy bằng **linux script**. Run CameraUIT_log.sh:
    ```Shell
    cd CAMERA-UIT-multi
    ./CameraUIT_log.sh <config_path> <camera_info_path>
    ```
   Với cách 2, lưu các file txt thống kê cho từng ngày (giống cách 1) + logs toàn bộ những gì print ra màn hình của python thành 1 file ./logs/CAMERAUIT_full_logs_date__time.txt
  
## Các option trong file config

Các file config cho script là các file yaml (có đuôi .yml). Có thể tham khảo config mẫu trong [./cfgs/cfg_test.yml](https://github.com/Flavius1996/CAMERA-UIT-multi/blob/master/cfgs/cfg_test.yml)

Trong đó gồm các option sau:

**STORE_PATH**: đường dẫn đến nơi sẽ lưu trữ các frames được captured.

**LOGS_PATH**: đường dẫn đến nơi sẽ lưu trữ logs.

**SAMPLING_RATE**: số frames sẽ được captured trong 1 giây.

**IMAGE_QUALITY**: Chất lượng ảnh JPG được nén (default=100%), số này càng thấp ảnh càng tốn ít dung lượng tuy nhiên chất lượng ảnh sẽ kém.

**IMAGE_FILENAME_STRINGFORMAT**: định dạng đặt tên file cho từng ảnh frame lưu trên ổ cứng. Dựa theo cấu trúc của một [python stringformat](https://pyformat.info/).

*Ví dụ:* Trong file config:
```Shell
    IMAGE_FILENAME_STRINGFORMAT: '"{}_{}_{}__{}".format(camera_name, date, time, count)'
```

Thì các frame sẽ được lưu theo định dạng trên với camera_name, date, time, count lần lượt được điền vào vị trí 2 dấu {}, ví dụ ảnh có thể được lưu dưới tên file sau: test01_26022018_23-47-57__280.jpg

Các trường có thể được dùng ở đây là: camera_name, camera_ip, date, time, count (thứ tự của frames trong phiên làm việc)

WARNING: Không dùng kí tự đặc biệt để lưu tên file. Mặc định file lưu với đuôi .jpg nên không cần thêm đuôi file ở stringformat này.

**DATE_FORMAT**: Định dạng ngày/tháng/năm cho string trường date khi lưu tên file. Default: '%d%m%Y'

**TIME_FORMAT**:  Định dạng giờ/phút/giây cho string trường time khi lưu tên file. Default: '%H-%M-%S'

### TÙY CHỌN CÁCH CHẠY CAPTURE:
#### CÁCH 1: Lập lịch chạy từ ngày X -> Y và trong khoảng thời gian A -> B
**START_TIME**: Thời gian bắt đầu chạy trong ngày (theo 24H format: HH:MM). Ví dụ: '07:00'

**END_TIME**: Thời gian kết thúc capture trong ngày (theo 24H format: HH:MM). Ví dụ: '18:00'

**START_DATE**: Ngày sẽ bắt đầu capture (ghi theo định dạng dd/MM/YYYY). Ví dụ: '26/02/2018'

**END_DATE**: Ngày sẽ kết thúc capture (ghi theo định dạng dd/MM/YYYY). Ví dụ: '01/03/2018'

#### CÁCH 2: Bắt đầu capture ngay lập tức và kết thúc sau khoảng thời gian bao nhiêu phút.
**CAPTURING_TIME**: Khoảng thời gian capturing tính theo ***phút***.

Để chọn chạy theo cách 1, thì set CAPTURING_TIME bằng 0.

## Cấu trúc file xml lưu thông tin camera
Thao khảo tại [./camera_info/info_test.xml](https://github.com/Flavius1996/CAMERA-UIT-multi/blob/master/camera_info/info_test.xml)

Ví dụ: Capture cho 2 camera:
```shell
<CAMERA_INFO>
    <camera name="test01">
        <link>rtsp://test:12345@192.168.75.27:554</link>
    </camera>
    <camera name="test02">
        <link>rtsp://test:12345@192.168.75.27:554</link>
    </camera>
</CAMERA_INFO>
```

Yêu cầu: mỗi camera phải có tên khác nhau.

