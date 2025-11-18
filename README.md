
If the model needs to be run, the required software version is as follows:
tensorflow==2.8.0
joblib==1.1.0
scikit-learn==1.0.2
xgboost==1.6.0
lightgbm==3.3.5

To obtain the sentiment prediction results, you can import the model into predictornew.py.

Weibo Data Collection Framework - Academic Guide

1. Cookie Acquisition Methods

Browser Extraction (Recommended):
1. Open Chrome and visit `m.weibo.cn`
2. Press F12 → Network tab → Refresh page
3. Search for keywords and find API requests
4. Copy as cURL and extract cookie values

Manual Inspection:
- F12 → Application → Storage → Cookies
- Copy all cookies under `https://m.weibo.cn`

2. Core Code Components

Time Format Conversion:
```python
def trans_time(v_str):
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
    return timeArray.strftime("%Y-%m-%d %H:%M:%S")
```

Data Collection Functions:
- `search_weibo()`: Discovers relevant Weibo posts
- `get_comments()`: Systematically collects comment data
- Implements academic-grade data validation and rate limiting

3. Research Configuration

Basic Setup:
```python
keyword_list = ['research topic keywords']
max_page = 10   Ethical pagination limit
comment_file = 'research_data.csv'
```

Rate Limiting Protocol:
- Random delays: 1-3 seconds between requests
- Maximum 10 pages per Weibo ID
- Cookie-based session authentication

4. Output Data Structure

The framework generates structured datasets containing:
- Weibo IDs for content tracking
- Timestamps for temporal analysis  
- Comment text for NLP processing
- User demographics for population studies
- Geographic data for spatial analysis

5. Ethical Compliance

Research Requirements:
- Use exclusively for academic purposes
- Adhere to platform Terms of Service
- Implement proper request throttling
- Anonymize personal data in publications
- Obtain institutional review board approval

Technical Specifications:
- Python 3.8+ environment
- Required libraries: requests, pandas, datetime
- UTF-8 encoding for Chinese text
- Secure data storage protocols

6. Academic Application

This framework supports research in:
- Computational social science
- Natural language processing  
- Digital humanities
- Social network analysis
- Public opinion research

When using this methodology, cite the framework and maintain transparency about data collection procedures in publications.

Manual Weibo Comment Collection Protocol

Data Collection Procedure

Phase 1: Advanced Search Setup
1. Access Platform
   - Navigate to: `https://s.weibo.com`
   - Click "Advanced Search" (高级搜索)

2. Configure Search Parameters
   - Keywords: "毕业生就业" (Graduate Employment)
   - Time Range: Set appropriate date boundaries
   - Content Type: Select "All" or "Original" based on research needs
   - Region: Optional geographic filtering

Phase 2: Content Identification
3. Identify Target Content
   - Sort results by "Hot" (热门) to find high-engagement posts
   - Look for posts with substantial comment volumes
   - Prioritize posts with recent activity timestamps
   - Select 10-20 representative posts for analysis

Phase 3: Manual Data Extraction
4. Comment Collection Process
   - Click on comment count to enter comment section
   - Scroll to load additional comments (incremental loading)
   - Select and copy comment text using:
     - `Ctrl+A` → `Ctrl+C` (select all and copy)
     - Or manual selection of individual comments
   - Paste content into structured document

Phase 4: Data Organization
5. Structured Storage Format
```
Post_ID: [Weibo ID]
Post_Content: [Original text]
Collection_Date: [YYYY-MM-DD]
Comment_Data:
1. [Comment text] | [Username] | [Timestamp]
2. [Comment text] | [Username] | [Timestamp]
3. [Comment text] | [Username] | [Timestamp]
```

Quality Control Measures

Data Validation
- Verify comment timestamps are within research period
- Ensure complete text capture (check for truncation)
- Document source URLs for reference
- Record collection date and time

Ethical Considerations
- Collect only publicly available content
- Anonymize usernames in final dataset
- Exclude personal identification information
- Respect platform terms of service

Advantages of Manual Collection

Research Benefits:
- Direct quality control of data
- Contextual understanding of content
- Flexible adaptation to research needs
- No technical barriers for implementation

Methodological Strengths:
- Suitable for small-scale qualitative studies
- Ideal for pilot research and methodology development
- Compatible with content analysis frameworks
- Provides ground truth for automated methods validation

Recommended Scale
- Small Studies: 200-500 comments
- Medium Studies: 500-2,000 comments  
- Large Studies: Consider automated approaches

This manual protocol ensures data quality and contextual understanding while maintaining ethical research standards.
