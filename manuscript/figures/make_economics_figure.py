#!/usr/bin/env python3
"""Render the verifier-cost sign map from frozen C3 v2.1 results.

This is a presentation-only transformation. It reads the committed JSON and
does not execute an agent framework, model, verifier, or experiment.
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "gates" / "C3" / "v2_1" / "results_v2_1.json"
OUTPUT = Path(__file__).with_name("verifier_cost_sign_map.png")
FONT_PATH = Path("/System/Library/Fonts/Supplemental/Arial.ttf")


def delta(s: float, rho: float, v: float, rb: float) -> float:
    """Net saving as a fraction of one complete baseline run."""

    return s - v - rho * (s + rb)


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    rb = float(payload["meta"]["RB"])
    task = payload["taskB"]

    width, height = 1995, 640
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(FONT_PATH), 40)
    small = ImageFont.truetype(str(FONT_PATH), 38)
    title_font = ImageFont.truetype(str(FONT_PATH), 44)

    left_margin, right_margin = 190, 34
    top_margin, bottom_margin = 96, 116
    gap = 90
    panel_width = (width - left_margin - right_margin - gap) // 2
    panel_height = height - top_margin - bottom_margin
    y_min, y_max = -0.10, 0.15
    x_min, x_max = 0.0, 0.16

    def point(panel_left: int, x: float, y: float) -> tuple[int, int]:
        px = panel_left + int((x - x_min) / (x_max - x_min) * panel_width)
        py = top_margin + int((y_max - y) / (y_max - y_min) * panel_height)
        return px, py

    for panel_index, arm in enumerate(("reuse", "repair")):
        panel_left = left_margin + panel_index * (panel_width + gap)
        s = float(task["cost"][f"s_{arm}"])
        rho_outcome = float(task[arm]["rho_outcome"])
        rho_blame = float(task[arm]["rho_blame"])

        for y_tick in (-0.10, -0.05, 0.0, 0.05, 0.10, 0.15):
            _, py = point(panel_left, 0.0, y_tick)
            draw.line(
                [(panel_left, py), (panel_left + panel_width, py)],
                fill="#DDDDDD",
                width=2,
            )
            if panel_index == 0:
                label = f"{y_tick:.2f}"
                box = draw.textbbox((0, 0), label, font=small)
                draw.text(
                    (panel_left - 12 - (box[2] - box[0]), py - 20),
                    label,
                    fill="black",
                    font=small,
                )

        for x_tick in (0.0, 0.04, 0.08, 0.12, 0.16):
            px, _ = point(panel_left, x_tick, y_min)
            draw.line(
                [(px, top_margin), (px, top_margin + panel_height)],
                fill="#F0F0F0",
                width=1,
            )
            label = f"{x_tick:.2f}"
            box = draw.textbbox((0, 0), label, font=small)
            draw.text(
                (px - (box[2] - box[0]) / 2, top_margin + panel_height + 14),
                label,
                fill="black",
                font=small,
            )

        for marker_x in (0.01, 0.10):
            px, _ = point(panel_left, marker_x, y_min)
            for py in range(top_margin, top_margin + panel_height, 12):
                draw.line([(px, py), (px, min(py + 5, top_margin + panel_height))], fill="#666666", width=2)

        zero_left = point(panel_left, x_min, 0.0)
        zero_right = point(panel_left, x_max, 0.0)
        draw.line([zero_left, zero_right], fill="black", width=3)
        draw.line(
            [(panel_left, top_margin), (panel_left, top_margin + panel_height)],
            fill="black",
            width=3,
        )
        draw.line(
            [
                (panel_left, top_margin + panel_height),
                (panel_left + panel_width, top_margin + panel_height),
            ],
            fill="black",
            width=3,
        )

        xs = [x_min + i * (x_max - x_min) / 320 for i in range(321)]
        outcome_points = [point(panel_left, x, delta(s, rho_outcome, x, rb)) for x in xs]
        blame_points = [point(panel_left, x, delta(s, rho_blame, x, rb)) for x in xs]
        draw.line(outcome_points, fill="#0072B2", width=6, joint="curve")
        for index in range(0, len(blame_points) - 1, 14):
            draw.line(blame_points[index : index + 8], fill="#A33F00", width=6)

        panel_title = f"{arm.capitalize()} (s={s:.3f})"
        title_box = draw.textbbox((0, 0), panel_title, font=title_font)
        draw.text(
            (
                panel_left + (panel_width - (title_box[2] - title_box[0])) / 2,
                22,
            ),
            panel_title,
            fill="black",
            font=title_font,
        )
        x_label = "verifier cost v = C_verifier / C_full"
        x_box = draw.textbbox((0, 0), x_label, font=font)
        draw.text(
            (
                panel_left + (panel_width - (x_box[2] - x_box[0])) / 2,
                height - 56,
            ),
            x_label,
            fill="black",
            font=font,
        )

    draw.rectangle([(205, 112), (910, 220)], fill="white")
    draw.line([(220, 146), (295, 146)], fill="#0072B2", width=7)
    draw.text((312, 122), "outcome rejection ρ_outcome", fill="#0072B2", font=small)
    for px in range(220, 295, 16):
        draw.line([(px, 195), (min(px + 9, 295), 195)], fill="#A33F00", width=7)
    draw.text((312, 171), "post-hoc ρ_blame", fill="#A33F00", font=small)
    draw.rectangle([(1185, 112), (1935, 220)], fill="white")
    draw.text(
        (width - 780, 122),
        "Dashed curve is analysis-only:\nno runtime directed verifier.",
        fill="#7A3000",
        font=small,
    )

    rotated = Image.new("RGBA", (560, 60), (255, 255, 255, 0))
    rotated_draw = ImageDraw.Draw(rotated)
    rotated_draw.text(
        (0, 4),
        "net saving Δ / C_full",
        fill="black",
        font=font,
    )
    rotated = rotated.rotate(90, expand=True)
    image.paste(rotated, (8, 35), rotated)

    image.save(OUTPUT, dpi=(300, 300), optimize=True)


if __name__ == "__main__":
    main()
