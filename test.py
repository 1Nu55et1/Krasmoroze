# path: /test.py
import requests

def main():
    # Realizar una solicitud HTTP GET
    response = requests.get('https://www.example.com')
    print(f"Status code: {response.status_code}")

    try:
        print(f"Response content: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
