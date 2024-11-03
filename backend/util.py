import re


# Define a function to extract each section of a test generation response
def extract_sections(text):
    sections = {}
    # Regex to match each section with more specificity
    patterns = {
        "persona": r"(?<=Persona:\s)(.*?)(?=\n\nTask:|$)",
        "task": r"(?<=Task:\s)(.*?)(?=\n\nGoal:|$)",
        "goal": r"(?<=Goal:\s)(.*?)(?=\n\n|$)"
    }
    # Extract each section based on its pattern
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            sections[key] = match.group(0).strip()
    return sections
