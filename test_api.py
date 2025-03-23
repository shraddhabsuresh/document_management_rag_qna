import httpx

response = httpx.post("http://127.0.0.1:8000/api/ask", json={"question": "What is RAG?"})
print(response.status_code, response.json())
