
import turtle as Eil
import random
import math
import time

screen = Eil.Screen()
screen.setup(1200, 900)
screen.bgcolor("#050713")
screen.title("Aylin's Random Galaxy")

screen.tracer(0)

BLUE = "#075BFF"
WHITE = "#FFFFFF"
YELLOW = "#FFD700"
PINK = "#FF69B4"
LIGHT_PINK = "#FFB6C1"

star_colors = [
    "#D4AF37",
    "#B76E79",
    "#FF69B4",
    "#1677FF",
    "#FFFFFF"
]

flower_colors = [
    (PINK, YELLOW),
    (PINK, WHITE),
    (LIGHT_PINK, YELLOW),
    (WHITE, PINK),
    (PINK, LIGHT_PINK),
    (WHITE, YELLOW),
    (YELLOW, WHITE),
    (WHITE, WHITE)
]

spirals = []

center_pen = Eil.Turtle()
center_pen.hideturtle()
center_pen.speed(0)
center_pen.pensize(4)
center_pen.penup()
center_pen.goto(0, 0)
center_pen.setheading(0)
center_pen.pendown()

spirals.append({
    "pen": center_pen,
    "step": 0,
    "length": 3.5,
    "growth": 0.14,
    "turn": 15,
    "total": 280,
    "colors": [BLUE, WHITE, LIGHT_PINK],
    "delay": 0,
    "pace": 0.90
})

for i in range(7):

    p = Eil.Turtle()
    p.hideturtle()
    p.speed(0)

    color = random.choice([BLUE, BLUE, WHITE])
    p.pencolor(color)

    x = random.randint(-460, 460)
    y = random.randint(-340, 340)

    if -160 < x < 160 and -160 < y < 160:
        x += 220 if x >= 0 else -220

    p.penup()
    p.goto(x, y)
    p.setheading(random.randint(0, 360))
    p.pendown()

    if color == BLUE:
        p.pensize(3)
        start_len = random.uniform(2.8, 3.8)
        growth = random.uniform(0.10, 0.14)
        turn = random.randint(14, 17)
        total_steps = random.randint(150, 190)

    else:
        p.pensize(2)
        start_len = random.uniform(2.2, 3.0)
        growth = random.uniform(0.07, 0.10)
        turn = random.randint(15, 19)
        total_steps = random.randint(115, 145)

    spirals.append({
        "pen": p,
        "step": 0,
        "length": start_len,
        "growth": growth,
        "turn": turn,
        "total": total_steps,
        "colors": [color],
        "delay": random.randint(5, 75),
        "pace": random.uniform(0.55, 0.95)
    })


def create_star_path(x, y, size, color):

    pen = Eil.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.pencolor(color)
    pen.pensize(random.choice([2, 3]))

    vertices = []
    rotation = random.randint(0, 360)

    for i in range(5):
        angle = math.radians(90 + rotation + i * 72)
        px = x + size * math.cos(angle)
        py = y + size * math.sin(angle)
        vertices.append((px, py))

    order = [0, 2, 4, 1, 3, 0]

    waypoints = []
    step_size = random.uniform(5.0, 11.0)

    for idx in range(5):
        p1 = vertices[order[idx]]
        p2 = vertices[order[idx + 1]]

        dist = math.hypot(
            p2[0] - p1[0],
            p2[1] - p1[1]
        )

        steps = max(2, int(dist / step_size))

        for s in range(1, steps + 1):
            t_ratio = s / steps

            wx = p1[0] + (p2[0] - p1[0]) * t_ratio
            wy = p1[1] + (p2[1] - p1[1]) * t_ratio

            waypoints.append((wx, wy))

    pen.penup()
    pen.goto(vertices[order[0]])

    return {
        "pen": pen,
        "waypoints": waypoints,
        "step": 0,
        "total": len(waypoints),
        "pace": random.uniform(0.60, 0.98)
    }


