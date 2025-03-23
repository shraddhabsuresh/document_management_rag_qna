import httpx

response = httpx.post("http://127.0.0.1:8000/api/ask", json={"question": "What is RAG?"})

try:
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", e)
    print("Raw Response:", response.text)
