from manim import *
import numpy as np
import random

random.seed(42)
np.random.seed(42)


def generate_fracture_network(n_fractures=35, width=14, height=8):
    """Generate a random fracture network as line segments."""
    fractures = []

    # Horizontal-ish fractures (bedding planes with slight tilt)
    for i in range(10):
        y = random.uniform(-3.5, 3.5)
        x_start = random.uniform(-7, -3)
        x_end = random.uniform(3, 7)
        dy = random.uniform(-0.4, 0.4)
        fractures.append(((x_start, y, 0), (x_end, y + dy, 0)))

    # Vertical-ish fractures (joints)
    for i in range(12):
        x = random.uniform(-6, 6)
        y_start = random.uniform(1.5, 4)
        y_end = random.uniform(-4, -1.5)
        dx = random.uniform(-0.5, 0.5)
        fractures.append(((x, y_start, 0), (x + dx, y_end, 0)))

    # Diagonal fractures
    for i in range(13):
        angle = random.uniform(-60, 60)  # degrees from vertical
        length = random.uniform(1.5, 4.0)
        cx = random.uniform(-6, 6)
        cy = random.uniform(-3, 3)
        rad = np.radians(angle)
        dx = length / 2 * np.sin(rad)
        dy = length / 2 * np.cos(rad)
        fractures.append(
            ((cx - dx, cy + dy, 0), (cx + dx, cy - dy, 0))
        )

    return fractures


def find_flow_path(fractures, start_x, top_y=4.0, bottom_y=-4.0):
    """
    Trace a downward path through the fracture network starting near start_x.
    Returns list of (x, y) waypoints.
    """
    path = [(start_x, top_y)]
    current_x, current_y = start_x, top_y
    visited_segments = set()

    for _ in range(80):
        if current_y <= bottom_y:
            break

        best = None
        best_score = -1e9

        for idx, (p1, p2) in enumerate(fractures):
            if idx in visited_segments:
                continue
            x1, y1, _ = p1
            x2, y2, _ = p2

            # Check if this segment is reachable (close to current position)
            # and goes downward or laterally
            seg_len = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if seg_len < 0.1:
                continue

            # Distance from current point to segment endpoints
            d1 = np.sqrt((x1 - current_x) ** 2 + (y1 - current_y) ** 2)
            d2 = np.sqrt((x2 - current_x) ** 2 + (y2 - current_y) ** 2)

            if min(d1, d2) > 2.0:
                continue

            # Prefer segments that go downward
            if d1 < d2:
                end_x, end_y = x2, y2
                start_dist = d1
            else:
                end_x, end_y = x1, y1
                start_dist = d2

            dy = end_y - current_y
            # Score: reward downward movement, penalise distance
            score = dy - 0.3 * start_dist + random.uniform(-0.3, 0.3)

            if score > best_score:
                best_score = score
                best = (idx, end_x, end_y)

        if best is None:
            # Drift slightly downward if stuck
            current_x += random.uniform(-0.3, 0.3)
            current_y -= random.uniform(0.2, 0.6)
            path.append((current_x, current_y))
        else:
            idx, end_x, end_y = best
            visited_segments.add(idx)
            current_x, current_y = end_x, end_y
            path.append((current_x, current_y))

    # Ensure we reach the bottom
    path.append((current_x, bottom_y))
    return path


class FractureNetworkAnimation(Scene):
    def construct(self):
        # ── Background: dark rock colour ──────────────────────────────────
        self.camera.background_color = "#1a1a2e"

        # ── Title ─────────────────────────────────────────────────────────
        title = Text(
            "Fracture Network – Groundwater Flow",
            font_size=28,
            color=WHITE,
        ).to_edge(UP, buff=0.15)
        subtitle = Text(
            "Water particles migrating through rock fractures under gravity",
            font_size=16,
            color=GRAY,
        ).next_to(title, DOWN, buff=0.05)
        self.add(title, subtitle)

        # ── Rock body (background rectangle) ──────────────────────────────
        rock = Rectangle(
            width=14,
            height=8,
            fill_color="#2d2d44",
            fill_opacity=0.6,
            stroke_width=0,
        )
        self.add(rock)

        # ── Generate and draw fractures ───────────────────────────────────
        fractures = generate_fracture_network()

        fracture_lines = VGroup()
        for p1, p2 in fractures:
            line = Line(
                np.array(p1),
                np.array(p2),
                stroke_color="#8899aa",
                stroke_width=1.2,
                stroke_opacity=0.75,
            )
            fracture_lines.add(line)

        self.play(
            LaggedStart(
                *[Create(l) for l in fracture_lines],
                lag_ratio=0.04,
            ),
            run_time=3,
        )
        self.wait(0.5)

        # ── Particle entry label ──────────────────────────────────────────
        rain_label = Text("↓ rainfall / infiltration", font_size=14, color="#66aaff").move_to(
            UP * 3.7 + LEFT * 3
        )
        self.play(FadeIn(rain_label), run_time=0.5)

        # ── Animate water particles ───────────────────────────────────────
        start_xs = np.linspace(-5.5, 5.5, 12)
        particle_color = "#44aaff"
        trail_color = "#1166cc"

        # Build all paths first
        paths = [find_flow_path(fractures, sx) for sx in start_xs]

        # Animate particles in batches so the scene feels lively
        for batch_start in range(0, len(paths), 3):
            batch_paths = paths[batch_start: batch_start + 3]
            animations = []

            for path in batch_paths:
                dot = Dot(
                    point=np.array([path[0][0], path[0][1], 0]),
                    radius=0.07,
                    color=particle_color,
                    fill_opacity=0.9,
                )

                # Build a VMobject path for the particle to follow
                points = [np.array([x, y, 0]) for x, y in path]
                mob_path = VMobject()
                mob_path.set_points_as_corners(points)

                # Trail effect using UpdateFromAlphaFunc
                trail_dots = []
                for pt in points[::3]:
                    td = Dot(point=pt, radius=0.035, color=trail_color, fill_opacity=0.4)
                    trail_dots.append(td)
                trail_group = VGroup(*trail_dots)

                animations.append(
                    AnimationGroup(
                        MoveAlongPath(dot, mob_path, rate_func=linear),
                        FadeIn(trail_group, run_time=0.1),
                        lag_ratio=0,
                    )
                )
                self.add(dot)

            self.play(*animations, run_time=4)
            self.wait(0.2)

        self.wait(1)

        # ── Final annotation ──────────────────────────────────────────────
        conclusion = Text(
            "Fractures control preferential flow pathways",
            font_size=18,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(Write(conclusion), run_time=1.5)
        self.wait(2)
