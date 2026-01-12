from netmiko import ConnectHandler

def get_running_config(device):
    # Remove 'name' and 'vendor' as they aren't valid Netmiko arguments
    conn_params = {k: v for k, v in device.items() if k not in ['name', 'vendor']}
    with ConnectHandler(**conn_params) as conn:
        return conn.send_command("show running-config")

def apply_config(device, config):
    conn_params = {k: v for k, v in device.items() if k not in ['name', 'vendor']}
    with ConnectHandler(**conn_params) as conn:
        print(f"[+] Sending config to {device['name']}...")
        output = conn.send_config_set(config.split("\n"))
        conn.save_config()
        return output