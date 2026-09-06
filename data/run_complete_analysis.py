#!/usr/bin/env python3
"""
Complete Analysis Runner for Insider Threat Detection Dataset
============================================================

This script runs all analyses including data exploration, visualizations,
statistical analysis, and machine learning models.

Author: Research Team
Date: 2024
"""

import os
import sys
import time
from datetime import datetime

def run_analysis():
    """Run complete analysis pipeline."""
    
    print("🚀 INSIDER THREAT DETECTION - COMPLETE ANALYSIS")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check if required files exist
    required_files = [
        'ueba_data.csv',
        'network_logs.csv', 
        'pam_data.csv',
        'dlp_events.csv',
        'insider_threat_scenarios.csv',
        'malware_indicators.csv'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required dataset files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all dataset files are in the current directory.")
        return False
    
    print("✅ All dataset files found!")
    
    # Step 1: Basic Data Analysis
    print("\n" + "=" * 60)
    print("STEP 1: BASIC DATA ANALYSIS")
    print("=" * 60)
    
    try:
        from data_loader import InsiderThreatDataLoader
        loader = InsiderThreatDataLoader()
        datasets = loader.load_all_datasets()
        
        if datasets:
            summary = loader.get_dataset_summary()
            print("\nDataset Summary:")
            for dataset_name, stats in summary.items():
                print(f"\n{dataset_name.upper()} Dataset:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
        else:
            print("❌ Failed to load datasets")
            return False
            
    except Exception as e:
        print(f"❌ Error in basic data analysis: {e}")
        return False
    
    # Step 2: Comprehensive Analysis
    print("\n" + "=" * 60)
    print("STEP 2: COMPREHENSIVE ANALYSIS")
    print("=" * 60)
    
    try:
        from comprehensive_analysis import InsiderThreatAnalyzer
        analyzer = InsiderThreatAnalyzer()
        
        if analyzer.load_datasets():
            analyzer.preprocess_data()
            analyzer.create_comprehensive_plots()
            analyzer.create_interactive_plots()
            analyzer.generate_statistical_report()
            analyzer.create_machine_learning_demo()
        else:
            print("❌ Failed to load datasets for comprehensive analysis")
            return False
            
    except Exception as e:
        print(f"❌ Error in comprehensive analysis: {e}")
        return False
    
    # Step 3: Advanced Machine Learning
    print("\n" + "=" * 60)
    print("STEP 3: ADVANCED MACHINE LEARNING")
    print("=" * 60)
    
    try:
        from advanced_ml_models import AdvancedInsiderThreatML
        ml_analyzer = AdvancedInsiderThreatML()
        ml_analyzer.run_complete_ml_analysis()
        
    except Exception as e:
        print(f"❌ Error in advanced ML analysis: {e}")
        return False
    
    # Step 4: Generate Final Report
    print("\n" + "=" * 60)
    print("STEP 4: GENERATING FINAL REPORT")
    print("=" * 60)
    
    try:
        generate_final_report()
    except Exception as e:
        print(f"❌ Error generating final report: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ COMPLETE ANALYSIS FINISHED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

def generate_final_report():
    """Generate comprehensive final report."""
    
    report = []
    report.append("=" * 80)
    report.append("INSIDER THREAT DETECTION - COMPLETE ANALYSIS REPORT")
    report.append("=" * 80)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Dataset Overview
    report.append("DATASET OVERVIEW")
    report.append("-" * 40)
    report.append("This analysis covers comprehensive insider threat detection using:")
    report.append("• User Behavior Analytics (UEBA) data")
    report.append("• Network security logs")
    report.append("• Privileged Access Management (PAM) data")
    report.append("• Data Loss Prevention (DLP) events")
    report.append("• Labeled insider threat scenarios")
    report.append("• Malware and ransomware indicators")
    report.append("")
    
    # Analysis Components
    report.append("ANALYSIS COMPONENTS")
    report.append("-" * 40)
    report.append("1. Data Exploration and Preprocessing")
    report.append("2. Statistical Analysis and Visualization")
    report.append("3. Interactive Data Visualization")
    report.append("4. Traditional Machine Learning Models")
    report.append("5. Deep Neural Networks (DNN)")
    report.append("6. Recurrent Neural Networks (RNN)")
    report.append("7. Model Performance Evaluation")
    report.append("8. Feature Importance Analysis")
    report.append("")
    
    # Key Findings
    report.append("KEY FINDINGS")
    report.append("-" * 40)
    report.append("• Comprehensive threat detection framework implemented")
    report.append("• Multiple ML models trained and evaluated")
    report.append("• Advanced visualization techniques applied")
    report.append("• Feature engineering for alert prioritization")
    report.append("• Behavioral analytics for insider threat detection")
    report.append("")
    
    # Generated Files
    report.append("GENERATED FILES")
    report.append("-" * 40)
    report.append("Static Visualizations:")
    report.append("• comprehensive_analysis.png - 12-panel comprehensive analysis")
    report.append("• ml_analysis.png - Machine learning analysis")
    report.append("• advanced_ml_results.png - Advanced ML model results")
    report.append("")
    report.append("Interactive Visualizations:")
    report.append("• threat_timeline.html - Interactive threat timeline")
    report.append("• network_traffic.html - Network traffic analysis")
    report.append("• ueba_heatmap.html - UEBA risk heatmap")
    report.append("")
    report.append("Reports:")
    report.append("• statistical_report.txt - Statistical analysis report")
    report.append("• ml_analysis_report.txt - Machine learning report")
    report.append("• ml_features.csv - ML-ready feature dataset")
    report.append("")
    
    # Research Applications
    report.append("RESEARCH APPLICATIONS")
    report.append("-" * 40)
    report.append("This dataset and analysis support research on:")
    report.append("• Intelligent alert prioritization")
    report.append("• Behavioral analytics for threat detection")
    report.append("• Machine learning in cybersecurity")
    report.append("• Insider threat detection and prevention")
    report.append("• Network security monitoring")
    report.append("• Data loss prevention")
    report.append("")
    
    # Technical Implementation
    report.append("TECHNICAL IMPLEMENTATION")
    report.append("-" * 40)
    report.append("• Python-based analysis pipeline")
    report.append("• TensorFlow/Keras for deep learning")
    report.append("• Scikit-learn for traditional ML")
    report.append("• Matplotlib/Seaborn for static plots")
    report.append("• Plotly for interactive visualizations")
    report.append("• Pandas for data manipulation")
    report.append("")
    
    # Citation
    report.append("CITATION")
    report.append("-" * 40)
    report.append("Intelligent Prioritization and Escalation of Insider Threat Alerts")
    report.append("Using Machine Learning and Behavioural Analytics")
    report.append("")
    report.append("Research Team, 2024")
    report.append("Insider Threat Detection Dataset and Analysis")
    report.append("")
    
    # Save final report
    with open('complete_analysis_report.txt', 'w') as f:
        f.write('\n'.join(report))
    
    print("✓ Final report saved as 'complete_analysis_report.txt'")
    print('\n'.join(report))

def main():
    """Main function."""
    start_time = time.time()
    
    success = run_analysis()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nTotal execution time: {duration:.2f} seconds ({duration/60:.2f} minutes)")
    
    if success:
        print("\n🎉 All analyses completed successfully!")
        print("\nGenerated Files Summary:")
        print("📊 Static Visualizations:")
        print("   • comprehensive_analysis.png")
        print("   • ml_analysis.png") 
        print("   • advanced_ml_results.png")
        print("\n🌐 Interactive Visualizations:")
        print("   • threat_timeline.html")
        print("   • network_traffic.html")
        print("   • ueba_heatmap.html")
        print("\n📋 Reports:")
        print("   • statistical_report.txt")
        print("   • ml_analysis_report.txt")
        print("   • complete_analysis_report.txt")
        print("\n💾 Data Files:")
        print("   • ml_features.csv")
        print("   • alert_features.csv")
    else:
        print("\n❌ Analysis failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
