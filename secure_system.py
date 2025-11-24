import logging
import time
import json
import re

# --- 1. SECURITY CONFIGURATION ---
# Setup secure logging (Standard Library)
logging.basicConfig(
    filename='security_events.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Mock Database (Simulating sensitive data)
CITIZEN_DB = {
    "1010101010": {"name": "Talal Alharbi", "status": "Immune", "vaccine": "Pfizer"},
    "2020202020": {"name": "Sarah Ahmed", "status": "Not Immune", "vaccine": "None"}
}

# Rate Limiting Memory
request_history = {}

class TawakkalnaBackend:
    """
    A secure backend simulation class.
    """
    
    def __init__(self):
        self.valid_token = "NAFATH-SECURE-2025"

    def _check_rate_limit(self, user_ip):
        """Prevents DDoS by limiting requests."""
        current_time = time.time()
        if user_ip not in request_history:
            request_history[user_ip] = []
        
        # Keep only requests from the last 60 seconds
        request_history[user_ip] = [t for t in request_history[user_ip] if current_time - t < 60]
        
        # Limit: 3 requests per minute
        if len(request_history[user_ip]) >= 3:
            logging.warning(f"DoS Prevention: Rate limit exceeded for IP {user_ip}")
            return False
        
        request_history[user_ip].append(current_time)
        return True

    def _validate_input(self, national_id):
        """Ensures ID is exactly 10 digits to prevent Injection attacks."""
        if re.fullmatch(r"^\d{10}$", national_id):
            return True
        logging.warning(f"Input Validation: Invalid ID format detected - {national_id}")
        return False

    def get_citizen_data(self, token, national_id, user_ip="192.168.1.1"):
        """
        The main secure function (API endpoint simulation).
        """
        # 1. Rate Limiting Check
        if not self._check_rate_limit(user_ip):
            return {"error": "Too Many Requests", "code": 429}

        # 2. Access Control (Authentication)
        if token != self.valid_token:
            logging.warning(f"Auth Failure: Invalid token used for ID {national_id}")
            return {"error": "Unauthorized Access", "code": 401}

        # 3. Input Validation
        if not self._validate_input(national_id):
            return {"error": "Invalid Input Format", "code": 400}

        # 4. Data Retrieval
        record = CITIZEN_DB.get(national_id)
        
        if record:
            # 5. Audit Logging (Success)
            logging.info(f"Access Granted: Record {national_id} accessed by authorized user.")
            return {"status": "success", "data": record, "code": 200}
        else:
            # 6. Audit Logging (Not Found)
            logging.info(f"Query: Record {national_id} not found.")
            return {"error": "Record Not Found", "code": 404}