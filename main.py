# path: /main.py
from include.remy import Remy

def main():
    # Realizar una solicitud HTTP GET
    response = Remy().request_sync('GET', 'https://www.example.com')
    print(f"Status code: {response.status}")

    try:
        print(f"Response content: {response.data.decode()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
