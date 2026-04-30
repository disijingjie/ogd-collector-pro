import math

# 圆心(100,100), 半径90
# SVG: 0°=3点钟, 顺时针增加。12点钟=-90°

cx, cy, r = 100, 100, 90

# 数据
data = [
    ("静态页面型", 47.7, "#2563eb"),
    ("动态渲染型", 27.3, "#059669"),
    ("接口API型", 15.9, "#d97706"),
    ("混合型", 9.1, "#db2777"),
]

current_angle = -90  # 12点钟方向

for name, pct, color in data:
    angle_span = pct / 100 * 360
    start_angle = current_angle
    end_angle = current_angle + angle_span

    # 起点坐标
    rad1 = math.radians(start_angle)
    x1 = cx + r * math.cos(rad1)
    y1 = cy + r * math.sin(rad1)

    # 终点坐标
    rad2 = math.radians(end_angle)
    x2 = cx + r * math.cos(rad2)
    y2 = cy + r * math.sin(rad2)

    large_arc = 1 if angle_span > 180 else 0

    print(f"<!-- {name} {pct}% = {angle_span:.2f}° ({start_angle:.2f}° → {end_angle:.2f}°) -->")
    print(f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large_arc} 1 {x2:.1f},{y2:.1f} z" fill="{color}" stroke="#fff" stroke-width="2"/>')

    current_angle = end_angle

print(f"\nTotal angle: {current_angle + 90:.2f}° (should be 360°)")
