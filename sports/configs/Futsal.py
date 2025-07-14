from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class FutsalPitchConfiguration:
    width: int = 2000  # cm（20m）
    length: int = 4000  # cm（40m）
    penalty_area_radius: int = 600  # 半径6m
    centre_circle_radius: int = 300  # 半径3m
    penalty_spot_distance: int = 600  # 6m

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
        "#00FF00", "#00FF00", "#00FF00",
        "#FF1493", "#FF1493"
    ])

    def draw_arcs(self, image):
        import cv2
        import numpy as np

        # センターサークル
        center = (int(self.length / 2), int(self.width / 2))
        radius = int(self.centre_circle_radius)
        cv2.circle(image, center, radius, (255, 255, 255), 2)

        # 左ペナルティアーク
        left = (int(self.penalty_spot_distance), int(self.width / 2))
        cv2.ellipse(image, left, (radius, radius), 0, 270, 90, (255, 255, 255), 2)

        # 右ペナルティアーク
        right = (int(self.length - self.penalty_spot_distance), int(self.width / 2))
        cv2.ellipse(image, right, (radius, radius), 0, 90, 270, (255, 255, 255), 2)

        return image

