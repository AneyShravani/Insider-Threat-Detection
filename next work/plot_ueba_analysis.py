#!/usr/bin/env python3
"""
Individual UEBA Analysis Plots
==============================

This script generates individual plots for UEBA analysis including:
- User activity patterns
- Risk score distribution
- Activity type analysis
- Time-based behavior patterns

Author: Research Team
Date: 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

def load_data():
    """Load the UEBA data."""
    try:
        df = pd.read_csv('ueba_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        print(f"✓ Loaded {len(df)} UEBA records")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def plot_user_activity_patterns(df):
    """Plot user activity patterns."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Activity type distribution
    activity_counts = df['activity_type'].value_counts()
    axes[0,0].bar(activity_counts.index, activity_counts.values, color='lightblue')
    axes[0,0].set_xlabel('Activity Type')
    axes[0,0].set_ylabel('Count')
    axes[0,0].set_title('Activity Type Distribution')
    axes[0,0].tick_params(axis='x', rotation=45)
    axes[0,0].grid(True, alpha=0.3)
    
    # Top users by activity count
    user_activity = df['user_id'].value_counts().head(10)
    axes[0,1].barh(user_activity.index, user_activity.values, color='lightcoral')
    axes[0,1].set_xlabel('Activity Count')
    axes[0,1].set_title('Top 10 Most Active Users')
    axes[0,1].grid(True, alpha=0.3)
    
    # Resource access patterns
    resource_counts = df['resource_accessed'].value_counts().head(10)
    axes[1,0].barh(resource_counts.index, resource_counts.values, color='lightgreen')
    axes[1,0].set_xlabel('Access Count')
    axes[1,0].set_title('Top 10 Most Accessed Resources')
    axes[1,0].grid(True, alpha=0.3)
    
    # Activity by hour of day
    df['hour'] = df['timestamp'].dt.hour
    hourly_activity = df['hour'].value_counts().sort_index()
    axes[1,1].plot(hourly_activity.index, hourly_activity.values, marker='o', linewidth=2, color='purple')
    axes[1,1].set_xlabel('Hour of Day')
    axes[1,1].set_ylabel('Activity Count')
    axes[1,1].set_title('Activity by Hour of Day')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ueba_activity_patterns.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: ueba_activity_patterns.png")

