#!/usr/bin/env python3
"""
Comprehensive Analysis of Insider Threat Detection Dataset
==========================================================

This script provides detailed analysis, visualizations, and machine learning
demonstrations for the insider threat detection dataset.

Author: Research Team
Date: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class InsiderThreatAnalyzer:
    """
    Comprehensive analyzer for insider threat detection dataset.
    """
    
    def __init__(self):
        """Initialize the analyzer."""
        self.ueba_data = None
        self.network_logs = None
        self.pam_data = None
        self.dlp_events = None
        self.threat_scenarios = None
        self.malware_indicators = None
        self.alert_features = None
        
    def load_datasets(self):
        """Load all datasets."""
        print("Loading datasets...")
        
        try:
            self.ueba_data = pd.read_csv('ueba_data.csv')
            self.network_logs = pd.read_csv('network_logs.csv')
            self.pam_data = pd.read_csv('pam_data.csv')
            self.dlp_events = pd.read_csv('dlp_events.csv')
            self.threat_scenarios = pd.read_csv('insider_threat_scenarios.csv')
            self.malware_indicators = pd.read_csv('malware_indicators.csv')
            
            print("✓ All datasets loaded successfully!")
            return True
        except Exception as e:
            print(f"✗ Error loading datasets: {e}")
            return False
    
    def preprocess_data(self):
        """Preprocess all datasets."""
        print("\nPreprocessing data...")
        
        # Convert timestamps
        for df_name in ['ueba_data', 'network_logs', 'pam_data', 'dlp_events']:
            df = getattr(self, df_name)
            if df is not None:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        self.threat_scenarios['detection_time'] = pd.to_datetime(self.threat_scenarios['detection_time'])
        self.malware_indicators['timestamp'] = pd.to_datetime(self.malware_indicators['timestamp'])
        
        print("✓ Data preprocessing completed!")
    
    def create_comprehensive_plots(self):
        """Create comprehensive visualizations."""
        print("\nCreating comprehensive visualizations...")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 24))
        
        # 1. Threat Severity Distribution
        plt.subplot(4, 3, 1)
        severity_counts = self.threat_scenarios['severity'].value_counts()
        colors = ['#ff6b6b', '#ffd93d', '#6bcf7f']
        plt.pie(severity_counts.values, labels=severity_counts.index, autopct='%1.1f%%', colors=colors)
        plt.title('Threat Severity Distribution', fontsize=14, fontweight='bold')
        
        # 2. Risk Score Distribution
        plt.subplot(4, 3, 2)
        plt.hist(self.threat_scenarios['risk_score'], bins=15, alpha=0.7, color='skyblue', edgecolor='black')
        plt.xlabel('Risk Score')
        plt.ylabel('Frequency')
        plt.title('Risk Score Distribution', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # 3. Threat Types
        plt.subplot(4, 3, 3)
        threat_counts = self.threat_scenarios['threat_type'].value_counts().head(10)
        plt.barh(range(len(threat_counts)), threat_counts.values, color='lightcoral')
        plt.yticks(range(len(threat_counts)), threat_counts.index)
        plt.xlabel('Count')
        plt.title('Top 10 Threat Types', fontsize=14, fontweight='bold')
        
        # 4. UEBA Activity Patterns
        plt.subplot(4, 3, 4)
        activity_counts = self.ueba_data['activity_type'].value_counts().head(8)
        plt.bar(range(len(activity_counts)), activity_counts.values, color='lightgreen')
        plt.xticks(range(len(activity_counts)), activity_counts.index, rotation=45)
        plt.ylabel('Count')
        plt.title('UEBA Activity Types', fontsize=14, fontweight='bold')
        
        # 5. Network Protocol Distribution
        plt.subplot(4, 3, 5)
        protocol_counts = self.network_logs['protocol'].value_counts()
        plt.pie(protocol_counts.values, labels=protocol_counts.index, autopct='%1.1f%%')
        plt.title('Network Protocol Distribution', fontsize=14, fontweight='bold')
        
        # 6. DLP Violations by Risk Level
        plt.subplot(4, 3, 6)
        dlp_risk = self.dlp_events['risk_level'].value_counts()
        colors = ['#ff6b6b', '#ffd93d', '#6bcf7f']
        plt.bar(dlp_risk.index, dlp_risk.values, color=colors)
        plt.ylabel('Count')
        plt.title('DLP Violations by Risk Level', fontsize=14, fontweight='bold')
        
        # 7. Malware Impact Analysis
        plt.subplot(4, 3, 7)
        impact_counts = self.malware_indicators['system_impact'].value_counts()
        plt.bar(impact_counts.index, impact_counts.values, color=['#ff6b6b', '#ffd93d', '#6bcf7f'])
        plt.ylabel('Count')
        plt.title('Malware System Impact', fontsize=14, fontweight='bold')
        
        # 8. PAM Risk Levels
        plt.subplot(4, 3, 8)
        pam_risk = self.pam_data['risk_level'].value_counts()
        plt.pie(pam_risk.values, labels=pam_risk.index, autopct='%1.1f%%')
        plt.title('PAM Risk Level Distribution', fontsize=14, fontweight='bold')
        
        # 9. Financial Impact Analysis
        plt.subplot(4, 3, 9)
        financial_impact = self.threat_scenarios['financial_impact'].sort_values(ascending=False).head(10)
        plt.barh(range(len(financial_impact)), financial_impact.values, color='gold')
        plt.yticks(range(len(financial_impact)), [f'Scenario {i+1}' for i in range(len(financial_impact))])
        plt.xlabel('Financial Impact ($)')
        plt.title('Top 10 Financial Impact Scenarios', fontsize=14, fontweight='bold')
        
        # 10. Time-based Analysis
        plt.subplot(4, 3, 10)
        self.threat_scenarios['hour'] = self.threat_scenarios['detection_time'].dt.hour
        hourly_counts = self.threat_scenarios['hour'].value_counts().sort_index()
        plt.plot(hourly_counts.index, hourly_counts.values, marker='o', linewidth=2, markersize=6)
        plt.xlabel('Hour of Day')
        plt.ylabel('Threat Count')
        plt.title('Threat Detection by Hour', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # 11. User Risk Analysis
        plt.subplot(4, 3, 11)
        user_risk = self.ueba_data.groupby('user_id')['risk_score'].mean().sort_values(ascending=False).head(10)
        plt.barh(range(len(user_risk)), user_risk.values, color='lightblue')
        plt.yticks(range(len(user_risk)), user_risk.index)
        plt.xlabel('Average Risk Score')
        plt.title('Top 10 Risky Users', fontsize=14, fontweight='bold')
        
        # 12. Malware Confidence Scores
        plt.subplot(4, 3, 12)
        plt.hist(self.malware_indicators['confidence_score'], bins=15, alpha=0.7, color='orange', edgecolor='black')
        plt.xlabel('Confidence Score')
        plt.ylabel('Frequency')
        plt.title('Malware Detection Confidence', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('comprehensive_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✓ Comprehensive plots saved as 'comprehensive_analysis.png'")
    
    def create_interactive_plots(self):
        """Create interactive Plotly visualizations."""
        print("\nCreating interactive visualizations...")
        
        # 1. Interactive Threat Timeline
        fig1 = px.scatter(self.threat_scenarios, 
                         x='detection_time', 
                         y='risk_score',
                         color='severity',
                         size='financial_impact',
                         hover_data=['threat_type', 'user_id'],
                         title='Threat Detection Timeline with Risk Scores')
        fig1.write_html('threat_timeline.html')
        
        # 2. Network Traffic Analysis
        fig2 = px.scatter(self.network_logs,
                         x='bytes_transferred',
                         y='connection_duration',
                         color='severity',
                         size='bytes_transferred',
                         hover_data=['source_ip', 'destination_ip', 'protocol'],
                         title='Network Traffic Analysis')
        fig2.write_html('network_traffic.html')
        
        # 3. UEBA Risk Heatmap
        ueba_pivot = self.ueba_data.pivot_table(
            values='risk_score',
            index='user_id',
            columns='activity_type',
            aggfunc='mean'
        ).fillna(0)
        
        fig3 = px.imshow(ueba_pivot,
                        title='UEBA Risk Heatmap by User and Activity',
                        color_continuous_scale='Reds')
        fig3.write_html('ueba_heatmap.html')
        
        print("✓ Interactive plots saved as HTML files")
    
    def generate_statistical_report(self):
        """Generate comprehensive statistical report."""
        print("\nGenerating statistical report...")
        
        report = []
        report.append("=" * 60)
        report.append("INSIDER THREAT DETECTION DATASET - STATISTICAL REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Dataset Overview
        report.append("DATASET OVERVIEW:")
        report.append("-" * 20)
        report.append(f"UEBA Records: {len(self.ueba_data)}")
        report.append(f"Network Logs: {len(self.network_logs)}")
        report.append(f"PAM Events: {len(self.pam_data)}")
        report.append(f"DLP Violations: {len(self.dlp_events)}")
        report.append(f"Threat Scenarios: {len(self.threat_scenarios)}")
        report.append(f"Malware Indicators: {len(self.malware_indicators)}")
        report.append("")
        
        # Threat Analysis
        report.append("THREAT ANALYSIS:")
        report.append("-" * 20)
        report.append(f"High Severity Threats: {len(self.threat_scenarios[self.threat_scenarios['severity'] == 'high'])}")
        report.append(f"Medium Severity Threats: {len(self.threat_scenarios[self.threat_scenarios['severity'] == 'medium'])}")
        report.append(f"Low Severity Threats: {len(self.threat_scenarios[self.threat_scenarios['severity'] == 'low'])}")
        report.append(f"Average Risk Score: {self.threat_scenarios['risk_score'].mean():.3f}")
        report.append(f"Total Financial Impact: ${self.threat_scenarios['financial_impact'].sum():,}")
        report.append("")
        
        # User Analysis
        report.append("USER ANALYSIS:")
        report.append("-" * 20)
        report.append(f"Unique Users: {self.ueba_data['user_id'].nunique()}")
        report.append(f"Most Active User: {self.ueba_data['user_id'].value_counts().index[0]}")
        report.append(f"Highest Risk User: {self.ueba_data.groupby('user_id')['risk_score'].mean().idxmax()}")
        report.append("")
        
        # Network Analysis
        report.append("NETWORK ANALYSIS:")
        report.append("-" * 20)
        report.append(f"Unique Source IPs: {self.network_logs['source_ip'].nunique()}")
        report.append(f"Unique Destination IPs: {self.network_logs['destination_ip'].nunique()}")
        report.append(f"Total Data Transferred: {self.network_logs['bytes_transferred'].sum():,} bytes")
        report.append(f"High Severity Events: {len(self.network_logs[self.network_logs['severity'] == 'high'])}")
        report.append("")
        
        # Malware Analysis
        report.append("MALWARE ANALYSIS:")
        report.append("-" * 20)
        report.append(f"High Impact Malware: {len(self.malware_indicators[self.malware_indicators['system_impact'] == 'high'])}")
        report.append(f"Average Confidence Score: {self.malware_indicators['confidence_score'].mean():.3f}")
        report.append(f"Unique Threat Families: {self.malware_indicators['threat_family'].nunique()}")
        report.append("")
        
        # Save report
        with open('statistical_report.txt', 'w') as f:
            f.write('\n'.join(report))
        
        print("✓ Statistical report saved as 'statistical_report.txt'")
        print('\n'.join(report))
    
    def create_machine_learning_demo(self):
        """Create machine learning demonstration."""
        print("\nCreating machine learning demonstration...")
        
        # Create features for ML
        features = []
        
        for _, scenario in self.threat_scenarios.iterrows():
            user_id = scenario['user_id']
            
            # Get user's UEBA data
            user_ueba = self.ueba_data[self.ueba_data['user_id'] == user_id]
            user_network = self.network_logs[self.network_logs['user_id'] == user_id]
            user_pam = self.pam_data[self.pam_data['user_id'] == user_id]
            user_dlp = self.dlp_events[self.dlp_events['user_id'] == user_id]
            
            feature_vector = {
                'scenario_id': scenario['scenario_id'],
                'user_id': user_id,
                'ueba_activities': len(user_ueba),
                'ueba_avg_risk': user_ueba['risk_score'].mean() if len(user_ueba) > 0 else 0,
                'network_connections': len(user_network),
                'network_bytes': user_network['bytes_transferred'].sum() if len(user_network) > 0 else 0,
                'pam_events': len(user_pam),
                'dlp_violations': len(user_dlp),
                'threat_severity': 1 if scenario['severity'] == 'high' else (0.5 if scenario['severity'] == 'medium' else 0),
                'risk_score': scenario['risk_score'],
                'financial_impact': scenario['financial_impact'],
                'escalation_required': 1 if scenario['escalation_path'] == 'immediate_escalation' else 0
            }
            features.append(feature_vector)
        
        ml_data = pd.DataFrame(features)
        
        # Create ML visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Feature correlation
        correlation_matrix = ml_data[['ueba_avg_risk', 'network_bytes', 'pam_events', 'dlp_violations', 'risk_score']].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=axes[0,0])
        axes[0,0].set_title('Feature Correlation Matrix')
        
        # Risk vs Financial Impact
        axes[0,1].scatter(ml_data['risk_score'], ml_data['financial_impact'], alpha=0.6)
        axes[0,1].set_xlabel('Risk Score')
        axes[0,1].set_ylabel('Financial Impact ($)')
        axes[0,1].set_title('Risk Score vs Financial Impact')
        
        # Feature importance (simulated)
        feature_importance = {
            'UEBA Risk': 0.35,
            'Network Activity': 0.25,
            'PAM Events': 0.20,
            'DLP Violations': 0.20
        }
        axes[1,0].bar(feature_importance.keys(), feature_importance.values(), color='lightblue')
        axes[1,0].set_title('Feature Importance (Simulated)')
        axes[1,0].set_ylabel('Importance Score')
        
        # Escalation prediction
        escalation_counts = ml_data['escalation_required'].value_counts()
        axes[1,1].pie(escalation_counts.values, labels=['No Escalation', 'Escalation Required'], autopct='%1.1f%%')
        axes[1,1].set_title('Escalation Requirements')
        
        plt.tight_layout()
        plt.savefig('ml_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Save ML data
        ml_data.to_csv('ml_features.csv', index=False)
        
        print("✓ Machine learning analysis saved as 'ml_analysis.png'")
        print("✓ ML features saved as 'ml_features.csv'")
    
    def run_complete_analysis(self):
        """Run complete analysis pipeline."""
        print("🚀 Starting Comprehensive Insider Threat Analysis")
        print("=" * 60)
        
        # Load data
        if not self.load_datasets():
            return
        
        # Preprocess data
        self.preprocess_data()
        
        # Generate all analyses
        self.create_comprehensive_plots()
        self.create_interactive_plots()
        self.generate_statistical_report()
        self.create_machine_learning_demo()
        
        print("\n" + "=" * 60)
        print("✅ COMPREHENSIVE ANALYSIS COMPLETED!")
        print("=" * 60)
        print("\nGenerated Files:")
        print("• comprehensive_analysis.png - Static visualizations")
        print("• threat_timeline.html - Interactive threat timeline")
        print("• network_traffic.html - Interactive network analysis")
        print("• ueba_heatmap.html - Interactive UEBA heatmap")
        print("• statistical_report.txt - Statistical summary")
        print("• ml_analysis.png - Machine learning analysis")
        print("• ml_features.csv - ML-ready features")

def main():
    """Main function to run the analysis."""
    analyzer = InsiderThreatAnalyzer()
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()