def create_flower_path(x, y, size, petal_color, center_color):

    pen = Eil.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.pensize(random.choice([2, 3]))

    waypoints = []
    rotation = math.radians(random.randint(0, 360))

    steps_per_petal = 14

    for p in range(5):
        base_angle = rotation + p * (2 * math.pi / 5)

        for s in range(steps_per_petal + 1):
            t_val = (s / steps_per_petal) * math.pi
            r = size * (math.sin(t_val) ** 0.65)

            theta = (
                base_angle
                + (t_val / math.pi) * (2 * math.pi / 5) * 0.88
            )

            wx = x + r * math.cos(theta)
            wy = y + r * math.sin(theta)

            waypoints.append((wx, wy, petal_color, True))

    center_radius = size * 0.22
    center_steps = 12

    for s in range(center_steps + 1):
        ang = (s / center_steps) * 2 * math.pi

        wx = x + center_radius * math.cos(ang)
        wy = y + center_radius * math.sin(ang)

        draw_line = False if s == 0 else True

        waypoints.append((wx, wy, center_color, draw_line))

    pen.penup()
    pen.goto(x, y)

    return {
        "pen": pen,
        "waypoints": waypoints,
        "step": 0,
        "total": len(waypoints),
        "pace": random.uniform(0.55, 0.92)
    }


stars = []

for i in range(17):
    sx = random.randint(-520, 520)
    sy = random.randint(-370, 370)
    ssize = random.randint(25, 65)
    scolor = random.choice(star_colors)

    stars.append(
        create_star_path(sx, sy, ssize, scolor)
    )

random.shuffle(stars)

flowers = []

for i in range(11):
    fx = random.randint(-500, 500)
    fy = random.randint(-360, 360)
    fsize = random.randint(22, 48)

    p_col, c_col = random.choice(flower_colors)

    flowers.append(
        create_flower_path(fx, fy, fsize, p_col, c_col)
    )

random.shuffle(flowers)

active_stars = []
next_star_idx = 0

active_flowers = []
next_flower_idx = 0

frame = 0

while (
    any(s["step"] < s["total"] for s in spirals)
    or any(st["step"] < st["total"] for st in stars)
    or any(fl["step"] < fl["total"] for fl in flowers)
):

    spirals_done = all(
        s["step"] >= s["total"] for s in spirals
    )

    for s in spirals:

        if frame >= s["delay"] and s["step"] < s["total"]:

            if random.random() < s["pace"]:

                p = s["pen"]
                step = s["step"]

                if len(s["colors"]) > 1:
                    p.pencolor(
                        s["colors"][(step // 4) % 2]
                    )

                p.forward(s["length"])
                p.right(s["turn"])

                s["length"] += s["growth"]
                s["step"] += 1

    if next_star_idx < len(stars) and (
        random.random() < 0.065 or spirals_done
    ):
        active_stars.append(stars[next_star_idx])
        next_star_idx += 1

    if next_flower_idx < len(flowers) and (
        random.random() < 0.060 or spirals_done
    ):
        active_flowers.append(flowers[next_flower_idx])
        next_flower_idx += 1

    for st in active_stars:

        if st["step"] < st["total"] and random.random() < st["pace"]:

            wx, wy = st["waypoints"][st["step"]]

            if st["step"] == 0:
                st["pen"].penup()
                st["pen"].goto(wx, wy)
                st["pen"].pendown()
            else:
                st["pen"].goto(wx, wy)

            st["step"] += 1

    for fl in active_flowers:

        if fl["step"] < fl["total"] and random.random() < fl["pace"]:

            wx, wy, col, draw_line = fl["waypoints"][fl["step"]]

            fl["pen"].pencolor(col)

            if not draw_line:
                fl["pen"].penup()
                fl["pen"].goto(wx, wy)
                fl["pen"].pendown()
            else:
                fl["pen"].goto(wx, wy)

            fl["step"] += 1

    screen.update()
    time.sleep(0.018)
    frame += 1

Eil.done()
