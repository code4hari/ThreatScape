import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

def analyze_network_data(csv_file):
    df = pd.read_csv(csv_file)
    
    data_summary = df.describe().to_string()
    

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")
        
    client = Anthropic(api_key=api_key)
    
    prompt = f"""Please analyze this network packet dataset for potential security threats or anomalies. 
    Consider patterns in packet counts, bytes, and protocol distributions.
    Pay special attention to:
    1. Unusual packet count or byte patterns
    2. Protocol distribution anomalies (TCP, UDP, ICMP)
    3. Potential indicators of malicious activity
    4. Any suspicious patterns in HTTP traffic
    
    Here's the statistical summary of the dataset:
    {data_summary}
    
    Here's a sample of the raw data:
    {df.head().to_string()}
    
    Please provide:
    1. The specific type of attack (DDos, Dos, etc).
    2. Explanation of why these patterns might indicate the specified attack
    3. Recommendations to fix the issue
    """
    
    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            system="You are a network security analyst specialized in identifying threats and anomalies in network traffic data.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        
        print("\nClaude's Security Analysis:")
        print(response.content[0].text)  
        
    except Exception as e:
        print(f"API Error: {str(e)}")

if __name__ == "__main__":
    csv_file = "C:/360/final project/ThreatScape/datasets/dos_attack_dataset.csv"
    
    try:
        analyze_network_data(csv_file)
    except Exception as e:
        print(f"Error occurred: {str(e)}")