from matplotlib import pyplot as plt
import cv2
import numpy as np

# フットサルコート用の描画パラメータ
length = 4000  # cm
width = 2000   # cm
centre_circle_radius = 300  # cm
penalty_spot_distance = 600  # cm
penalty_area_radius = 600  # cm
goal_width = 300  # cm

# 空の画像を作成（背景：木目フロア風）
image = np.zeros((int(width * 0.25 + 100), int(length * 0.25 + 100), 3), dtype=np.uint8)
image[:] = (58, 138, 193)[::-1]  # オレンジブラウン系

# 拡大倍率（1ピクセル=4cm）
scale = 0.25

# 線を描画するための関数
def draw_line(p1, p2):
    pt1 = (int(p1[0]*scale+50), int(p1[1]*scale+50))
    pt2 = (int(p2[0]*scale+50), int(p2[1]*scale+50))
    cv2.line(image, pt1, pt2, (255,255,255), 2)

# 四角形（外周）
draw_line((0, 0), (0, width))
draw_line((0, width), (length, width))
draw_line((length, width), (length, 0))
draw_line((length, 0), (0, 0))

# センターライン
draw_line((length/2, 0), (length/2, width))

# ゴール（縦線）
draw_line((0, width/2 - goal_width/2), (0, width/2 + goal_width/2))
draw_line((length, width/2 - goal_width/2), (length, width/2 + goal_width/2))

# センターサークル
center = (int(length/2*scale+50), int(width/2*scale+50))
cv2.circle(image, center, int(centre_circle_radius*scale), (255,255,255), 2)

# ペナルティマーク
cv2.circle(image, (int(penalty_spot_distance*scale+50), int(width/2*scale+50)), 4, (255,255,255), -1)
cv2.circle(image, (int((length - penalty_spot_distance)*scale+50), int(width/2*scale+50)), 4, (255,255,255), -1)

# ペナルティアーク
cv2.ellipse(image,
            (int(penalty_spot_distance*scale+50), int(width/2*scale+50)),
            (int(penalty_area_radius*scale), int(penalty_area_radius*scale)),
            0, 270, 90, (255,255,255), 2)
cv2.ellipse(image,
            (int((length - penalty_spot_distance)*scale+50), int(width/2*scale+50)),
            (int(penalty_area_radius*scale), int(penalty_area_radius*scale)),
            0, 90, 270, (255,255,255), 2)

# 表示
plt.figure(figsize=(10, 5))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.title("Futsal Court (Scaled View)")
plt.show()
