from manim import *
import numpy as np


class RotationLine(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        # ── Manual axes (no LaTeX) ────────────────────────────────────────
        origin_pt = ORIGIN + LEFT * 3 + DOWN * 3   # scene position of (0,0)
        scale = 1.1                                  # pixels per unit

        def p(x, y):
            """Convert data coords to scene coords."""
            return origin_pt + RIGHT * x * scale + UP * y * scale

        # Axis lines
        x_axis = Arrow(p(0, 0), p(5.5, 0), buff=0, color=WHITE, stroke_width=2, tip_length=0.2)
        y_axis = Arrow(p(0, 0), p(0, 5.5), buff=0, color=WHITE, stroke_width=2, tip_length=0.2)

        # Tick marks and labels (1–5)
        ticks = VGroup()
        tick_labels = VGroup()
        for i in range(1, 6):
            # X ticks
            ticks.add(Line(p(i, -0.1), p(i, 0.1), color=WHITE, stroke_width=1.5))
            tick_labels.add(
                Text(str(i), font_size=18, color=WHITE).move_to(p(i, -0.35))
            )
            # Y ticks
            ticks.add(Line(p(-0.1, i), p(0.1, i), color=WHITE, stroke_width=1.5))
            tick_labels.add(
                Text(str(i), font_size=18, color=WHITE).move_to(p(-0.35, i))
            )

        x_label = Text("X", font_size=26, color=WHITE).next_to(x_axis.get_end(), RIGHT, buff=0.1)
        y_label = Text("Y", font_size=26, color=WHITE).next_to(y_axis.get_end(), UP,    buff=0.1)

        self.play(
            Create(x_axis), Create(y_axis),
            Write(x_label), Write(y_label),
            Create(ticks), Write(tick_labels),
            run_time=1,
        )

        # ── Line from (0,0) to (5,0) ──────────────────────────────────────
        origin_scene = p(0, 0)
        end_x_scene  = p(5, 0)

        line     = Line(origin_scene, end_x_scene, color=YELLOW, stroke_width=3)
        dot_orig = Dot(origin_scene, color=RED,    radius=0.09)
        dot_end  = Dot(end_x_scene,  color=YELLOW, radius=0.09)

        self.play(Create(line), FadeIn(dot_orig), FadeIn(dot_end), run_time=0.5)
        self.wait(0.4)

        # ── Arc path for the endpoint ─────────────────────────────────────
        radius_px = scale * 5  # 5 units * scale
        arc_path = Arc(
            radius=radius_px,
            start_angle=0,
            angle=PI / 2,
            arc_center=origin_scene,
        )

        # ── Rotate 90° CCW in 7 s ─────────────────────────────────────────
        self.play(
            Rotating(
                line,
                angle=PI / 2,
                about_point=origin_scene,
                rate_func=linear,
                run_time=7,
            ),
            MoveAlongPath(
                dot_end,
                arc_path,
                rate_func=linear,
                run_time=7,
            ),
        )

        self.wait(1)
