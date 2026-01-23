import requests
import sys
from datetime import datetime

class AskMyCityAPITester:
    def __init__(self, base_url="https://urbanguide-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, expected_data_checks=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, timeout=10)

            print(f"Status Code: {response.status_code}")
            
            success = response.status_code == expected_status
            
            if success:
                try:
                    response_data = response.json()
                    print(f"Response: {response_data}")
                    
                    # Additional data validation if provided
                    if expected_data_checks:
                        for check_name, check_func in expected_data_checks.items():
                            if not check_func(response_data):
                                success = False
                                print(f"❌ Data validation failed: {check_name}")
                                break
                    
                    if success:
                        self.tests_passed += 1
                        print(f"✅ Passed - {name}")
                    
                except Exception as e:
                    success = False
                    print(f"❌ Failed to parse JSON response: {str(e)}")
                    
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                if response.text:
                    print(f"Response: {response.text}")

            if not success:
                self.failed_tests.append({
                    'name': name,
                    'endpoint': endpoint,
                    'expected_status': expected_status,
                    'actual_status': response.status_code,
                    'response': response.text[:200] if response.text else 'No response'
                })

            return success, response.json() if success and response.text else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                'name': name,
                'endpoint': endpoint,
                'error': str(e)
            })
            return False, {}

    def test_health_check(self):
        """Test API health check"""
        return self.run_test(
            "API Health Check",
            "GET",
            "api/",
            200,
            expected_data_checks={
                'has_message': lambda data: 'message' in data
            }
        )

    def test_get_cities(self):
        """Test getting all cities"""
        success, response = self.run_test(
            "Get All Cities",
            "GET",
            "api/cities",
            200,
            expected_data_checks={
                'is_list': lambda data: isinstance(data, list),
                'has_three_cities': lambda data: len(data) == 3,
                'has_required_fields': lambda data: all('name' in city and 'slug' in city for city in data),
                'has_expected_cities': lambda data: set(city['slug'] for city in data) == {'delhi', 'mumbai', 'bangalore'}
            }
        )
        return success, response

    def test_get_city_services(self, city_slug, expected_city_name):
        """Test getting services for a specific city"""
        success, response = self.run_test(
            f"Get {expected_city_name} Services",
            "GET",
            f"api/cities/{city_slug}",
            200,
            expected_data_checks={
                'has_name': lambda data: data.get('name') == expected_city_name,
                'has_slug': lambda data: data.get('slug') == city_slug,
                'has_services': lambda data: 'services' in data and isinstance(data['services'], list),
                'has_four_services': lambda data: len(data.get('services', [])) == 4,
                'has_service_types': lambda data: set(service['service_type'] for service in data.get('services', [])) == {'Emergency', 'Hospital', 'Police', 'Helpline'},
                'services_have_required_fields': lambda data: all(
                    all(field in service for field in ['service_type', 'contact', 'description', 'city_slug'])
                    for service in data.get('services', [])
                )
            }
        )
        return success, response

    def test_invalid_city(self):
        """Test getting services for non-existent city"""
        return self.run_test(
            "Invalid City (404 Test)",
            "GET",
            "api/cities/nonexistent",
            404
        )

def main():
    print("🚀 Starting AskMyCity API Tests")
    print("=" * 50)
    
    # Setup
    tester = AskMyCityAPITester()

    # Run tests
    print("\n📋 Running Backend API Tests...")
    
    # Test 1: Health check
    tester.test_health_check()
    
    # Test 2: Get all cities
    cities_success, cities_data = tester.test_get_cities()
    
    # Test 3: Get services for each city
    if cities_success:
        test_cities = [
            ('delhi', 'Delhi'),
            ('mumbai', 'Mumbai'),
            ('bangalore', 'Bangalore')
        ]
        
        for city_slug, city_name in test_cities:
            tester.test_get_city_services(city_slug, city_name)
    
    # Test 4: Invalid city (should return 404)
    tester.test_invalid_city()

    # Print results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    
    if tester.failed_tests:
        print("\n❌ Failed Tests:")
        for failed_test in tester.failed_tests:
            error_msg = failed_test.get('error', f'Status {failed_test.get("actual_status", "unknown")}')
            print(f"  - {failed_test['name']}: {error_msg}")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())