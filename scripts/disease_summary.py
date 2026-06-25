import pandas as pd

df = pd.read_excel("data/prediction_logs_25062026.xlsx")

def classify_disease(text):

    text = str(text).lower()

    if "normal" in text:
        return "Normal"

    elif "nodule" in text:
        return "Nodule"

    elif "fracture" in text:
        return "Fracture"

    elif "osteoarthritis" in text:
        return "Osteoarthritis"

    elif (
        "joint space narrowing" in text
        or "degenerative joint disease" in text
    ):
        return "Joint Disease"

    elif "effusion" in text:
        return "Effusion"

    elif (
        "fecal loading" in text
        or "bowel" in text
    ):
        return "Gastrointestinal"

    else:
        return "Others"

df["disease_category"] = (
    df["pred_summary"]
    .apply(classify_disease)
)

summary = (
    df["disease_category"]
    .value_counts()
)

print(summary)