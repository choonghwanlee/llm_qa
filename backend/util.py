import re


# Define a function to extract each section of a test generation response
def extract_sections(text):
    sections = {}
    # Regex to match each section
    patterns = {
        "Persona": r"Persona:\s*(.*?)(?=\n\n|$)",
        "Task": r"Task:\s*(.*?)(?=\n\n|$)",
        "Goal": r"Goal:\s*(.*?)(?=\n\n|$)"
    }
    # Extract each section based on its pattern
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL)
        if match:
            sections[key] = match.group(1).strip()
    return sections
