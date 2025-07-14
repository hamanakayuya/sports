from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class FutsalPitchConfiguration:
    width: int = 2000  # cm = 20m
    length: int = 4000  # cm = 40m
    goal_width: int = 300  # cm = 3m
    penalty_area_radius: int = 600  # 6m
    centre_circle_radius: int = 300  # 3m
    penalty_spot_distance: int = 600  # 6m

    @property
    def vertices(self) -> List[Tuple[int, int]]:
        return [
            (0, 0),  # 0: 左下角
            (0, self.width),  # 1: 左上角
            (self.length, self.width),  # 2: 右上角
            (self.length, 0),  # 3: 右下角
            (self.length // 2, 0),  # 4: センター下
            (self.length // 2, self.width),  # 5: センター上
            (self.length // 2, self.width // 2),  # 6: センター中央
        ]

    edges: List[Tuple[int, int]] = field(default_factory=lambda: [
        (0, 1), (1, 2), (2, 3), (3, 0),  # 外枠
        (4, 5),  # センターライン
    ])

    labels: List[str] = field(default_factory=lambda: [
        "left_bottom", "left_top", "right_top", "right_bottom",
        "center_bottom", "center_top", "center_point"
    ])

    colors: List[str] = field(default_factory=lambda: [
        "#FFFFFF", "#FFFFFF", "#FFFFFF", "#FFFFFF",
        "#FFFFFF", "#FFFFFF", "#FFFFFF"
    ])

    def draw_arcs(self, image):
        import cv2

        # センターサークル
        center = (int(self.length / 2), int(self.width / 2))
        cv2.circle(image, center, self.centre_circle_radius, (255, 255, 255), 2)

        # 左ペナルティアーク（外向き）
        left_arc_center = (self.penalty_spot_distance, self.width // 2)
        cv2.ellipse(image, left_arc_center,
                    (self.penalty_area_radius, self.penalty_area_radius),
                    0, 270, 90, (255, 255, 255), 2)

        # 右ペナルティアーク（外向き）
        right_arc_center = (self.length - self.penalty_spot_distance, self.width // 2)
        cv2.ellipse(image, right_arc_center,
                    (self.penalty_area_radius, self.penalty_area_radius),
                    0, 90, 270, (255, 255, 255), 2)

        # ゴール（簡略表現：外枠の中央部に直線を描く）
        goal_line_length = self.goal_width
        # 左ゴール
        cv2.line(image,
                 (0, self.width // 2 - goal_line_length // 2),
                 (0, self.width // 2 + goal_line_length // 2),
                 (255, 255, 255), 2)
        # 右ゴール
        cv2.line(image,
                 (self.length, self.width // 2 - goal_line_length // 2),
                 (self.length, self.width // 2 + goal_line_length // 2),
                 (255, 255, 255), 2)

        # ペナルティマーク
        cv2.circle(image, (self.penalty_spot_distance, self.width // 2), 5, (255, 255, 255), -1)
        cv2.circle(image, (self.length - self.penalty_spot_distance, self.width // 2), 5, (255, 255, 255), -1)

        return image
