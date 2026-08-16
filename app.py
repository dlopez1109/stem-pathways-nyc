import pandas as pd

# Load our STEM opportunity database
opportunities = pd.read_csv("data/opportunities.csv")

# Example student profile
student = {
    "grade": "11",
    "location": "NYC",
    "interests": ["Engineering", "Computer Science"],
    "experience_level": "Beginner",
    "needs_free": True
}


def calculate_match(student, opportunity):
    score = 0

    grades = str(opportunity["grades"]).split(";")
    fields = str(opportunity["fields"]).split(";")

    # Grade match
    if student["grade"] in grades:
        score += 25

    # Location match
    if student["location"].lower() == str(opportunity["location"]).lower():
        score += 20

    # STEM interest match
    if any(interest in fields for interest in student["interests"]):
        score += 25

    # Experience level match
    if student["experience_level"].lower() == str(
        opportunity["experience_level"]
    ).lower():
        score += 15

    # Financial accessibility
    if student["needs_free"] and str(opportunity["cost"]).lower() == "free":
        score += 15

    return score


# Calculate matches
results = []

for _, opportunity in opportunities.iterrows():
    score = calculate_match(student, opportunity)

    results.append({
        "name": opportunity["name"],
        "match_score": score
    })


# Rank best matches first
results = sorted(
    results,
    key=lambda x: x["match_score"],
    reverse=True
)


print("STEM PATHWAYS NYC")
print("-----------------")
print("\nTop Opportunity Matches:\n")

for result in results:
    print(f'{result["name"]}: {result["match_score"]}% match')
