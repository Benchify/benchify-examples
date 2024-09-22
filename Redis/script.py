import redis

def redis_operations():
    # Create a Redis client
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    # Set a key-value pair
    redis_client.set('greeting', 'Hello, Redis!')

    # Get the value for a key
    value = redis_client.get('greeting')
    print(value.decode('utf-8'))  # Decode bytes to string

    # Increment a counter
    redis_client.incr('visitor_count')

    # Get the current count
    count = redis_client.get('visitor_count')
    print(f"Visitor count: {count.decode('utf-8')}")

    # Delete a key
    redis_client.delete('greeting')

    # Check if a key exists
    exists = redis_client.exists('greeting')
    print(f"Does 'greeting' exist? {exists}")

# Call the function to execute Redis operations
if __name__ == "__main__":
    redis_operations()

