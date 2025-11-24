import unittest
from secure_system import TawakkalnaBackend

class TestSecurityFramework(unittest.TestCase):
    
    def setUp(self):
        self.system = TawakkalnaBackend()
        self.valid_token = "NAFATH-SECURE-2025"
        self.hacker_token = "FAKE-HACKER-TOKEN"

    def test_1_valid_access(self):
        print("\n[TEST 1] Checking Valid User Access...")
        response = self.system.get_citizen_data(self.valid_token, "1010101010")
        
        if response['code'] == 200:
            print("   [PASS] Valid user got data:", response['data'])
        else:
            print("   [FAIL] Valid user was blocked.")
        self.assertEqual(response['code'], 200)

    def test_2_unauthorized_access(self):
        print("\n[TEST 2] Checking Hacker Access (Spoofing)...")
        response = self.system.get_citizen_data(self.hacker_token, "1010101010")
        
        if response['code'] == 401:
            print("   [PASS] Hacker blocked successfully.")
        else:
            print("   [FAIL] Security hole! Hacker got in.")
        self.assertEqual(response['code'], 401)

    def test_3_sql_injection_prevention(self):
        print("\n[TEST 3] Checking Input Validation (Injection)...")
        # Malicious input trying to trick the database
        response = self.system.get_citizen_data(self.valid_token, "101010 OR 1=1")
        
        if response['code'] == 400:
            print("   [PASS] Malicious input rejected.")
        else:
            print("   [FAIL] System accepted bad input.")
        self.assertEqual(response['code'], 400)

    def test_4_rate_limiting(self):
        print("\n[TEST 4] Checking DDoS Protection (Rate Limit)...")
        # Simulate spamming requests
        print("   Sending 4 rapid requests...")
        responses = []
        for _ in range(4):
            responses.append(self.system.get_citizen_data(self.valid_token, "1010101010"))
        
        last_response = responses[-1]
        if last_response['code'] == 429:
            print("   [PASS] Rate limit triggered on 4th request.")
        else:
            print("   [FAIL] Rate limit failed.")
        self.assertEqual(last_response['code'], 429)

if __name__ == '__main__':
    print("--- STARTING SECURITY POC TESTS ---")
    unittest.main()