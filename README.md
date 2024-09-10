# **Polygon Validator Monitoring Tool**

## **Overview**

The **Polygon Validator Monitoring Tool** is a containerized solution designed to monitor the performance of a Polygon Validator node. It performs the following key tasks:

- **Tracking checkpoints** signed and proposed by the validator.
- **Monitoring Bor and Heimdall block heights** to ensure they are increasing and in sync.
- **Sending alerts** via a Telegram chat if any issues are detected, such as missed checkpoints or unsynced block heights.

The tool is fully containerized using Docker, making it easy to deploy locally or on a cloud server.

## **Features**

- **Checkpoint Tracking**: Monitors checkpoints signed and proposed by the configured validator.
- **Block Height Monitoring**: Tracks Bor and Heimdall block heights to ensure they are increasing and in sync.
- **Alerting**: Sends alerts via Telegram if any monitoring issues are detected (e.g., missed checkpoints, unsynced block heights).
- **Containerized**: Easily deployable via Docker for consistent performance across environments.

## **Prerequisites**

Before using this tool, ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/).
- **Python 3.x** (if running locally without Docker).
- **Telegram Bot**: Set up a Telegram bot (instructions below) to receive alerts.
- **Polygon Validator Address**: The address of the validator node you want to monitor.

## **Getting Started**

### 1. **Clone the Repository**

Clone the repository to your local machine:

```
git clone <your-repository-url>
cd <your-repository-directory>
```

### 2. Create and Configure a Telegram Bot

1. **Open Telegram and Search for BotFather**
   - Start a chat with `BotFather` by typing `/start`.
   - To create a new bot, type `/newbot` and follow the prompts.
   - Set a name and a username (which must end with 'bot', e.g., `MyValidatorMonitorBot`) for your bot.
   - Save the bot token provided by BotFather for later use.

2. **Add the Bot to a Group or Channel**
   - Open the Telegram group or channel where you want to receive alerts.
   - Add your bot as a member.

3. **Retrieve the Chat ID**
   - Send any message to the group or channel.
   - Replace `<YourBotToken>` with the bot token you received from BotFather and visit the following URL:
     ```
     https://api.telegram.org/bot<YourBotToken>/getUpdates
     ```
   - Look for `"chat":{"id":-123456789}` in the response to find your chat ID.

### 3. Configure `config.yaml`

Edit the `config.yaml` file with the following configurations:

```yaml
validator_address: "0xYourValidatorAddress"  # Replace with your validator's address
rpc_endpoint: "https://polygon-rpc.com/"     # Replace with the correct Polygon RPC endpoint
telegram_chat_id: "-123456789"               # Replace with your Telegram Chat ID
telegram_bot_token: "123456789:YourBotToken" # Replace with your Telegram bot token
```
### Deployment

#### Option 1: Running with Docker

1. **Build the Docker Image**
   - Open a terminal on your machine where Docker is installed.
   - Run the following command to build the Docker image for the monitoring tool:
     ```bash
     docker build -t polygon-validator-monitor .
     ```

2. **Run the Docker Container**
   - Continue in the terminal and start the Docker container using the command:
     ```bash
     docker run -d --name validator-monitor polygon-validator-monitor
     ```

3. **Check Logs**
   - To verify that the application is running correctly and monitoring as expected, check the logs using:
     ```bash
     docker logs validator-monitor
     ```

This deployment process using Docker ensures that your monitoring tool is set up in a contained environment, which can be consistently replicated across any machine with Docker installed, minimizing environment-related discrepancies.

