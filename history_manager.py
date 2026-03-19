import json
from datetime import datetime
from pathlib import Path

class HistoryManager:
    def __init__(self, history_file=None):
        self.history_file = str(history_file or Path(__file__).parent / "query_history.json")
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not Path(self.history_file).exists():
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def load_history(self):
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_query(self, query_text, connection_name, success=True, error_message=None, user_request=None):
        """
        Saves a query to the history file.
        Logs timestamp, target DB, the query string, success status,
        and optionally the natural language request that generated the query.
        """
        history = self.load_history()

        entry = {
            "timestamp": datetime.now().isoformat(),
            "connection_name": connection_name,
            "query": query_text.strip(),
            "success": success,
        }

        if user_request:
            entry["user_request"] = user_request.strip()
        if error_message:
            entry["error_message"] = str(error_message)

        history.append(entry)
        
        # Keep the latest 500 items to prevent the file from growing indefinitely (optional, user preference)
        history = history[-500:]

        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

    def get_recent_successful_queries(self, limit=10):
        history = self.load_history()
        successful_queries = [entry for entry in history if entry.get("success")]
        return successful_queries[-limit:]
