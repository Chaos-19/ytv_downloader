# Global dictionary to store temporary data for each chat (e.g., URL, status)
import json

temporary_data = {}

def set_data(chat_id, data):
    """Set temporary data for a specific chat"""
    temporary_data[chat_id] = data

def get_data(chat_id):
    """Get temporary data for a specific chat"""
    print(json.dumps(temporary_data))
    return temporary_data.get(chat_id, None)

def delete_data(chat_id):
    """Delete temporary data for a specific chat"""
    if chat_id in temporary_data:
        del temporary_data[chat_id]