def plot_risk_score_analysis(df):
    """Plot UEBA risk score analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Risk score distribution
    axes[0,0].hist(df['risk_score'], bins=30, color='skyblue', alpha=0.7, edgecolor='black')
    axes[0,0].set_xlabel('Risk Score')
    axes[0,0].set_ylabel('Frequency')
    axes[0,0].set_title('UEBA Risk Score Distribution')
    axes[0,0].grid(True, alpha=0.3)
    
    # Risk score by activity type
    activity_risk = df.groupby('activity_type')['risk_score'].mean().sort_values(ascending=False)
    axes[0,1].bar(activity_risk.index, activity_risk.values, color='gold')
    axes[0,1].set_xlabel('Activity Type')
    axes[0,1].set_ylabel('Average Risk Score')
    axes[0,1].set_title('Average Risk Score by Activity Type')
    axes[0,1].tick_params(axis='x', rotation=45)
    axes[0,1].grid(True, alpha=0.3)
    
    # Risk score box plot by activity
    df.boxplot(column='risk_score', by='activity_type', ax=axes[1,0])
    axes[1,0].set_xlabel('Activity Type')
    axes[1,0].set_ylabel('Risk Score')
    axes[1,0].set_title('Risk Score Distribution by Activity Type')
    axes[1,0].tick_params(axis='x', rotation=45)
    axes[1,0].grid(True, alpha=0.3)
    
    # Top risky users
    user_risk = df.groupby('user_id')['risk_score'].mean().sort_values(ascending=False).head(10)
    axes[1,1].barh(user_risk.index, user_risk.values, color='red')
    axes[1,1].set_xlabel('Average Risk Score')
    axes[1,1].set_title('Top 10 Riskiest Users')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ueba_risk_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: ueba_risk_analysis.png")

def plot_time_based_analysis(df):
    """Plot time-based behavior analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Activity by day of week
    df['day_of_week'] = df['timestamp'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_activity = df['day_of_week'].value_counts().reindex(day_order)
    axes[0,0].bar(daily_activity.index, daily_activity.values, color='lightblue')
    axes[0,0].set_xlabel('Day of Week')
    axes[0,0].set_ylabel('Activity Count')
    axes[0,0].set_title('Activity by Day of Week')
    axes[0,0].tick_params(axis='x', rotation=45)
    axes[0,0].grid(True, alpha=0.3)
    
    # Risk score by hour
    hourly_risk = df.groupby('hour')['risk_score'].mean()
    axes[0,1].plot(hourly_risk.index, hourly_risk.values, marker='o', linewidth=2, color='red')
    axes[0,1].set_xlabel('Hour of Day')
    axes[0,1].set_ylabel('Average Risk Score')
    axes[0,1].set_title('Average Risk Score by Hour')
    axes[0,1].grid(True, alpha=0.3)
    
    # Activity heatmap (hour vs day)
    activity_pivot = df.groupby(['hour', 'day_of_week']).size().unstack(fill_value=0)
    activity_pivot = activity_pivot.reindex(columns=day_order)
    sns.heatmap(activity_pivot, annot=True, fmt='d', cmap='YlOrRd', ax=axes[1,0])
    axes[1,0].set_title('Activity Heatmap (Hour vs Day)')
    
    # Risk score heatmap
    risk_pivot = df.groupby(['hour', 'day_of_week'])['risk_score'].mean().unstack(fill_value=0)
    risk_pivot = risk_pivot.reindex(columns=day_order)
    sns.heatmap(risk_pivot, annot=True, fmt='.2f', cmap='Reds', ax=axes[1,1])
    axes[1,1].set_title('Risk Score Heatmap (Hour vs Day)')
    
    plt.tight_layout()
    plt.savefig('ueba_time_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: ueba_time_analysis.png")

def plot_behavioral_anomalies(df):
    """Plot behavioral anomaly detection."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Risk score timeline
    df_sorted = df.sort_values('timestamp')
    axes[0,0].scatter(range(len(df_sorted)), df_sorted['risk_score'], alpha=0.6, color='blue')
    axes[0,0].set_xlabel('Time Sequence')
    axes[0,0].set_ylabel('Risk Score')
    axes[0,0].set_title('Risk Score Timeline')
    axes[0,0].grid(True, alpha=0.3)
    
    # High-risk activities
    high_risk = df[df['risk_score'] > df['risk_score'].quantile(0.9)]
    high_risk_activity = high_risk['activity_type'].value_counts()
    axes[0,1].pie(high_risk_activity.values, labels=high_risk_activity.index, autopct='%1.1f%%')
    axes[0,1].set_title('High-Risk Activities Distribution')
    
    # User behavior patterns
    user_patterns = df.groupby('user_id').agg({
        'risk_score': ['mean', 'std', 'count']
    }).round(2)
    user_patterns.columns = ['avg_risk', 'risk_std', 'activity_count']
    
    axes[1,0].scatter(user_patterns['activity_count'], user_patterns['avg_risk'], 
                     alpha=0.6, s=user_patterns['risk_std']*50, color='green')
    axes[1,0].set_xlabel('Activity Count')
    axes[1,0].set_ylabel('Average Risk Score')
    axes[1,0].set_title('User Behavior Patterns (Size = Risk Variability)')
    axes[1,0].grid(True, alpha=0.3)
    
    # Anomaly detection (simple threshold)
    anomaly_threshold = df['risk_score'].mean() + 2 * df['risk_score'].std()
    anomalies = df[df['risk_score'] > anomaly_threshold]
    
    axes[1,1].hist(df['risk_score'], bins=30, alpha=0.7, color='lightblue', label='Normal')
    axes[1,1].hist(anomalies['risk_score'], bins=30, alpha=0.7, color='red', label='Anomalies')
    axes[1,1].axvline(anomaly_threshold, color='red', linestyle='--', label=f'Threshold ({anomaly_threshold:.2f})')
    axes[1,1].set_xlabel('Risk Score')
    axes[1,1].set_ylabel('Frequency')
    axes[1,1].set_title('Anomaly Detection')
    axes[1,1].legend()
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('ueba_anomaly_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: ueba_anomaly_analysis.png")

def main():
    """Main function to generate all UEBA analysis plots."""
    print("🚀 GENERATING INDIVIDUAL UEBA ANALYSIS PLOTS")
    print("=" * 60)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Generate plots
    print("\n📊 Generating user activity patterns...")
    plot_user_activity_patterns(df)
    
    print("\n📊 Generating risk score analysis...")
    plot_risk_score_analysis(df)
    
    print("\n📊 Generating time-based analysis...")
    plot_time_based_analysis(df)
    
    print("\n📊 Generating behavioral anomaly analysis...")
    plot_behavioral_anomalies(df)
    
    print("\n" + "=" * 60)
    print("✅ ALL UEBA ANALYSIS PLOTS GENERATED!")
    print("=" * 60)
    print("\nGenerated Files:")
    print("• ueba_activity_patterns.png")
    print("• ueba_risk_analysis.png")
    print("• ueba_time_analysis.png")
    print("• ueba_anomaly_analysis.png")

if __name__ == "__main__":
    main()
