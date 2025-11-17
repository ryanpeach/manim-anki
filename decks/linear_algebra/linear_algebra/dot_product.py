import numpy as np
from manim import (
    Scene,
    Axes,
    Arrow,
    MathTex,
    DashedLine,
    Angle,
    VGroup,
    DOWN,
    LEFT,
    UP,
    RIGHT,
    RightAngle,
)
from manim import FadeIn, FadeOut, Create, Write, GrowArrow

A_COLOR = "#00FFD0"
B_COLOR = "#61E47C"
THETA_COLOR = "#FFEA00"
RESULT_COLOR = "#FF9100"


class DotProductScene(Scene):
    def color_all(self, tex: MathTex) -> MathTex:
        """Color all occurrences of a's and b's consistently."""
        pairs = [
            (r"a_1", A_COLOR),
            (r"a_2", A_COLOR),
            (r"\vec a", A_COLOR),
            (r"b_1", B_COLOR),
            (r"b_2", B_COLOR),
            (r"\vec b", B_COLOR),
            (r"\theta", THETA_COLOR),
            (r"\text{scalar}", RESULT_COLOR),
        ]
        for key, color in pairs:
            tex.set_color_by_tex(key, color)
        return tex

    def construct(self):
        # -----------------------------
        # LEFT: STATIC MATH
        # -----------------------------
        vec_defs = MathTex(
            r"\vec a = \begin{bmatrix}a_1 \\ a_2\end{bmatrix}, \quad",
            r"\vec b = \begin{bmatrix}b_1 \\ b_2\end{bmatrix}",
        )
        self.color_all(vec_defs)

        dot_expansion = [
            MathTex(
                r"\vec a \cdot \vec b = a_1 b_1 + a_2 b_2",
                substrings_to_isolate=[
                    r"a_1",
                    r"a_2",
                    r"\vec a",
                    r"b_1",
                    r"b_2",
                    r"\vec b",
                ],
            ),
            MathTex(
                r"\vec a \cdot \vec b = \|\vec a\| \|\vec b\| \cos\theta",
                substrings_to_isolate=[r"\vec a", r"\vec b", r"\theta"],
            ),
            MathTex(
                r"\vec a \cdot \vec b = \text{scalar}",
                substrings_to_isolate=[r"\vec a", r"\vec b", r"\text{scalar}"],
            ),
        ]
        for tex in dot_expansion:
            self.color_all(tex)

        left = VGroup(vec_defs, *dot_expansion).arrange(
            direction=DOWN, aligned_edge=LEFT, buff=0.5
        )
        left.to_edge(LEFT, buff=1)

        # Intro
        self.play(Write(vec_defs))
        for tex in dot_expansion:
            self.play(Write(tex))
        self.wait(0.5)

        # -----------------------------
        # RIGHT: AXES + THREE ROUNDS
        # -----------------------------
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 4, 1],
            x_length=4,
            y_length=4,
            tips=False,
        )
        axes.add_coordinates()
        axes.to_edge(RIGHT, buff=1)

        self.play(Create(axes))

        # Label BELOW x-axis
        proj_label = MathTex(
            r"\text{component of }\vec b\text{ along }\vec a", color=RESULT_COLOR
        ).scale(0.55)
        proj_label.next_to(axes.x_axis, DOWN, buff=0.4)

        # -----------------------------
        # THREE RANDOM VECTORS
        # -----------------------------

        rng = np.random.default_rng(seed=4)

        for _ in range(3):
            # Generate reasonable non-collinear vectors
            theta = 0
            length_diff_ok = False
            while True:
                a_vec = rng.uniform(0.8, 3.2, size=2)
                b_vec = rng.uniform(0.8, 3.2, size=2)
                theta = np.arccos(
                    np.dot(a_vec, b_vec)
                    / (np.linalg.norm(a_vec) * np.linalg.norm(b_vec))
                )
                len_a = np.linalg.norm(a_vec)
                len_b = np.linalg.norm(b_vec)
                length_diff_ok = abs(len_a - len_b) > 0.2 * max(len_a, len_b)
                if np.pi / 4 > theta > np.pi / 8 and length_diff_ok:
                    break

            origin = axes.coords_to_point(0, 0)

            # Main vectors
            arrow_a = Arrow(
                origin,
                axes.coords_to_point(a_vec[0], a_vec[1]),
                buff=0,
                color=A_COLOR,
            )
            arrow_b = Arrow(
                origin,
                axes.coords_to_point(b_vec[0], b_vec[1]),
                buff=0,
                color=B_COLOR,
            )

            label_a = MathTex(r"\vec a", color=A_COLOR).next_to(
                arrow_a.get_end(), RIGHT, buff=0.15
            )
            label_b = MathTex(r"\vec b", color=B_COLOR).next_to(
                arrow_b.get_end(), UP, buff=0.15
            )

            self.play(GrowArrow(arrow_a), FadeIn(label_a))
            self.play(GrowArrow(arrow_b), FadeIn(label_b))
            self.wait(0.3)

            # -------------------------
            # PROJECTION COMPUTATION
            # -------------------------
            a2 = np.dot(a_vec, a_vec)
            ab = np.dot(a_vec, b_vec)
            proj_factor = ab / a2
            proj_vec = proj_factor * a_vec

            proj_point = axes.coords_to_point(proj_vec[0], proj_vec[1])
            b_tip = arrow_b.get_end()

            proj_arrow = Arrow(
                origin,
                proj_point,
                buff=0,
                color=RESULT_COLOR,
                stroke_width=arrow_a.stroke_width / 2,
                tip_length=arrow_a.tip_length / 2,
            )
            drop_line = DashedLine(b_tip, proj_point, color=B_COLOR)
            guide_line = DashedLine(origin, proj_point, color=A_COLOR)
            right_angle = RightAngle(
                drop_line, guide_line, length=0.3, quadrant=(-1, -1)
            )
            right_angle.set_z_index(arrow_a.z_index - 1)

            # angle between a and b
            def angle_from_x(vec):
                return np.arctan2(vec[1], vec[0])

            if angle_from_x(b_vec) > angle_from_x(a_vec):
                angle_arc = Angle(
                    arrow_a,
                    arrow_b,
                    radius=0.45,
                    color=THETA_COLOR,
                )
            else:
                angle_arc = Angle(
                    arrow_b,
                    arrow_a,
                    radius=0.45,
                    color=THETA_COLOR,
                )
            theta_label = MathTex(r"\theta", color=THETA_COLOR).next_to(
                angle_arc, RIGHT, buff=0.05
            )

            # Draw projection geometry
            self.play(Create(angle_arc), FadeIn(theta_label))
            self.play(Create(guide_line))
            self.play(Create(drop_line))
            self.play(Create(right_angle))
            self.play(GrowArrow(proj_arrow))
            self.wait(0.6)

            # Highlight relationship
            # self.play(
            #     Indicate(proj_arrow, scale_factor=1.05),
            #     Indicate(dot_expansion[4], scale_factor=1.05)
            # )
            # self.wait(0.6)

            # Clean up for next round
            self.play(
                FadeOut(
                    VGroup(
                        right_angle,
                        guide_line,
                        arrow_a,
                        arrow_b,
                        label_a,
                        label_b,
                        proj_arrow,
                        drop_line,
                        angle_arc,
                        theta_label,
                    )
                )
            )
            self.wait(0.2)

        # Fade everything out
        self.play(FadeOut(axes))
        self.play(FadeOut(*dot_expansion))
        self.play(FadeOut(vec_defs))

        # end
        self.wait(0.5)
