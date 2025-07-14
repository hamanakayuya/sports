from dataclasses import dataclass, field
from typing import List, Tuple
import cv2

@dataclass
class FutsalPitchConfiguration:
    width: int = 2000
    length: int = 4000
    centre_circle_radius: int = 300
    penalty_spot_distance: int = 600
    penalty_arc_radius: int = 600
    goal_width: int = 300

    @property
    def vertices(self) -> List[Tuple[float, float]]:
        return [
            (0, 0), (0, self.width), (self.length, self.width), (self.length, 0),
            (self.length / 2, 0), (self.length / 2, self.width),
        ]

    edges: List[Tuple[int, int]] = field(default_factory=lambda: [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5),
    ])

    def draw_arcs(self, image, scale: float, offset: Tuple[int, int]):
        center = (int(self.length / 2 * scale + offset[0]), int(self.width / 2 * scale + offset[1]))
        radius = int(self.centre_circle_radius * scale)
        cv2.circle(image, center, radius, (255, 255, 255), 2)

        left_spot = (int(self.penalty_spot_distance * scale + offset[0]), int(self.width / 2 * scale + offset[1]))
        right_spot = (int((self.length - self.penalty_spot_distance) * scale + offset[0]), int(self.width / 2 * scale + offset[1]))
        cv2.circle(image, left_spot, 4, (255, 255, 255), -1)
        cv2.circle(image, right_spot, 4, (255, 255, 255), -1)

        cv2.ellipse(image, left_spot, (radius, radius), 0, 270, 90, (255, 255, 255), 2)
        cv2.ellipse(image, right_spot, (radius, radius), 0, 90, 270, (255, 255, 255), 2)

        goal_half = self.goal_width / 2
        cv2.line(image,
                 (int(0 * scale + offset[0]), int((self.width / 2 - goal_half) * scale + offset[1])),
                 (int(0 * scale + offset[0]), int((self.width / 2 + goal_half) * scale + offset[1])),
                 (255, 255, 255), 2)
        cv2.line(image,
                 (int(self.length * scale + offset[0]), int((self.width / 2 - goal_half) * scale + offset[1])),
                 (int(self.length * scale + offset[0]), int((self.width / 2 + goal_half) * scale + offset[1])),
                 (255, 255, 255), 2)
        return image
