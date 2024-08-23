
# TapMonster AutoBot

### 🚀 **Support the Project!**

If you find this project helpful, consider supporting me by using my referral link for the TapMonsters app. Your support helps me continue working on projects like this!

👉 **[Use my referral link to get started!](https://t.me/tapmonsters_bot/start?startapp=ref1956860053&startApp=ref1956860053)
 or else
 [Join my clan](https://t.me/tapmonsters_bot/start?startapp=ref1956860053-clanAKCJ7&startApp=ref1956860053-clanAKCJ7)**👈
Thank you for your support! 🙌
**************************************

A Python tool for managing and automating operations through the TapMonster API. This application includes features to perform taps, purchase upgrades, and manage configurations automatically.

![Project Banner](resources/banner.jpg)

## Table of Contents

1. [Description](#description)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Contributing](#contributing)
8. [License](#license)
9. [Contact](#contact)

## Description

TapMonster AutoBot is designed to automate interactions with the TapMonster API, allowing for the execution of actions such as taps, purchasing upgrades, and managing configurations. The script operates based on configurable parameters and includes colorful console logging for better visibility.

## Features

- Retrieve user data from the TapMonster API.
- Execute taps with random configurations.
- Purchase the most cost-effective upgrades based on analysis.
- Flexible configuration through a JSON file.
- Command-line interface with colorful and informative logs.

## Requirements

Ensure you have the following dependencies installed:

- Python 3.6 or higher
- [requests](https://pypi.org/project/requests/)
- [tqdm](https://pypi.org/project/tqdm/)
- [colorama](https://pypi.org/project/colorama/)

You can install these dependencies using:

```bash
pip install -r requirements.txt
```

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/akumanomi1988/TapMonster_AutoBot.git
    cd TapMonster_AutoBot
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the configuration file:**

    - Copy the `config.example.json` file to `config.json`:

        ```bash
        cp config.example.json config.json
        ```

    - Open `config.json` and add your bearer token and adjust other settings as needed.

## Configuration

The `config.json` file is used to configure the script. It should be copied from `config.example.json` and filled with the appropriate values.

**Example `config.json`:**

```json
{
    "bearer_token": "",
    "min_wait_time": 10,
    "max_wait_time": 30,
    "buy_until_no_more": true
}
```

- **`bearer_token`**: Your API authorization token. Replace the empty string with your actual token.
- **`min_wait_time`**: Minimum wait time in seconds between iterations.
- **`max_wait_time`**: Maximum wait time in seconds between iterations.
- **`buy_until_no_more`**: Boolean to determine if upgrades should be purchased until no more can be bought (`true`) or until no more affordable upgrades are available (`false`).

## Usage

1. **Run the script:**

    ```bash
    python main.py
    ```

2. The script will automatically:

    - Retrieve user data from the API.
    - Execute taps with random amounts until fewer than 100 taps are remaining.
    - Evaluate and purchase the most cost-effective upgrade available based on the configuration.
    - Wait for a random period before repeating the process.
