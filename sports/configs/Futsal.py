from dataclasses import dataclass, field
from typing import List, Tuple
import cv2

@dataclass
class FutsalPitchConfiguration:
    # ── サイズ設定（cm 単位）──────────────────────
    width: int  = 2000          # コート短辺（20 m）
    length: int = 4000          # コート長辺（40 m）
    centre_circle_radius: int   = 300   # センターサークル半径（3 m）
    penalty_spot_distance: int  = 600   # ペナルティマークまでの距離（6 m）
    penalty_arc_radius: int     = 600   # ペナルティアーク半径（6 m）
    goal_width: int             = 300   # ゴール幅（3 m）

    # ── 描画用スケール & 余白（px）───────────────
    scale: float               = 0.25            # 1 cm → 0.25 px  (25 px ≒ 1 m)
    offset: Tuple[int, int]    = (50, 50)        # (x, y) マージン

    # ── 頂点定義（長方形 + センターライン端）────
    @property
    def vertices(self) -> List[Tuple[float, float]]:
        return [
            (0, 0),                         # 0 左下
            (0, self.width),                # 1 左上
            (self.length, self.width),      # 2 右上
            (self.length, 0),               # 3 右下
            (self.length / 2, 0),           # 4 センター下
            (self.length / 2, self.width)   # 5 センター上
        ]

    # ── 線分（edges）──
    edges: List[Tuple[int, int]] = field(default_factory=lambda: [
        (0, 1), (1, 2), (2, 3), (3, 0),   # 外枠
        (4, 5)                            # センターライン
    ])

    # ────────────────────────────────────────────
    def _to_px(self, point: Tuple[float, float]) -> Tuple[int, int]:
        """cm 座標 → 描画ピクセル座標へ変換"""
        return (
            int(point[0] * self.scale + self.offset[0]),
            int(point[1] * self.scale + self.offset[1])
        )

    def draw_arcs(self, image):
        """センターサークル・ペナルティアーク・ゴール線などを描画"""
        # センターサークル
        cv2.circle(
            image,
            self._to_px((self.length / 2, self.width / 2)),
            int(self.centre_circle_radius * self.scale),
            (255, 255, 255), 2
        )

        # ペナルティマーク & アーク
        for x_cm in (self.penalty_spot_distance, self.length - self.penalty_spot_distance):
            spot = self._to_px((x_cm, self.width / 2))
            cv2.circle(image, spot, 4, (255, 255, 255), -1)

            # アーク（左: 270→90°, 右: 90→270°）
            start, end = (270, 90) if x_cm < self.length / 2 else (90, 270)
            cv2.ellipse(
                image, spot,
                (int(self.penalty_arc_radius * self.scale),) * 2,
                0, start, end, (255, 255, 255), 2
            )

        # ゴール縦線
        g_half = self.goal_width / 2
        for x_cm in (0, self.length):
            p1 = self._to_px((x_cm, self.width / 2 - g_half))
            p2 = self._to_px((x_cm, self.width / 2 + g_half))
            cv2.line(image, p1, p2, (255, 255, 255), 2)

        return image
