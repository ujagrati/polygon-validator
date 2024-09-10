import requests
import yaml
import time

# Load config from yaml file
def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

# Send an alert to Telegram
def send_telegram_alert(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Failed to send alert: {response.text}")

# Get the latest checkpoint data
def get_checkpoints(validator_address, rpc_endpoint):
    url = f"{rpc_endpoint.rstrip('/')}/checkpoints?validator={validator_address}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching checkpoints: {e}")
        return None

# Get Bor and Heimdall block heights
def get_block_heights(rpc_endpoint):
    try:
        bor_response = requests.get(f"{rpc_endpoint.rstrip('/')}/bor_block_height")
        bor_response.raise_for_status()
        bor_height = bor_response.json()

        heimdall_response = requests.get(f"{rpc_endpoint.rstrip('/')}/heimdall_block_height")
        heimdall_response.raise_for_status()
        heimdall_height = heimdall_response.json()

        return bor_height, heimdall_height
    except requests.exceptions.RequestException as e:
        print(f"Error fetching block heights: {e}")
        return None, None

# Main monitoring logic
def monitor(config):
    validator_address = config['validator_address']
    rpc_endpoint = config['rpc_endpoint']
    bot_token = config['telegram_bot_token']
    chat_id = config['telegram_chat_id']

    last_bor_height = None
    last_heimdall_height = None
    last_checkpoint_time = None

    while True:
        # Get checkpoints
        checkpoints = get_checkpoints(validator_address, rpc_endpoint)
        if checkpoints is None:
            send_telegram_alert(bot_token, chat_id, "Failed to fetch checkpoint data.")
        else:
            latest_checkpoint_time = checkpoints.get("lastCheckpointTime")
            if last_checkpoint_time is None:
                last_checkpoint_time = latest_checkpoint_time
            elif latest_checkpoint_time == last_checkpoint_time:
                send_telegram_alert(bot_token, chat_id, "No new checkpoint signed or proposed by the validator.")
            else:
                last_checkpoint_time = latest_checkpoint_time

        # Get block heights
        bor_height, heimdall_height = get_block_heights(rpc_endpoint)
        if bor_height is None or heimdall_height is None:
            send_telegram_alert(bot_token, chat_id, "Failed to fetch block heights.")
        else:
            if last_bor_height is not None and bor_height <= last_bor_height:
                send_telegram_alert(bot_token, chat_id, "Bor block height is not increasing.")
            if last_heimdall_height is not None and heimdall_height <= last_heimdall_height:
                send_telegram_alert(bot_token, chat_id, "Heimdall block height is not increasing.")
            if abs(bor_height - heimdall_height) > 1:  # Assume a tolerance of 1 block for sync
                send_telegram_alert(bot_token, chat_id, "Bor and Heimdall heights are out of sync.")

            last_bor_height = bor_height
            last_heimdall_height = heimdall_height

        # Wait before the next check
        time.sleep(60)  # Poll every 60 seconds

if __name__ == "__main__":
    config = load_config("config.yaml")
    monitor(config)
