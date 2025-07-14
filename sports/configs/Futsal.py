# sports/configs/Futsal.py
from dataclasses import dataclass, field
from typing import List, Tuple
import cv2

@dataclass
class FutsalPitchConfiguration:
    # ── 寸法 (cm) ──────────────────────────
    width: int  = 2000          # 20 m
    length: int = 4000          # 40 m
    centre_circle_radius: int  = 300   # 3 m
    penalty_spot_distance: int = 600   # 6 m
    penalty_arc_radius: int    = 600   # 6 m
    goal_width: int            = 300   # 3 m

    # ── 描画用パラメータ ──────────────────
    scale: float              = 0.25          # 1 cm → 0.25 px（25 px ≒ 1 m）
    offset: Tuple[int, int]   = (50, 50)      # 余白 (x, y)

    # ─────────────────────────────────────
    @property
    def vertices(self) -> List[Tuple[float, float]]:
        # 0-3: 外枠 / 4-5: センターライン端
        return [
            (0, 0), (0, self.width), (self.length, self.width), (self.length, 0),
            (self.length / 2, 0), (self.length / 2, self.width)
        ]

    edges: List[Tuple[int, int]] = field(
        default_factory=lambda: [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5)]
    )

    labels: List[str]  = field(default_factory=lambda: [""] * 6)
    colors: List[str]  = field(default_factory=lambda: ["#FFFFFF"] * 6)

    # ------------- 内部 util ----------------
    def _px(self, p: Tuple[float, float]) -> Tuple[int, int]:
        return (int(p[0] * self.scale + self.offset[0]),
                int(p[1] * self.scale + self.offset[1]))

    # ------------- 追加ライン ----------------
    def draw_extras(self, img):
        # センターサークル
        cv2.circle(
            img, self._px((self.length / 2, self.width / 2)),
            int(self.centre_circle_radius * self.scale),
            (255, 255, 255), 2
        )
        # 左右ペナルティマーク & アーク
        for x in (self.penalty_spot_distance,
                  self.length - self.penalty_spot_distance):
            spot = self._px((x, self.width / 2))
            cv2.circle(img, spot, 4, (255, 255, 255), -1)
            start, end = (270, 90) if x < self.length / 2 else (90, 270)
            cv2.ellipse(
                img, spot,
                (int(self.penalty_arc_radius * self.scale),) * 2,
                0, start, end, (255, 255, 255), 2
            )
        # ゴール縦線
        g = self.goal_width / 2
        for x in (0, self.length):
            cv2.line(
                img, self._px((x, self.width / 2 - g)),
                self._px((x, self.width / 2 + g)),
                (255, 255, 255), 2
            )
        return img
