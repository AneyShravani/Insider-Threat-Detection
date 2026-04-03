#!/usr/bin/env python3
"""
Data Loader for Insider Threat Detection Dataset
================================================

This script provides utilities for loading and preprocessing the insider threat
detection dataset for machine learning applications.

Author: Research Team
Date: 2024
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class InsiderThreatDataLoader:
    """
    A class to load and preprocess insider threat detection datasets.
    """
    
    def __init__(self, data_dir='.'):
        """
        Initialize the data loader.
        
        Args:
            data_dir (str): Directory containing the dataset files
        """
        self.data_dir = data_dir
        self.ueba_data = None
        self.network_logs = None
        self.pam_data = None
        self.dlp_events = None
        self.threat_scenarios = None
        self.malware_indicators = None
        
    def load_all_datasets(self):
        """
        Load all dataset files.
        
        Returns:
            dict: Dictionary containing all loaded datasets
        """
        try:
            print("Loading UEBA data...")
            self.ueba_data = pd.read_csv(f'{self.data_dir}/ueba_data.csv')
            
            print("Loading network logs...")
            self.network_logs = pd.read_csv(f'{self.data_dir}/network_logs.csv')
            
            print("Loading PAM data...")
            self.pam_data = pd.read_csv(f'{self.data_dir}/pam_data.csv')
            
            print("Loading DLP events...")
            self.dlp_events = pd.read_csv(f'{self.data_dir}/dlp_events.csv')
            
            print("Loading threat scenarios...")
            self.threat_scenarios = pd.read_csv(f'{self.data_dir}/insider_threat_scenarios.csv')
            
            print("Loading malware indicators...")
            self.malware_indicators = pd.read_csv(f'{self.data_dir}/malware_indicators.csv')
            
            print("All datasets loaded successfully!")
            
            return {
                'ueba': self.ueba_data,
                'network': self.network_logs,
                'pam': self.pam_data,
                'dlp': self.dlp_events,
                'scenarios': self.threat_scenarios,
                'malware': self.malware_indicators
            }
            
        except FileNotFoundError as e:
            print(f"Error: Could not find dataset file - {e}")
            return None
        except Exception as e:
            print(f"Error loading datasets: {e}")
            return None
    
    def preprocess_ueba_data(self):
        """
        Preprocess UEBA data for machine learning.
        
        Returns:
            pd.DataFrame: Preprocessed UEBA data
        """
        if self.ueba_data is None:
            print("UEBA data not loaded. Please load datasets first.")
            return None
            
        df = self.ueba_data.copy()
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['login_time'] = pd.to_datetime(df['login_time'])
        df['logout_time'] = pd.to_datetime(df['logout_time'])
        
        # Create time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_after_hours'] = ((df['hour'] < 8) | (df['hour'] > 18)).astype(int)
        
        # Create activity frequency features
        activity_counts = df.groupby('user_id')['activity_type'].count().reset_index()
        activity_counts.columns = ['user_id', 'total_activities']
        df = df.merge(activity_counts, on='user_id', how='left')
        
        # Create risk score features
        risk_features = df.groupby('user_id').agg({
            'risk_score': ['mean', 'max', 'sum', 'std']
        }).reset_index()
        risk_features.columns = ['user_id', 'avg_risk', 'max_risk', 'total_risk', 'risk_std']
        df = df.merge(risk_features, on='user_id', how='left')
        
        # Encode categorical variables
        df['activity_type_encoded'] = pd.Categorical(df['activity_type']).codes
        df['data_type_encoded'] = pd.Categorical(df['data_type']).codes
        df['application_encoded'] = pd.Categorical(df['application_used']).codes
        
        return df
    
    def preprocess_network_logs(self):
        """
        Preprocess network logs for machine learning.
        
        Returns:
            pd.DataFrame: Preprocessed network logs
        """
        if self.network_logs is None:
            print("Network logs not loaded. Please load datasets first.")
            return None
            
        df = self.network_logs.copy()
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        
        # Create network traffic features
        df['bytes_per_second'] = df['bytes_transferred'] / df['connection_duration']
        df['is_external'] = ~df['destination_ip'].str.startswith('192.168.')
        df['is_external'] = df['is_external'].astype(int)
        
        # Encode categorical variables
        df['protocol_encoded'] = pd.Categorical(df['protocol']).codes
        df['event_type_encoded'] = pd.Categorical(df['event_type']).codes
        df['threat_category_encoded'] = pd.Categorical(df['threat_category']).codes
        
        # Create user-based features
        user_traffic = df.groupby('user_id').agg({
            'bytes_transferred': ['sum', 'mean', 'max'],
            'connection_duration': ['sum', 'mean'],
            'is_external': 'sum'
        }).reset_index()
        
        user_traffic.columns = ['user_id', 'total_bytes', 'avg_bytes', 'max_bytes', 
                               'total_duration', 'avg_duration', 'external_connections']
        df = df.merge(user_traffic, on='user_id', how='left')
        
        return df
    
    def create_alert_features(self):
        """
        Create features for alert prioritization.
        
        Returns:
            pd.DataFrame: Features for alert prioritization
        """
        if any([self.ueba_data is None, self.network_logs is None, 
                self.pam_data is None, self.dlp_events is None]):
            print("Some datasets not loaded. Please load all datasets first.")
            return None
        
        # Merge all datasets by user_id and timestamp
        ueba_processed = self.preprocess_ueba_data()
        network_processed = self.preprocess_network_logs()
        
        # Create alert features
        alert_features = []
        
        for _, scenario in self.threat_scenarios.iterrows():
            user_id = scenario['user_id']
            detection_time = pd.to_datetime(scenario['detection_time'])
            
            # Get user activities in the last 24 hours
            time_window = detection_time - timedelta(hours=24)
            
            # UEBA features
            user_ueba = ueba_processed[
                (ueba_processed['user_id'] == user_id) & 
                (ueba_processed['timestamp'] >= time_window) &
                (ueba_processed['timestamp'] <= detection_time)
            ]
            
            # Network features
            user_network = network_processed[
                (network_processed['user_id'] == user_id) & 
                (network_processed['timestamp'] >= time_window) &
                (network_processed['timestamp'] <= detection_time)
            ]
            
            # PAM features
            user_pam = self.pam_data[
                (self.pam_data['user_id'] == user_id) & 
                (pd.to_datetime(self.pam_data['timestamp']) >= time_window) &
                (pd.to_datetime(self.pam_data['timestamp']) <= detection_time)
            ]
            
            # DLP features
            user_dlp = self.dlp_events[
                (self.dlp_events['user_id'] == user_id) & 
                (pd.to_datetime(self.dlp_events['timestamp']) >= time_window) &
                (pd.to_datetime(self.dlp_events['timestamp']) <= detection_time)
            ]
            
            # Create feature vector
            features = {
                'scenario_id': scenario['scenario_id'],
                'user_id': user_id,
                'threat_type': scenario['threat_type'],
                'severity': scenario['severity'],
                'risk_score': scenario['risk_score'],
                'false_positive': scenario['false_positive'],
                
                # UEBA features
                'ueba_activity_count': len(user_ueba),
                'ueba_avg_risk': user_ueba['risk_score'].mean() if len(user_ueba) > 0 else 0,
                'ueba_max_risk': user_ueba['risk_score'].max() if len(user_ueba) > 0 else 0,
                'ueba_high_risk_activities': len(user_ueba[user_ueba['risk_score'] > 0.7]),
                
                # Network features
                'network_connections': len(user_network),
                'network_total_bytes': user_network['bytes_transferred'].sum() if len(user_network) > 0 else 0,
                'network_external_connections': user_network['is_external'].sum() if len(user_network) > 0 else 0,
                'network_high_severity': len(user_network[user_network['severity'] == 'high']),
                
                # PAM features
                'pam_privileged_actions': len(user_pam),
                'pam_high_risk_actions': len(user_pam[user_pam['risk_level'] == 'high']),
                'pam_privilege_escalation': user_pam['privilege_escalation'].sum() if len(user_pam) > 0 else 0,
                
                # DLP features
                'dlp_violations': len(user_dlp),
                'dlp_high_risk_violations': len(user_dlp[user_dlp['risk_level'] == 'high']),
                'dlp_blocked_attempts': len(user_dlp[user_dlp['blocked_status'] == 'blocked']),
                
                # Target variables
                'escalation_required': 1 if scenario['escalation_path'] in ['immediate_escalation'] else 0,
                'financial_impact': scenario['financial_impact']
            }
            
            alert_features.append(features)
        
        return pd.DataFrame(alert_features)
    
    def get_dataset_summary(self):
        """
        Get a summary of all datasets.
        
        Returns:
            dict: Summary statistics for all datasets
        """
        summary = {}
        
        if self.ueba_data is not None:
            summary['ueba'] = {
                'rows': len(self.ueba_data),
                'columns': len(self.ueba_data.columns),
                'unique_users': self.ueba_data['user_id'].nunique(),
                'date_range': f"{self.ueba_data['timestamp'].min()} to {self.ueba_data['timestamp'].max()}"
            }
        
        if self.network_logs is not None:
            summary['network'] = {
                'rows': len(self.network_logs),
                'columns': len(self.network_logs.columns),
                'unique_users': self.network_logs['user_id'].nunique(),
                'unique_ips': self.network_logs['source_ip'].nunique()
            }
        
        if self.pam_data is not None:
            summary['pam'] = {
                'rows': len(self.pam_data),
                'columns': len(self.pam_data.columns),
                'unique_users': self.pam_data['user_id'].nunique(),
                'high_risk_actions': len(self.pam_data[self.pam_data['risk_level'] == 'high'])
            }
        
        if self.dlp_events is not None:
            summary['dlp'] = {
                'rows': len(self.dlp_events),
                'columns': len(self.dlp_events.columns),
                'unique_users': self.dlp_events['user_id'].nunique(),
                'blocked_events': len(self.dlp_events[self.dlp_events['blocked_status'] == 'blocked'])
            }
        
        if self.threat_scenarios is not None:
            summary['scenarios'] = {
                'rows': len(self.threat_scenarios),
                'columns': len(self.threat_scenarios.columns),
                'high_severity': len(self.threat_scenarios[self.threat_scenarios['severity'] == 'high']),
                'false_positives': len(self.threat_scenarios[self.threat_scenarios['false_positive'] == True])
            }
        
        if self.malware_indicators is not None:
            summary['malware'] = {
                'rows': len(self.malware_indicators),
                'columns': len(self.malware_indicators.columns),
                'high_impact': len(self.malware_indicators[self.malware_indicators['system_impact'] == 'high']),
                'avg_confidence': self.malware_indicators['confidence_score'].mean()
            }
        
        return summary

def main():
    """
    Main function to demonstrate dataset loading and preprocessing.
    """
    print("Insider Threat Detection Dataset Loader")
    print("=" * 50)
    
    # Initialize data loader
    loader = InsiderThreatDataLoader()
    
    # Load all datasets
    datasets = loader.load_all_datasets()
    
    if datasets is None:
        print("Failed to load datasets. Please check file paths.")
        return
    
    # Get dataset summary
    summary = loader.get_dataset_summary()
    print("\nDataset Summary:")
    print("-" * 30)
    for dataset_name, stats in summary.items():
        print(f"\n{dataset_name.upper()} Dataset:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    # Create alert features
    print("\nCreating alert features...")
    alert_features = loader.create_alert_features()
    
    if alert_features is not None:
        print(f"Alert features shape: {alert_features.shape}")
        print(f"High severity alerts: {len(alert_features[alert_features['severity'] == 'high'])}")
        print(f"Escalation required: {alert_features['escalation_required'].sum()}")
        
        # Save processed data
        alert_features.to_csv('alert_features.csv', index=False)
        print("Alert features saved to 'alert_features.csv'")
    
    print("\nDataset loading and preprocessing completed!")

if __name__ == "__main__":
    main()
