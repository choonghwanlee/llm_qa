import os
from supabase import create_client, Client

# Initialize the Supabase client
url: str = "https://hpqjqscppcxkorulngck.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhwcWpxc2NwcGN4a29ydWxuZ2NrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzA1MTI1MjMsImV4cCI6MjA0NjA4ODUyM30.mQyDxrnj49FcO839wDlIVbSspTXJ2NlienlfeWSq6Lw"
supabase: Client = create_client(url, key)

def update_metrics(test_id, updated_data):
    # Update the row in the "LLMQA" table using the given test_id
    response = supabase.table('LLMQA').update(updated_data).eq('test_id', test_id).execute()

    if response.status_code == 200:
        print("Update successful:", response.data)
    else:
        print("Error updating data:", response.error)

# Define the test_id of the row to update and the new metrics
test_id = "your-test-id-uuid"  # Replace with the UUID of the test_id you want to update
updated_data = {
    'repetitiveness_metric': 0.75,
    'helpfulness_metric': 0.85,
    'goal_completion_accuracy': 0.90,
    # Add more fields here if needed
}

update_metrics(test_id, updated_data)
