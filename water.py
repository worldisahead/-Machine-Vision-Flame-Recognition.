'''
实验名称：火焰检测
平台：01Studio CanMV K230
说明：使用摄像头检测火焰区域（基于HSV颜色空间）
'''

import time
from media.sensor import *
from media.display import *
from media.image import *
from media.media import *

# 初始化摄像头
sensor = Sensor()
sensor.reset()
sensor.set_pixformat(Sensor.RGB565)
sensor.set_framesize(Sensor.QVGA)  # 320x240
sensor.skip_frames(time=2000)

# 初始化显示器
Display.init(Display.VIRT, sensor.width(), sensor.height())
MediaManager.init()
sensor.run()

clock = time.clock()

# HSV火焰颜色范围（可以根据实际光照和火源调整）
# H: 0~30（红-橙） S: 100~255 V: 100~255
thresholds = (0, 30, 100, 255, 100, 255)

while True:
    clock.tick()

    img = sensor.snapshot()

    # 图像转换为HSV（K230用 threshold() 会自动转换处理）
    blobs = img.find_blobs([thresholds], area_threshold=150, merge=True)

    for blob in blobs:
        # 画出火焰区域
        img.draw_rectangle(blob.rect(), color=(255, 0, 0)) # 红框
        img.draw_cross(blob.cx(), blob.cy(), color=(0, 255, 0)) # 中心点
        img.draw_string(blob.x(), blob.y() - 10, "FIRE", scale=1.5, color=(255, 0, 0))

    Display.show_image(img)
    print("FPS:", clock.fps(), "火焰区域数:", len(blobs))