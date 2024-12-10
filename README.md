# Crypto Accountant Script

## Overview

This Python script helps crypto accountants manage data efficiently. The primary functionality is a script that retrieves and classes all the transactions given a wallet address in the Starknet blockchain.

---

## Prerequisites

1. **Python Version**  
   Ensure you have Python 3.8 or later installed.  
   You can check your Python version with:

   ```bash
   python --version
   ```

2. **API Key**  
   You’ll need a `PROJECT_ID` associated with your [BlastAPI](https://blastapi.io/) account.

---

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Install Dependencies**

   [OPTIONAL]
   First create a virtual environment in the cloned repository folder:

   ```bash
   python3 -m venv env
   ```

   Activate the environment:

   For MacOS/Linux

   ```bash
   source env/bin/activate
   ```

   For Windows

   ```bash
   .\env\Scripts\activate
   ```

   Use the `requirements.txt` file to install the necessary packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**

   - A `.env.template` file is provided.
   - Rename it to `.env`:
   - Open the `.env` file in a text editor and replace `<PROJECT_ID>` with your actual project ID from BlastAPI:

     ```plaintext
     PROJECT_ID=<your_project_id>
     ```

   - Add one or multiple wallet addresses in the config.py file (in WALLET_ADDRESSES) to create a .csv file for each of them.

---

## Usage

To use the script, simply run the following command in your terminal:

```bash
python run.py
```

### Example

If your wallet address is `0xabc123...`:
WALLET_ADDRESSES = ["0xabc123..."] in config.py

A CSV file will be generated with all the transactions for the given wallet address.
