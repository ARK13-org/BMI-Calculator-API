def classify_bmi(bmi: float) -> str:
    # Adult BMI reference categories; BMI is a screening measure, not a diagnosis.
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    if bmi < 35:
        return "Obesity Class I"
    if bmi < 40:
        return "Obesity Class II"
    return "Obesity Class III"


def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m * height_m), 2)


def healthy_weight_range(height_cm: float) -> tuple[float, float]:
    height_m = height_cm / 100
    return round(18.5 * height_m * height_m, 1), round(24.9 * height_m * height_m, 1)
