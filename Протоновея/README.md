# NOVEYA: The FDL-Context Navigator
> *Powered by Amazon Nova Act & AWS Bedrock*

**NOVEYA** is an intelligent agentic system that filters digital information through **Formal-Dialectical Logic (FDL)**. It helps users navigate the web by autonomously resolving contradictions in news and data, providing a "Synthesized Brief" of reality.

---

## 🏗 Architecture

The system operates on a **Thesis-Antithesis-Synthesis** cycle:

1.  **Thesis (Input):** The user defines a topic or browses a URL.
2.  **Antithesis (The Nova Agent):** **Amazon Nova Act** scans the content, identifying logical fallacies, emotional noise, and structural contradictions.
3.  **Synthesis (Resolution):** The system applies the **"Cathedral of Twelve Theses"** protocol (via Amazon Nova Pro) to generate a harmonized summary—clean, neutral, and structurally sound.

## 🛠 Tech Stack

* **Core AI:** Amazon Nova Pro (Reasoning), Amazon Nova Act (Navigation).
* **Infrastructure:** AWS Bedrock, AWS Lambda.
* **Logic Kernel:** Python (FDL Algorithms).
* **Integration:** Boto3 SDK.

## 🚀 Installation & Setup

### Prerequisites
* Python 3.9+
* AWS Account with Bedrock Access enabled (specifically for Nova models).

### Steps
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/NOVEYA-FDL-Navigator.git](https://github.com/YOUR_USERNAME/NOVEYA-FDL-Navigator.git)
    cd NOVEYA-FDL-Navigator
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure AWS Credentials:**
    Ensure your `~/.aws/credentials` file is set up, or export environment variables:
    ```bash
    export AWS_ACCESS_KEY_ID="YOUR_KEY"
    export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
    export AWS_DEFAULT_REGION="us-east-1"
    ```

4.  **Run the FDL Agent:**
    ```bash
    python nova_fdl_agent.py
    ```

## 🧩 Key Components

* `nova_fdl_agent.py`: The main entry point for the Amazon Nova integration.
* `fdl_prompts.py`: Contains the **"Cathedral of Twelve Theses"** system prompts.
* `config.py`: Configuration for AWS Bedrock model IDs and temperature settings.

## ⚖️ The FDL Protocol
This project is strictly governed by the **Formal-Dialectical Logic** framework. It does not generate arbitrary content; it *restructures* existing content to remove entropy (chaos).

---
*Submitted for the Amazon Nova AI Hackathon 2026.*
