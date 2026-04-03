#!/usr/bin/env python3
"""
Individual Network Analysis Plots
================================

This script generates individual plots for network analysis including:
- Network traffic patterns
- Protocol analysis
- Security events
- Traffic volume analysis

Author: Research Team
Date: 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

def load_data():
    """Load the network logs data."""
    try:
        df = pd.read_csv('network_logs.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        print(f"✓ Loaded {len(df)} network log records")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def plot_traffic_patterns(df):
    """Plot network traffic patterns."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Protocol distribution
    protocol_counts = df['protocol'].value_counts()
    axes[0,0].pie(protocol_counts.values, labels=protocol_counts.index, autopct='%1.1f%%')
    axes[0,0].set_title('Network Protocol Distribution')
    
    # Event type distribution
    event_counts = df['event_type'].value_counts()
    axes[0,1].bar(event_counts.index, event_counts.values, color='lightblue')
    axes[0,1].set_xlabel('Event Type')
    axes[0,1].set_ylabel('Count')
    axes[0,1].set_title('Network Event Type Distribution')
    axes[0,1].tick_params(axis='x', rotation=45)
    axes[0,1].grid(True, alpha=0.3)
    
    # Traffic volume by hour
    df['hour'] = df['timestamp'].dt.hour
    hourly_traffic = df.groupby('hour')['bytes_transferred'].sum()
    axes[1,0].plot(hourly_traffic.index, hourly_traffic.values, marker='o', linewidth=2, color='green')
    axes[1,0].set_xlabel('Hour of Day')
    axes[1,0].set_ylabel('Total Bytes Transferred')
    axes[1,0].set_title('Network Traffic Volume by Hour')
    axes[1,0].grid(True, alpha=0.3)
    
    # Top source IPs
    top_sources = df['source_ip'].value_counts().head(10)
    axes[1,1].barh(top_sources.index, top_sources.values, color='lightcoral')
    axes[1,1].set_xlabel('Connection Count')
    axes[1,1].set_title('Top 10 Source IPs')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('network_traffic_patterns.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: network_traffic_patterns.png")

def plot_security_events(df):
    """Plot network security events analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Severity distribution
    severity_counts = df['severity'].value_counts()
    colors = ['#ff6b6b', '#ffd93d', '#6bcf7f']
    axes[0,0].pie(severity_counts.values, labels=severity_counts.index, autopct='%1.1f%%', colors=colors)
    axes[0,0].set_title('Network Event Severity Distribution')
    
    # Security events by protocol
    security_by_protocol = pd.crosstab(df['protocol'], df['severity'])
    security_by_protocol.plot(kind='bar', ax=axes[0,1], color=colors)
    axes[0,1].set_xlabel('Protocol')
    axes[0,1].set_ylabel('Count')
    axes[0,1].set_title('Security Events by Protocol')
    axes[0,1].legend(title='Severity')
    axes[0,1].tick_params(axis='x', rotation=45)
    axes[0,1].grid(True, alpha=0.3)
    
    # High severity events timeline
    high_severity = df[df['severity'] == 'high']
    if len(high_severity) > 0:
        high_severity_sorted = high_severity.sort_values('timestamp')
        axes[1,0].scatter(range(len(high_severity_sorted)), high_severity_sorted['bytes_transferred'], 
                         alpha=0.6, color='red')
        axes[1,0].set_xlabel('Time Sequence')
        axes[1,0].set_ylabel('Bytes Transferred')
        axes[1,0].set_title('High Severity Events Timeline')
        axes[1,0].grid(True, alpha=0.3)
    
    # Event type by severity
    event_severity = pd.crosstab(df['event_type'], df['severity'])
    event_severity.plot(kind='bar', ax=axes[1,1], color=colors)
    axes[1,1].set_xlabel('Event Type')
    axes[1,1].set_ylabel('Count')
    axes[1,1].set_title('Event Types by Severity')
    axes[1,1].legend(title='Severity')
    axes[1,1].tick_params(axis='x', rotation=45)
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('network_security_events.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: network_security_events.png")

def plot_traffic_volume_analysis(df):
    """Plot network traffic volume analysis."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Bytes transferred distribution
    axes[0,0].hist(df['bytes_transferred'], bins=30, color='skyblue', alpha=0.7, edgecolor='black')
    axes[0,0].set_xlabel('Bytes Transferred')
    axes[0,0].set_ylabel('Frequency')
    axes[0,0].set_title('Network Traffic Volume Distribution')
    axes[0,0].grid(True, alpha=0.3)
    
    # Traffic volume by protocol
    protocol_traffic = df.groupby('protocol')['bytes_transferred'].sum().sort_values(ascending=False)
    axes[0,1].bar(protocol_traffic.index, protocol_traffic.values, color='lightgreen')
    axes[0,1].set_xlabel('Protocol')
    axes[0,1].set_ylabel('Total Bytes Transferred')
    axes[0,1].set_title('Traffic Volume by Protocol')
    axes[0,1].tick_params(axis='x', rotation=45)
    axes[0,1].grid(True, alpha=0.3)
    
    # Traffic volume by severity
    severity_traffic = df.groupby('severity')['bytes_transferred'].sum().sort_values(ascending=False)
    colors = ['#ff6b6b', '#ffd93d', '#6bcf7f']
    axes[1,0].bar(severity_traffic.index, severity_traffic.values, color=colors)
    axes[1,0].set_xlabel('Severity')
    axes[1,0].set_ylabel('Total Bytes Transferred')
    axes[1,0].set_title('Traffic Volume by Severity')
    axes[1,0].grid(True, alpha=0.3)
    
    # Traffic volume box plot by protocol
    df.boxplot(column='bytes_transferred', by='protocol', ax=axes[1,1])
    axes[1,1].set_xlabel('Protocol')
    axes[1,1].set_ylabel('Bytes Transferred')
    axes[1,1].set_title('Traffic Volume Distribution by Protocol')
    axes[1,1].tick_params(axis='x', rotation=45)
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('network_traffic_volume.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: network_traffic_volume.png")

def plot_network_anomalies(df):
    """Plot network anomaly detection."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Traffic volume timeline
    df_sorted = df.sort_values('timestamp')
    axes[0,0].scatter(range(len(df_sorted)), df_sorted['bytes_transferred'], alpha=0.6, color='blue')
    axes[0,0].set_xlabel('Time Sequence')
    axes[0,0].set_ylabel('Bytes Transferred')
    axes[0,0].set_title('Network Traffic Volume Timeline')
    axes[0,0].grid(True, alpha=0.3)
    
    # Anomaly detection (high traffic volume)
    traffic_threshold = df['bytes_transferred'].quantile(0.95)
    high_traffic = df[df['bytes_transferred'] > traffic_threshold]
    
    axes[0,1].hist(df['bytes_transferred'], bins=30, alpha=0.7, color='lightblue', label='Normal')
    axes[0,1].hist(high_traffic['bytes_transferred'], bins=30, alpha=0.7, color='red', label='High Traffic')
    axes[0,1].axvline(traffic_threshold, color='red', linestyle='--', label=f'Threshold ({traffic_threshold:.0f})')
    axes[0,1].set_xlabel('Bytes Transferred')
    axes[0,1].set_ylabel('Frequency')
    axes[0,1].set_title('Network Traffic Anomaly Detection')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # Connection patterns
    connection_counts = df.groupby('source_ip').size().sort_values(ascending=False)
    axes[1,0].hist(connection_counts, bins=20, color='purple', alpha=0.7, edgecolor='black')
    axes[1,0].set_xlabel('Connection Count per IP')
    axes[1,0].set_ylabel('Frequency')
    axes[1,0].set_title('Connection Patterns Distribution')
    axes[1,0].grid(True, alpha=0.3)
    
    # Protocol vs severity heatmap
    protocol_severity = pd.crosstab(df['protocol'], df['severity'])
    sns.heatmap(protocol_severity, annot=True, fmt='d', cmap='YlOrRd', ax=axes[1,1])
    axes[1,1].set_title('Protocol vs Severity Heatmap')
    
    plt.tight_layout()
    plt.savefig('network_anomaly_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Saved: network_anomaly_analysis.png")

def main():
    """Main function to generate all network analysis plots."""
    print("🚀 GENERATING INDIVIDUAL NETWORK ANALYSIS PLOTS")
    print("=" * 60)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Generate plots
    print("\n📊 Generating traffic patterns...")
    plot_traffic_patterns(df)
    
    print("\n📊 Generating security events analysis...")
    plot_security_events(df)
    
    print("\n📊 Generating traffic volume analysis...")
    plot_traffic_volume_analysis(df)
    
    print("\n📊 Generating network anomaly analysis...")
    plot_network_anomalies(df)
    
    print("\n" + "=" * 60)
    print("✅ ALL NETWORK ANALYSIS PLOTS GENERATED!")
    print("=" * 60)
    print("\nGenerated Files:")
    print("• network_traffic_patterns.png")
    print("• network_security_events.png")
    print("• network_traffic_volume.png")
    print("• network_anomaly_analysis.png")

if __name__ == "__main__":
    main()
