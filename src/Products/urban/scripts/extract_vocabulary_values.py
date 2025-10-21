import json

# Step 1: Load data from JSON file
with open("form_composition_data.json", "r") as f:
    data = json.load(f)  # this should be a list of dicts

# Step 2: Extract only 'id' and 'title'
result = [{"id": item.get("id"), "title": item.get("title")} for item in data]

# Step 3 (optional): Save result to a new JSON file
with open("filtered_values.json", "w") as f:
    json.dump(result, f, indent=4)

# Print to check
print(result)