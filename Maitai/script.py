import aiohttp
import asyncio
from quart import Quart, jsonify, request

app = Quart(__name__)

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

@app.route('/fetch', methods=['POST'])
async def fetch():
    data = await request.get_json()
    urls = data.get('urls', [])

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        responses = await asyncio.gather(*tasks)
    
    return jsonify({"responses": responses})

@app.route('/')
async def index():
    return "Welcome to the Quart aiohttp example!"

if __name__ == '__main__':
    app.run(debug=True)

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        # Flag to detect if any swap happened during this pass
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        
        # If no elements were swapped, the array is already sorted
        if not swapped:
            break

    return arr
