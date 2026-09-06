#!/usr/bin/env python3
"""
Individual Threat Analysis Plots
================================

This script generates individual plots for threat analysis including:
- Threat severity distribution
- Risk score analysis
- Threat type analysis
- Financial impact analysis

Author: Research Team
Date: 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

def load_data():
    """Load the insider threat scenarios data."""
    try:
        df = pd.read_csv('insider_threat_scenarios.csv')
        print(f"✓ Loaded {len(df)} threat scenarios")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def plot_threat_severity(df):
    """Plot threat severity distribution."""
    plt.figure(figsize=(10, 6))
    
    severity_counts = df['severity'].value_counts()
    colors = ['#ff6b6b', '#ffd93d', '#6bcf7f']
    
    plt.pie(severity_counts.values, labels=severity_counts.index, autopct='%1.1f%%', 
            colors=colors, startangle=90)
    plt.title('Threat Severity Distribution', fontsize=16, fontweight='bold')
    plt.axis('equal')
    
    plt.tight_layout()
    plt.savefig('threat_severity_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: threat_severity_distribution.png")

def plot_risk_score_analysis(df):
    """Plot risk score analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Risk score histogram
    axes[0,0].hist(df['risk_score'], bins=20, color='skyblue', alpha=0.7, edgecolor='black')
    axes[0,0].set_xlabel('Risk Score')
    axes[0,0].set_ylabel('Frequency')
    axes[0,0].set_title('Risk Score Distribution')
    axes[0,0].grid(True, alpha=0.3)
    
    # Risk score by severity
    severity_risk = df.groupby('severity')['risk_score'].mean().sort_values(ascending=False)
    axes[0,1].bar(severity_risk.index, severity_risk.values, color=['#ff6b6b', '#ffd93d', '#6bcf7f'])
    axes[0,1].set_xlabel('Severity')
    axes[0,1].set_ylabel('Average Risk Score')
    axes[0,1].set_title('Average Risk Score by Severity')
    axes[0,1].grid(True, alpha=0.3)
    
    # Risk score box plot
    df.boxplot(column='risk_score', by='severity', ax=axes[1,0])
    axes[1,0].set_xlabel('Severity')
    axes[1,0].set_ylabel('Risk Score')
    axes[1,0].set_title('Risk Score Distribution by Severity')
    axes[1,0].grid(True, alpha=0.3)
    
    # Risk score vs financial impact
    axes[1,1].scatter(df['risk_score'], df['financial_impact'], alpha=0.6, color='purple')
    axes[1,1].set_xlabel('Risk Score')
    axes[1,1].set_ylabel('Financial Impact ($)')
    axes[1,1].set_title('Risk Score vs Financial Impact')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('risk_score_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: risk_score_analysis.png")

def plot_threat_types(df):
    """Plot threat type analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Threat type distribution
    threat_counts = df['threat_type'].value_counts()
    axes[0,0].barh(threat_counts.index, threat_counts.values, color='lightcoral')
    axes[0,0].set_xlabel('Count')
    axes[0,0].set_title('Threat Type Distribution')
    axes[0,0].grid(True, alpha=0.3)
    
    # Threat type by severity
    threat_severity = pd.crosstab(df['threat_type'], df['severity'])
    threat_severity.plot(kind='bar', ax=axes[0,1], color=['#ff6b6b', '#ffd93d', '#6bcf7f'])
    axes[0,1].set_xlabel('Threat Type')
    axes[0,1].set_ylabel('Count')
    axes[0,1].set_title('Threat Types by Severity')
    axes[0,1].legend(title='Severity')
    axes[0,1].tick_params(axis='x', rotation=45)
    axes[0,1].grid(True, alpha=0.3)
    
    # Average financial impact by threat type
    impact_by_type = df.groupby('threat_type')['financial_impact'].mean().sort_values(ascending=False)
    axes[1,0].bar(impact_by_type.index, impact_by_type.values, color='gold')
    axes[1,0].set_xlabel('Threat Type')
    axes[1,0].set_ylabel('Average Financial Impact ($)')
    axes[1,0].set_title('Average Financial Impact by Threat Type')
    axes[1,0].tick_params(axis='x', rotation=45)
    axes[1,0].grid(True, alpha=0.3)
    
    # Threat type heatmap
    threat_risk = df.groupby('threat_type')['risk_score'].mean().sort_values(ascending=False)
    axes[1,1].bar(threat_risk.index, threat_risk.values, color='lightblue')
    axes[1,1].set_xlabel('Threat Type')
    axes[1,1].set_ylabel('Average Risk Score')
    axes[1,1].set_title('Average Risk Score by Threat Type')
    axes[1,1].tick_params(axis='x', rotation=45)
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('threat_type_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: threat_type_analysis.png")

def plot_financial_impact(df):
    """Plot financial impact analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Financial impact distribution
    axes[0,0].hist(df['financial_impact'], bins=20, color='lightgreen', alpha=0.7, edgecolor='black')
    axes[0,0].set_xlabel('Financial Impact ($)')
    axes[0,0].set_ylabel('Frequency')
    axes[0,0].set_title('Financial Impact Distribution')
    axes[0,0].grid(True, alpha=0.3)
    
    # Financial impact by severity
    impact_by_severity = df.groupby('severity')['financial_impact'].mean().sort_values(ascending=False)
    axes[0,1].bar(impact_by_severity.index, impact_by_severity.values, color=['#ff6b6b', '#ffd93d', '#6bcf7f'])
    axes[0,1].set_xlabel('Severity')
    axes[0,1].set_ylabel('Average Financial Impact ($)')
    axes[0,1].set_title('Average Financial Impact by Severity')
    axes[0,1].grid(True, alpha=0.3)
    
    # Financial impact box plot
    df.boxplot(column='financial_impact', by='severity', ax=axes[1,0])
    axes[1,0].set_xlabel('Severity')
    axes[1,0].set_ylabel('Financial Impact ($)')
    axes[1,0].set_title('Financial Impact Distribution by Severity')
    axes[1,0].grid(True, alpha=0.3)
    
    # Cumulative financial impact
    sorted_impact = df['financial_impact'].sort_values(ascending=False)
    cumulative_impact = sorted_impact.cumsum()
    axes[1,1].plot(range(len(cumulative_impact)), cumulative_impact, linewidth=2, color='red')
    axes[1,1].set_xlabel('Threat Scenario Rank')
    axes[1,1].set_ylabel('Cumulative Financial Impact ($)')
    axes[1,1].set_title('Cumulative Financial Impact')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('financial_impact_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: financial_impact_analysis.png")

def main():
    """Main function to generate all threat analysis plots."""
    print("🚀 GENERATING INDIVIDUAL THREAT ANALYSIS PLOTS")
    print("=" * 60)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Generate plots
    print("\n📊 Generating threat severity distribution...")
    plot_threat_severity(df)
    
    print("\n📊 Generating risk score analysis...")
    plot_risk_score_analysis(df)
    
    print("\n📊 Generating threat type analysis...")
    plot_threat_types(df)
    
    print("\n📊 Generating financial impact analysis...")
    plot_financial_impact(df)
    
    print("\n" + "=" * 60)
    print("✅ ALL THREAT ANALYSIS PLOTS GENERATED!")
    print("=" * 60)
    print("\nGenerated Files:")
    print("• threat_severity_distribution.png")
    print("• risk_score_analysis.png")
    print("• threat_type_analysis.png")
    print("• financial_impact_analysis.png")

if __name__ == "__main__":
    main()
