from dataclasses import dataclass, field
from typing import List, Tuple
import cv2
import numpy as np


@dataclass
class FutsalPitchConfiguration:
    width: int = 2000  # cm
    length: int = 4000  # cm
    goal_width: int = 300  # cm
    penalty_area_radius: int = 600  # cm
    centre_circle_radius: int = 300  # cm
    penalty_spot_distance: int = 600  # cm

    @property
    def vertices(self) -> List[Tuple[float, float]]:
        return [
            (0, 0),  # 0 左下
            (0, self.width),  # 1 左上
            (self.length, self.width),  # 2 右上
            (self.length, 0),  # 3 右下
            (self.length / 2, 0),  # 4 センター下
            (self.length / 2, self.width),  # 5 センター上
            (self.length / 2, self.width / 2),  # 6 センター中心
            (self.penalty_spot_distance, self.width / 2),  # 7 左ペナルティマーク
            (self.length - self.penalty_spot_distance, self.width / 2),  # 8 右ペナルティマーク
        ]

    edges: List[Tuple[int, int]] = field(default_factory=lambda: [
        (0, 1), (1, 2), (2, 3), (3, 0),  # 外枠
        (4, 5),  # センターライン
    ])

    labels: List[str] = field(default_factory=lambda: [
        "corner_lb", "corner_lt", "corner_rt", "corner_rb",
        "center_bottom", "center_top", "center_circle",
        "penalty_left", "penalty_right"
    ])

    colors: List[str] = field(default_factory=lambda: [
        "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF",
        "#FFFFFF", "#FFFFFF", "#FFFFFF",
        "#FFFFFF", "#FFFFFF"
    ])

    def draw_arcs(self, image):
        # スケーリングが前提（座標変換済みの draw_pitch と互換性あり）
        # センターサークル
        center = self.project((self.length / 2, self.width / 2))
        radius = int(self.centre_circle_radius * self.scale)
        cv2.circle(image, center, radius, (255, 255, 255), 2)

        # 左ペナルティアーク
        left = self.project((self.penalty_spot_distance, self.width / 2))
        cv2.ellipse(image, left,
                    (radius, radius), 0, 270, 90, (255, 255, 255), 2)

        # 右ペナルティアーク
        right = self.project((self.length - self.penalty_spot_distance, self.width / 2))
        cv2.ellipse(image, right,
                    (radius, radius), 0, 90, 270, (255, 255, 255), 2)

        # ペナルティマーク
        cv2.circle(image, left, 4, (255, 255, 255), -1)
        cv2.circle(image, right, 4, (255, 255, 255), -1)

        return image

    # ===== 以下は supervision の draw_pitch に必要な補助関数 =====
    @property
    def scale(self):
        return 25 / 100  # 25px = 1m → 1px = 4cm

    def project(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """座標を supervision.draw.pitch のスケールとオフセットに一致させる"""
        offset_x, offset_y = 20, 10
        x = int(self.scale * (point[0] + offset_x * 100 / 25))
        y = int(self.scale * (point[1] + offset_y * 100 / 25))
        return (x, y)
