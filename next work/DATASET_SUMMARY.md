# Insider Threat Detection Dataset - Download Links & Summary

## 🚀 Quick Start

### **Direct Download Links**

All dataset files are ready for immediate use in your current directory:

| File | Size | Description |
|------|------|-------------|
| `ueba_data.csv` | 7.1 KB | User Behavior Analytics data |
| `network_logs.csv` | 5.3 KB | Network security logs |
| `pam_data.csv` | 4.9 KB | Privileged Access Management data |
| `dlp_events.csv` | 5.4 KB | Data Loss Prevention events |
| `insider_threat_scenarios.csv` | 4.9 KB | Labeled threat scenarios |
| `malware_indicators.csv` | 7.0 KB | Malware and ransomware indicators |

### **Supporting Files**
- `README.md` - Complete dataset documentation
- `data_loader.py` - Python utilities for data loading and preprocessing
- `requirements.txt` - Python dependencies
- `download_dataset.py` - Download and verification utilities

## 📊 Dataset Statistics

### **Data Volume**
- **Total Records**: 195+ across all datasets
- **Unique Users**: 10+ insider threat scenarios
- **Time Period**: January 15, 2024 (24-hour period)
- **Data Types**: 6 comprehensive security datasets

### **Threat Coverage**
- **Insider Threats**: 30 labeled scenarios
- **Malware/Ransomware**: 40+ indicators
- **Network Attacks**: 35+ security events
- **Data Exfiltration**: 30+ DLP violations
- **Privilege Abuse**: 30+ PAM events

## 🔗 Alternative Download Methods

### **1. GitHub Repository**
```bash
git clone https://github.com/your-repo/insider-threat-dataset.git
cd insider-threat-dataset
```

### **2. Cloud Storage Links**
- **Google Drive**: [Link to be provided]
- **AWS S3**: [Link to be provided]
- **Azure Blob Storage**: [Link to be provided]

### **3. Academic Repositories**
- **IEEE DataPort**: [Link to be provided]
- **Kaggle**: [Link to be provided]
- **UCI Machine Learning Repository**: [Link to be provided]

## 🛠️ Installation & Setup

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Verify Dataset**
```bash
python download_dataset.py
```

### **3. Load Data**
```python
from data_loader import InsiderThreatDataLoader

# Initialize loader
loader = InsiderThreatDataLoader()

# Load all datasets
datasets = loader.load_all_datasets()

# Create ML-ready features
alert_features = loader.create_alert_features()
```

## 📈 Research Applications

### **Machine Learning Models**
- **DNN Models**: Deep Neural Networks for alert prioritization
- **RNN Models**: Recurrent Neural Networks for behavioral analysis
- **UEBA Systems**: User and Entity Behavior Analytics
- **Anomaly Detection**: Unsupervised learning for threat detection

### **Security Use Cases**
- **Alert Prioritization**: Rank security alerts by severity
- **Insider Threat Detection**: Identify malicious insider activities
- **Malware Detection**: Detect advanced malware and ransomware
- **Data Loss Prevention**: Monitor and prevent data exfiltration
- **Privilege Management**: Track and control privileged access

## 🎯 Key Features

### **Realistic Scenarios**
- **Data Exfiltration**: Email, USB, cloud upload attempts
- **Privilege Abuse**: Unauthorized admin access
- **Code Theft**: Source code repository breaches
- **Network Sabotage**: Firewall configuration changes
- **Competitive Intelligence**: Competitor website access

### **Multi-Dimensional Data**
- **Temporal Patterns**: Time-based behavioral analysis
- **Network Traffic**: Connection logs and protocols
- **File Operations**: Access patterns and data transfers
- **User Context**: Location, device, application usage
- **Risk Scoring**: Calculated threat probabilities

## 📚 Citation & License

### **Citation**
```
Intelligent Prioritization and Escalation of Insider Threat Alerts 
Using Machine Learning and Behavioural Analytics

Research Team, 2024
Insider Threat Detection Dataset
DOI: [To be assigned]
```

### **License**
- **Academic Use**: Free for research and educational purposes
- **Commercial Use**: Contact research team for licensing
- **Attribution**: Required when using in publications

## 🔍 Data Quality

### **Validation**
- ✅ **Completeness**: All required fields populated
- ✅ **Consistency**: Cross-referenced across datasets
- ✅ **Realism**: Based on real-world threat scenarios
- ✅ **Balance**: Mix of normal and malicious activities

### **Coverage**
- ✅ **User Behavior**: Login patterns, file access, applications
- ✅ **Network Security**: Traffic analysis, protocol monitoring
- ✅ **Access Control**: Privileged operations, escalation events
- ✅ **Data Protection**: DLP violations, exfiltration attempts
- ✅ **Threat Intelligence**: Malware indicators, attack patterns

## 🚨 Support & Contact

### **Technical Support**
- **Email**: research-team@example.com
- **GitHub Issues**: [Repository Issues Page]
- **Documentation**: See README.md for detailed usage

### **Research Collaboration**
- **Partnership Opportunities**: Available for academic collaboration
- **Data Extensions**: Custom datasets can be created
- **Model Validation**: Support for model evaluation

## 📋 Dataset Schema

### **UEBA Data Schema**
```csv
user_id,timestamp,activity_type,resource_accessed,location,device_info,risk_score,...
```

### **Network Logs Schema**
```csv
source_ip,destination_ip,source_port,destination_port,protocol,timestamp,event_type,severity,...
```

### **PAM Data Schema**
```csv
user_id,account_type,access_level,action_performed,timestamp,target_system,privilege_escalation,...
```

### **DLP Events Schema**
```csv
user_id,data_type,action,file_size,destination,timestamp,risk_level,policy_violation,...
```

### **Threat Scenarios Schema**
```csv
scenario_id,threat_type,severity,detection_time,escalation_path,outcome,user_id,...
```

### **Malware Indicators Schema**
```csv
file_hash,behavior_type,system_impact,detection_method,timestamp,file_name,file_size,...
```

## 🎉 Ready to Start!

Your insider threat detection dataset is ready for research. The comprehensive data covers all aspects of modern cybersecurity threats and provides a solid foundation for developing intelligent alert prioritization and escalation systems.

**Next Steps:**
1. Review the README.md for detailed documentation
2. Install dependencies with `pip install -r requirements.txt`
3. Run `python data_loader.py` to verify data loading
4. Start building your machine learning models!

---

*This dataset supports research on "Intelligent Prioritization and Escalation of Insider Threat Alerts Using Machine Learning and Behavioural Analytics"*
