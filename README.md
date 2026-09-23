## Running the Project Locally

The large historical stock datasets used during development are not included in this repository due to GitHub file-size limitations. Therefore, to reproduce the complete project locally, the data collection, feature engineering and model training stages must first be executed before running the chatbot.

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Codes
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

> Additional development dependencies may be required for the data collection, model training and optimisation scripts if they are not included in the deployment-focused `requirements.txt`.

### 3. Configure Environment Variables

Create a `.env` file in the project directory:

```env
OPENAI_API_KEY=your_openai_api_key
RAG_VECTOR_STORE_ID=your_vector_store_id
```

The `.env` file is excluded from the repository and should not be committed to GitHub.

### 4. Collect Historical Stock Data

Run the data collection script to download the historical S&P 500 stock data required by the project.

```bash
python YOUR_DATA_COLLECTION_SCRIPT.py
```

The collected data will be stored in the appropriate `data/raw/` directory.

### 5. Perform Feature Engineering

Run the feature engineering pipeline to transform the raw stock data into the financial features required by the LightGBM model.

```bash
python YOUR_FEATURE_ENGINEERING_SCRIPT.py
```

This stage generates features including stock returns, volatility, trend strength, momentum, relative market performance and risk-adjusted momentum.

The resulting machine-learning dataset is stored locally and is not included in GitHub because of its size.

### 6. Train the LightGBM Model

Run the LightGBM training script after the feature-engineered dataset has been generated.

```bash
python YOUR_LIGHTGBM_TRAINING_SCRIPT.py
```

The trained model should be saved as:

```text
model/lgb_model.pkl
```

The project uses a LightGBM regression model to predict five-day future returns. The resulting predictions are subsequently used to rank stocks and generate Buy, Hold and Sell signals.

### 7. Generate the Deployment Dataset

The chatbot does not require the complete historical dataset during normal operation. Generate the smaller deployment dataset containing the latest feature values required by the trained model:

```bash
python create_deployment_data.py
```

This creates:

```text
data/deployment/latest_stock_features.csv
```

### 8. Run the Financial Advisor Bot

Once the trained model and deployment dataset are available, start the Flask application:

```bash
python app.py
```

Open the local address displayed by Flask in a web browser.

The complete reproduction workflow is therefore:

```text
Historical Stock Data
        ↓
Data Collection
        ↓
Feature Engineering
        ↓
Final ML Dataset
        ↓
LightGBM Training
        ↓
Trained Model
        ↓
Latest Deployment Features
        ↓
Flask Financial Advisor Bot
```

### Live Prototype

Users who only wish to evaluate the completed system do not need to reproduce the machine-learning pipeline. A deployed version of the completed Financial Advisor Bot is available at:

**[Open Financial Advisor Bot](https://financial-advisor-bot-bmue.onrender.com/)**