# Automated ML Platform

A web-based machine learning platform that allows users to upload datasets, configure models, and download trained models for later use.

## Features

- **Dataset Upload**: Upload CSV and Excel files
- **Model Configuration**: Support for Classification, Regression, and Clustering models
- **Target Column Selection**: Select and configure the target variable
- **Data Preview**: View uploaded dataset with interactive table
- **Model Metrics**: Real-time model evaluation metrics including:
  - Confusion Matrix (for classification)
  - ROC Curve
  - Feature Importance
  - Classification Report
- **Model Download**: Download trained models and preprocessing pipelines as `.joblib` files

## Project Structure

```
├── backend/
│   ├── main.py                 # Flask API server
│   ├── requirements.txt         # Python dependencies
│   └── ml/
│       ├── models.py           # Model training logic
│       ├── preprocessing.py    # Data preprocessing pipeline
│       ├── training.py         # Training orchestration
│       └── evaluation.py       # Model evaluation utilities
├── frontend/
│   └── data_engineering/
│       ├── package.json
│       ├── src/
│       │   ├── App.js          # Main React component
│       │   ├── components/     # React components
│       │   │   ├── SaveModelButton.jsx    # Download model component
│       │   │   ├── ModelSelection.jsx
│       │   │   ├── TargetColumnSelection.jsx
│       │   │   └── ...
│       │   └── index.js
│       ├── public/
│       └── build/
└── README.md
```

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## Installation & Setup

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend/data_engineering

# Install dependencies
npm install
```

## Running the Application

### Start Backend Server

```bash
cd backend

# Activate virtual environment (if not already active)
source venv/bin/activate

# Run Flask server
python main.py
```

The backend will start on `http://localhost:5000`

### Start Frontend Development Server

```bash
cd frontend/data_engineering

# Start React development server
npm start
```

The frontend will start on `http://localhost:3000`

## API Endpoints

### Train Model

**Endpoint:** `POST /api/train`

**Request Body:**
```json
{
  "model_type": "classification|regression|clustering",
  "target_column": "column_name",
  "data": [[row1...], [row2...], ...],
  "headers": ["col1", "col2", ...]
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "model_1",
  "metrics": {
    "confusion_matrix": [...],
    "classification_report": {...},
    "feature_importance": [...],
    "accuracy": 0.89
  }
}
```

### Download Model

**Endpoint:** `GET /api/download-model/<session_id>`

**Response:** Binary file (.joblib format) containing:
- Trained model
- Preprocessing pipeline
- Feature names
- Model type
- Target column name

### List Available Models

**Endpoint:** `GET /api/models`

**Response:**
```json
[
  {
    "session_id": "model_1",
    "model_type": "classification",
    "target_column": "target"
  }
]
```

### Health Check

**Endpoint:** `GET /health`

**Response:** `{"status": "ok"}`

## Using Downloaded Models

To load and use a previously downloaded model:

```python
import joblib

# Load the model package
model_package = joblib.load('trained_model_classification_model_1.joblib')

# Extract components
model = model_package['model']
preprocessor = model_package['preprocessor']
feature_names = model_package['feature_names']
model_type = model_package['model_type']

# Prepare new data
new_data = [[...]]  # Your new data
X_processed = preprocessor.transform(new_data, feature_names)

# Make predictions
predictions = model.predict(X_processed)
```

## Supported Models

### Classification
- Random Forest Classifier (100 estimators)
- Metrics: Accuracy, Precision, Recall, F1-Score, ROC-AUC

### Regression
- Random Forest Regressor (100 estimators)
- Metrics: MSE, RMSE, R² Score

### Clustering
- K-Means (3 clusters)
- Metrics: Inertia, Cluster Sizes

## Features

### Data Preprocessing
- Automatic handling of categorical variables (LabelEncoder)
- Missing value imputation
- Feature scaling (StandardScaler)

### Model Evaluation
- Confusion matrices
- Classification reports
- Feature importance scores
- ROC curves

### Download & Persistence
- Models saved as joblib files for easy transport
- Preprocessing pipeline included for consistent predictions
- Perfect for model deployment and sharing

## File Upload Support

- CSV files (.csv)
- Excel files (.xlsx, .xls)
- TSV files (.tsv)

## Troubleshooting

### CORS Errors
If you see CORS errors in the browser console, ensure that both frontend and backend are running and accessible.

### Model Not Found
Make sure to train a model on the "Dataset & Model" page before attempting to download. The session ID is created when training is initiated.

### Import Errors (Backend)
Verify all dependencies are installed:
```bash
pip install -r backend/requirements.txt
```

## Future Enhancements

- [ ] Model version history
- [ ] Batch predictions
- [ ] Model comparison tools
- [ ] Advanced hyperparameter tuning
- [ ] Real-time model monitoring
- [ ] Database persistence for models
- [ ] User authentication

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
