import os
import yaml
from openai import OpenAI
from netmiko import ConnectHandler

# 1. Setup OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_config(intent):
    prompt = f"Generate Cisco IOS CLI commands for: {intent}. Provide only the commands, no explanation."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def main():
    # 2. Get Device Details from GitHub Secrets
    device = {
        "device_type": "cisco_ios",
        "host": os.getenv("DEVICE_IP"),
        "username": os.getenv("DEVICE_USER"),
        "password": os.getenv("DEVICE_PASS"),
    }

    # 3. Define what you want to do
    intent = "Configure interface Loopback0 with description 'GitHub_Automation' and IP 1.1.1.1 255.255.255.255"

    print(f"Asking AI to generate config for: {intent}")
    config_commands = get_ai_config(intent)
    
    print(f"Applying following commands to {device['host']}:\n{config_commands}")

    # 4. Push to Device
    try:
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_config_set(config_commands.split("\n"))
            print("SUCCESS! Output:")
            print(output)
    except Exception as e:
        print(f"FAILED to connect to {device['host']}: {e}")

if __name__ == "__main__":
    main()
    