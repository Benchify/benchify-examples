import os
import openai

def function1(prompt):
    """
    Use OpenAI to generate a response to the given prompt.
    
    Args:
        prompt (str): The input prompt to send to OpenAI
        
    Returns:
        str: The generated response
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def function2(user_prompt):
    """
    Call function1 with the given prompt and return the response.
    
    Args:
        user_prompt (str): The prompt to process
        
    Returns:
        str: The response from function1
    """
    print(f"Sending prompt to OpenAI: {user_prompt}")
    response = function1(user_prompt)
    print(f"Received response from OpenAI")
    return response

def function3(str1, str2):
    """
    Find the longest common substring between two strings.
    
    Args:
        str1 (str): First string
        str2 (str): Second string
        
    Returns:
        str: The longest common substring
    """
    if not str1 or not str2:
        return ""
    
    # Create a table to store lengths of longest common suffixes
    m, n = len(str1), len(str2)
    dp = [[0 for _ in range(n+1)] for _ in range(m+1)]
    
    # To store the length of longest common substring
    max_length = 0
    # To store the ending position of longest common substring in str1
    end_pos = 0
    
    # Fill the dp table
    for i in range(1, m+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                if dp[i][j] > max_length:
                    max_length = dp[i][j]
                    end_pos = i
    
    # Extract the longest common substring
    return str1[end_pos - max_length:end_pos]

# Example usage
if __name__ == "__main__":
    # Example for function3
    print("Testing function3:")
    result = function3("abcdefg", "bcdxyz")
    print(f"Longest common substring: {result}")
    
    # Example for function2 (which calls function1)
    # Uncomment to test with OpenAI (requires API key)
    # print("\nTesting function2:")
    # response = function2("Explain the concept of recursion in programming")
    # print(f"Response: {response}")