#!/usr/bin/env python3
"""
Advanced Machine Learning Models for Insider Threat Detection
============================================================

This script demonstrates advanced ML models including DNN, RNN, and ensemble
methods for insider threat detection and alert prioritization.

Author: Research Team
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.neural_network import MLPClassifier
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, GRU, Conv1D, MaxPooling1D, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import warnings
warnings.filterwarnings('ignore')

class AdvancedInsiderThreatML:
    """
    Advanced machine learning models for insider threat detection.
    """
    
    def __init__(self):
        """Initialize the ML models."""
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.models = {}
        self.results = {}
        
    def load_and_prepare_data(self):
        """Load and prepare data for machine learning."""
        print("Loading and preparing data for ML...")
        
        # Load datasets
        ueba_data = pd.read_csv('ueba_data.csv')
        network_logs = pd.read_csv('network_logs.csv')
        pam_data = pd.read_csv('pam_data.csv')
        dlp_events = pd.read_csv('dlp_events.csv')
        threat_scenarios = pd.read_csv('insider_threat_scenarios.csv')
        
        # Create comprehensive feature set
        features = []
        
        for _, scenario in threat_scenarios.iterrows():
            user_id = scenario['user_id']
            
            # Get user's data from all sources
            user_ueba = ueba_data[ueba_data['user_id'] == user_id]
            user_network = network_logs[network_logs['user_id'] == user_id]
            user_pam = pam_data[pam_data['user_id'] == user_id]
            user_dlp = dlp_events[dlp_events['user_id'] == user_id]
            
            # Create feature vector
            feature_vector = {
                'scenario_id': scenario['scenario_id'],
                'user_id': user_id,
                
                # UEBA Features
                'ueba_activity_count': len(user_ueba),
                'ueba_avg_risk': user_ueba['risk_score'].mean() if len(user_ueba) > 0 else 0,
                'ueba_max_risk': user_ueba['risk_score'].max() if len(user_ueba) > 0 else 0,
                'ueba_risk_std': user_ueba['risk_score'].std() if len(user_ueba) > 0 else 0,
                'ueba_high_risk_activities': len(user_ueba[user_ueba['risk_score'] > 0.7]),
                
                # Network Features
                'network_connections': len(user_network),
                'network_total_bytes': user_network['bytes_transferred'].sum() if len(user_network) > 0 else 0,
                'network_avg_bytes': user_network['bytes_transferred'].mean() if len(user_network) > 0 else 0,
                'network_external_connections': len(user_network[~user_network['destination_ip'].str.startswith('192.168.')]),
                'network_high_severity': len(user_network[user_network['severity'] == 'high']),
                
                # PAM Features
                'pam_privileged_actions': len(user_pam),
                'pam_high_risk_actions': len(user_pam[user_pam['risk_level'] == 'high']),
                'pam_privilege_escalation': user_pam['privilege_escalation'].sum() if len(user_pam) > 0 else 0,
                'pam_avg_session_duration': user_pam['session_duration'].mean() if len(user_pam) > 0 else 0,
                
                # DLP Features
                'dlp_violations': len(user_dlp),
                'dlp_high_risk_violations': len(user_dlp[user_dlp['risk_level'] == 'high']),
                'dlp_blocked_attempts': len(user_dlp[user_dlp['blocked_status'] == 'blocked']),
                'dlp_total_file_size': user_dlp['file_size'].sum() if len(user_dlp) > 0 else 0,
                
                # Target Variables
                'threat_severity': 1 if scenario['severity'] == 'high' else (0.5 if scenario['severity'] == 'medium' else 0),
                'risk_score': scenario['risk_score'],
                'financial_impact': scenario['financial_impact'],
                'escalation_required': 1 if scenario['escalation_path'] == 'immediate_escalation' else 0,
                'is_threat': 1 if scenario['severity'] in ['high', 'medium'] else 0
            }
            features.append(feature_vector)
        
        self.data = pd.DataFrame(features)
        print(f"✓ Prepared dataset with {len(self.data)} samples and {len(self.data.columns)} features")
        
        return self.data
    
    def prepare_ml_data(self, target_column='is_threat'):
        """Prepare data for machine learning."""
        print(f"\nPreparing data for ML with target: {target_column}")
        
        # Select features and target
        feature_columns = [col for col in self.data.columns if col not in [
            'scenario_id', 'user_id', 'threat_severity', 'risk_score', 
            'financial_impact', 'escalation_required', 'is_threat'
        ]]
        
        X = self.data[feature_columns]
        y = self.data[target_column]
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"✓ Training set: {self.X_train.shape[0]} samples")
        print(f"✓ Test set: {self.X_test.shape[0]} samples")
        print(f"✓ Features: {self.X_train.shape[1]}")
        
        return self.X_train_scaled, self.X_test_scaled, self.y_train, self.y_test
    
    def train_traditional_models(self):
        """Train traditional machine learning models."""
        print("\nTraining traditional ML models...")
        
        # Random Forest
        print("Training Random Forest...")
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        rf_model.fit(self.X_train_scaled, self.y_train)
        self.models['Random Forest'] = rf_model
        
        # Gradient Boosting
        print("Training Gradient Boosting...")
        gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        gb_model.fit(self.X_train_scaled, self.y_train)
        self.models['Gradient Boosting'] = gb_model
        
        # Neural Network (sklearn)
        print("Training Neural Network (sklearn)...")
        nn_model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        nn_model.fit(self.X_train_scaled, self.y_train)
        self.models['Neural Network (sklearn)'] = nn_model
        
        print("✓ Traditional models trained successfully!")
    
    def build_dnn_model(self):
        """Build and train Deep Neural Network."""
        print("\nBuilding Deep Neural Network...")
        
        # Reshape data for DNN
        X_train_dnn = self.X_train_scaled.reshape((self.X_train_scaled.shape[0], self.X_train_scaled.shape[1], 1))
        X_test_dnn = self.X_test_scaled.reshape((self.X_test_scaled.shape[0], self.X_test_scaled.shape[1], 1))
        
        # Build DNN model
        dnn_model = Sequential([
            Conv1D(64, 3, activation='relu', input_shape=(X_train_dnn.shape[1], 1)),
            MaxPooling1D(2),
            Conv1D(32, 3, activation='relu'),
            MaxPooling1D(2),
            Flatten(),
            Dense(100, activation='relu'),
            Dropout(0.3),
            Dense(50, activation='relu'),
            Dropout(0.3),
            Dense(1, activation='sigmoid')
        ])
        
        dnn_model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # Train DNN
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        
        history = dnn_model.fit(
            X_train_dnn, self.y_train,
            epochs=100,
            batch_size=32,
            validation_split=0.2,
            callbacks=[early_stopping],
            verbose=0
        )
        
        self.models['Deep Neural Network'] = dnn_model
        self.dnn_history = history
        
        print("✓ Deep Neural Network trained successfully!")
        
        return dnn_model, history
    
    def build_rnn_model(self):
        """Build and train Recurrent Neural Network."""
        print("\nBuilding Recurrent Neural Network...")
        
        # Reshape data for RNN
        X_train_rnn = self.X_train_scaled.reshape((self.X_train_scaled.shape[0], self.X_train_scaled.shape[1], 1))
        X_test_rnn = self.X_test_scaled.reshape((self.X_test_scaled.shape[0], self.X_test_scaled.shape[1], 1))
        
        # Build RNN model
        rnn_model = Sequential([
            LSTM(64, return_sequences=True, input_shape=(X_train_rnn.shape[1], 1)),
            Dropout(0.2),
            LSTM(32, return_sequences=False),
            Dropout(0.2),
            Dense(50, activation='relu'),
            Dropout(0.3),
            Dense(1, activation='sigmoid')
        ])
        
        rnn_model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # Train RNN
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        
        history = rnn_model.fit(
            X_train_rnn, self.y_train,
            epochs=100,
            batch_size=32,
            validation_split=0.2,
            callbacks=[early_stopping],
            verbose=0
        )
        
        self.models['Recurrent Neural Network'] = rnn_model
        self.rnn_history = history
        
        print("✓ Recurrent Neural Network trained successfully!")
        
        return rnn_model, history
    
    def evaluate_models(self):
        """Evaluate all trained models."""
        print("\nEvaluating models...")
        
        for name, model in self.models.items():
            print(f"\nEvaluating {name}...")
            
            if 'Neural Network' in name and 'sklearn' not in name:
                # TensorFlow models
                X_test_reshaped = self.X_test_scaled.reshape((self.X_test_scaled.shape[0], self.X_test_scaled.shape[1], 1))
                y_pred_proba = model.predict(X_test_reshaped)
                y_pred = (y_pred_proba > 0.5).astype(int)
            else:
                # sklearn models
                y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
                y_pred = model.predict(self.X_test_scaled)
            
            # Calculate metrics
            accuracy = (y_pred == self.y_test).mean()
            auc_score = roc_auc_score(self.y_test, y_pred_proba)
            
            self.results[name] = {
                'accuracy': accuracy,
                'auc_score': auc_score,
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba
            }
            
            print(f"  Accuracy: {accuracy:.4f}")
            print(f"  AUC Score: {auc_score:.4f}")
    
    def create_comprehensive_plots(self):
        """Create comprehensive visualization of results."""
        print("\nCreating comprehensive visualizations...")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 16))
        
        # 1. Model Performance Comparison
        plt.subplot(3, 3, 1)
        model_names = list(self.results.keys())
        accuracies = [self.results[name]['accuracy'] for name in model_names]
        auc_scores = [self.results[name]['auc_score'] for name in model_names]
        
        x = np.arange(len(model_names))
        width = 0.35
        
        plt.bar(x - width/2, accuracies, width, label='Accuracy', alpha=0.8)
        plt.bar(x + width/2, auc_scores, width, label='AUC Score', alpha=0.8)
        plt.xlabel('Models')
        plt.ylabel('Score')
        plt.title('Model Performance Comparison')
        plt.xticks(x, model_names, rotation=45)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 2. ROC Curves
        plt.subplot(3, 3, 2)
        for name, result in self.results.items():
            fpr, tpr, _ = roc_curve(self.y_test, result['y_pred_proba'])
            plt.plot(fpr, tpr, label=f'{name} (AUC = {result["auc_score"]:.3f})')
        
        plt.plot([0, 1], [0, 1], 'k--', alpha=0.5)
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 3. Confusion Matrix (Best Model)
        plt.subplot(3, 3, 3)
        best_model = max(self.results.keys(), key=lambda x: self.results[x]['auc_score'])
        cm = confusion_matrix(self.y_test, self.results[best_model]['y_pred'])
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {best_model}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        # 4. Feature Importance (Random Forest)
        plt.subplot(3, 3, 4)
        if 'Random Forest' in self.models:
            rf_model = self.models['Random Forest']
            feature_importance = pd.DataFrame({
                'feature': self.X_train.columns,
                'importance': rf_model.feature_importances_
            }).sort_values('importance', ascending=False).head(10)
            
            plt.barh(range(len(feature_importance)), feature_importance['importance'])
            plt.yticks(range(len(feature_importance)), feature_importance['feature'])
            plt.xlabel('Feature Importance')
            plt.title('Top 10 Feature Importance (Random Forest)')
        
        # 5. DNN Training History
        plt.subplot(3, 3, 5)
        if hasattr(self, 'dnn_history'):
            plt.plot(self.dnn_history.history['accuracy'], label='Training Accuracy')
            plt.plot(self.dnn_history.history['val_accuracy'], label='Validation Accuracy')
            plt.xlabel('Epoch')
            plt.ylabel('Accuracy')
            plt.title('DNN Training History')
            plt.legend()
            plt.grid(True, alpha=0.3)
        
        # 6. RNN Training History
        plt.subplot(3, 3, 6)
        if hasattr(self, 'rnn_history'):
            plt.plot(self.rnn_history.history['accuracy'], label='Training Accuracy')
            plt.plot(self.rnn_history.history['val_accuracy'], label='Validation Accuracy')
            plt.xlabel('Epoch')
            plt.ylabel('Accuracy')
            plt.title('RNN Training History')
            plt.legend()
            plt.grid(True, alpha=0.3)
        
        # 7. Prediction Distribution
        plt.subplot(3, 3, 7)
        for name, result in self.results.items():
            plt.hist(result['y_pred_proba'], alpha=0.5, label=name, bins=20)
        plt.xlabel('Predicted Probability')
        plt.ylabel('Frequency')
        plt.title('Prediction Probability Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 8. Model Comparison Table
        plt.subplot(3, 3, 8)
        plt.axis('off')
        comparison_data = []
        for name, result in self.results.items():
            comparison_data.append([name, f"{result['accuracy']:.4f}", f"{result['auc_score']:.4f}"])
        
        table = plt.table(cellText=comparison_data,
                         colLabels=['Model', 'Accuracy', 'AUC Score'],
                         cellLoc='center',
                         loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        plt.title('Model Performance Summary')
        
        # 9. Data Distribution
        plt.subplot(3, 3, 9)
        plt.pie([(self.y_train == 0).sum(), (self.y_train == 1).sum()],
                labels=['No Threat', 'Threat'],
                autopct='%1.1f%%',
                colors=['lightblue', 'lightcoral'])
        plt.title('Target Variable Distribution')
        
        plt.tight_layout()
        plt.savefig('advanced_ml_results.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✓ Advanced ML results saved as 'advanced_ml_results.png'")
    
    def generate_ml_report(self):
        """Generate comprehensive ML report."""
        print("\nGenerating ML report...")
        
        report = []
        report.append("=" * 60)
        report.append("ADVANCED MACHINE LEARNING ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Dataset Information
        report.append("DATASET INFORMATION:")
        report.append("-" * 20)
        report.append(f"Total Samples: {len(self.data)}")
        report.append(f"Training Samples: {len(self.X_train)}")
        report.append(f"Test Samples: {len(self.X_test)}")
        report.append(f"Features: {self.X_train.shape[1]}")
        report.append(f"Positive Class Ratio: {(self.y_train == 1).mean():.2%}")
        report.append("")
        
        # Model Performance
        report.append("MODEL PERFORMANCE:")
        report.append("-" * 20)
        for name, result in self.results.items():
            report.append(f"{name}:")
            report.append(f"  Accuracy: {result['accuracy']:.4f}")
            report.append(f"  AUC Score: {result['auc_score']:.4f}")
            report.append("")
        
        # Best Model
        best_model = max(self.results.keys(), key=lambda x: self.results[x]['auc_score'])
        report.append(f"BEST PERFORMING MODEL: {best_model}")
        report.append(f"Best AUC Score: {self.results[best_model]['auc_score']:.4f}")
        report.append("")
        
        # Feature Analysis
        if 'Random Forest' in self.models:
            report.append("TOP 5 MOST IMPORTANT FEATURES:")
            report.append("-" * 20)
            rf_model = self.models['Random Forest']
            feature_importance = pd.DataFrame({
                'feature': self.X_train.columns,
                'importance': rf_model.feature_importances_
            }).sort_values('importance', ascending=False).head(5)
            
            for _, row in feature_importance.iterrows():
                report.append(f"  {row['feature']}: {row['importance']:.4f}")
        
        # Save report
        with open('ml_analysis_report.txt', 'w') as f:
            f.write('\n'.join(report))
        
        print("✓ ML report saved as 'ml_analysis_report.txt'")
        print('\n'.join(report))
    
    def run_complete_ml_analysis(self):
        """Run complete machine learning analysis."""
        print("🚀 Starting Advanced Machine Learning Analysis")
        print("=" * 60)
        
        # Load and prepare data
        self.load_and_prepare_data()
        self.prepare_ml_data()
        
        # Train models
        self.train_traditional_models()
        self.build_dnn_model()
        self.build_rnn_model()
        
        # Evaluate models
        self.evaluate_models()
        
        # Create visualizations
        self.create_comprehensive_plots()
        self.generate_ml_report()
        
        print("\n" + "=" * 60)
        print("✅ ADVANCED ML ANALYSIS COMPLETED!")
        print("=" * 60)
        print("\nGenerated Files:")
        print("• advanced_ml_results.png - Comprehensive ML visualizations")
        print("• ml_analysis_report.txt - Detailed ML performance report")

def main():
    """Main function to run the advanced ML analysis."""
    ml_analyzer = AdvancedInsiderThreatML()
    ml_analyzer.run_complete_ml_analysis()

if __name__ == "__main__":
    main()
