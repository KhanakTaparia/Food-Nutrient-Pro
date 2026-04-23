def scale(row, grams):
    factor = grams / 100
    return {k: v * factor for k, v in row.items() if k != "food"}


def bmi(weight, height):
    return weight / (height ** 2)


def calorie_need(weight, height, age, gender):
    base = 10 * weight + 6.25 * height - 5 * age
    return base + (5 if gender == "male" else -161)


def analyze(totals, goal):
    tips = []

    if totals["calories"] > goal:
        tips.append("⚠️ Over calorie limit")
    if totals["protein"] < 60:
        tips.append("💪 Low protein intake")
    if not tips:
        tips.append("✅ Balanced diet today")

    return tips