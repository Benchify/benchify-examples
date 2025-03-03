import OpenAI from 'openai';
import * as dotenv from 'dotenv';

// Load environment variables
dotenv.config();

/**
 * Uses OpenAI to generate a response to the given prompt.
 * 
 * @param prompt - The input prompt to send to OpenAI
 * @returns The generated response
 */
async function function1(prompt: string): Promise<string> {
    const openai = new OpenAI({
        apiKey: process.env.OPENAI_API_KEY
    });
    
    const response = await openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: prompt }
        ]
    });
    
    return response.choices[0].message.content || "";
}

/**
 * Calls function1 with the given prompt and returns the response.
 * 
 * @param userPrompt - The prompt to process
 * @returns The response from function1
 */
async function function2(userPrompt: string): Promise<string> {
    console.log(`Sending prompt to OpenAI: ${userPrompt}`);
    const response = await function1(userPrompt);
    console.log("Received response from OpenAI");
    return response;
}

/**
 * Finds the longest common substring between two strings.
 * 
 * @param str1 - First string
 * @param str2 - Second string
 * @returns The longest common substring
 */
function function3(str1: string, str2: string): string {
    if (!str1 || !str2) {
        return "";
    }
    
    // Create a table to store lengths of longest common suffixes
    const m = str1.length;
    const n = str2.length;
    const dp: number[][] = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
    
    // To store the length of longest common substring
    let maxLength = 0;
    // To store the ending position of longest common substring in str1
    let endPos = 0;
    
    // Fill the dp table
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            if (str1[i - 1] === str2[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                if (dp[i][j] > maxLength) {
                    maxLength = dp[i][j];
                    endPos = i;
                }
            }
        }
    }
    
    // Extract the longest common substring
    return str1.substring(endPos - maxLength, endPos);
}

// Example usage
async function main() {
    // Example for function3
    console.log("Testing function3:");
    const result = function3("abcdefg", "bcdxyz");
    console.log(`Longest common substring: ${result}`);
    
    // Example for function2 (which calls function1)
    // Uncomment to test with OpenAI (requires API key)
    // console.log("\nTesting function2:");
    // try {
    //     const response = await function2("Explain the concept of recursion in programming");
    //     console.log(`Response: ${response}`);
    // } catch (error) {
    //     console.error("Error:", error);
    // }
}

main().catch(console.error);