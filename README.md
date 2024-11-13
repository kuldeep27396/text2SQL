# Natural Language to BigQuery SQL Converter

This project is just what I haved presented in one of the hackathon and wrote a white paper on this. This is still in progress but idea is the same.

## Features

- 🤖 Natural language to SQL conversion using GPT-4
- 📊 Direct BigQuery integration
- 🔄 Automatic retry mechanism for API calls
- 📝 Comprehensive logging
- ⚡ Type hints for better IDE support
- 🔧 YAML-based configuration
- 🛡️ Error handling and validation

## Prerequisites

- Python 3.8+
- Google Cloud account with BigQuery access
- OpenAI API key
- Google Cloud service account credentials with BigQuery permissions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nl-to-bigquery-sql.git
cd nl-to-bigquery-sql
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install google-cloud-bigquery openai pyyaml
```

## Configuration

1. Create a `config.yaml` file in the project root:
```yaml
bigquery:
  project_id: "bigquery-public-data"  # or your project
  dataset_id: "samples"
  table_name: "shakespeare"
  credentials_path: "path/to/your/credentials.json"

openai:
  api_key: "your-openai-api-key"
  model: "gpt-4"
  temperature: 0.1
  max_tokens: 500

table_metadata:
  description: "Table description"
  schema:
    - name: "column_name"
      type: "STRING"
      description: "Column description"
```

2. Set up Google Cloud credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a project or select existing one
   - Enable BigQuery API
   - Create a service account
   - Download JSON credentials
   - Update `credentials_path` in config.yaml

3. Set up OpenAI API:
   - Get an API key from [OpenAI Platform](https://platform.openai.com)
   - Update `api_key` in config.yaml

## Usage

### Basic Usage

```python
from nl_to_sql_bigquery import NLToSQLBigQuery, BigQueryConfig, OpenAIConfig, load_config

# Load configuration
config = load_config('config.yaml')

# Create configuration objects
bq_config = BigQueryConfig(
    project_id=config['bigquery']['project_id'],
    dataset_id=config['bigquery']['dataset_id'],
    table_name=config['bigquery']['table_name'],
    credentials_path=config['bigquery'].get('credentials_path')
)

openai_config = OpenAIConfig(
    api_key=config['openai']['api_key'],
    model=config['openai'].get('model', 'gpt-4')
)

# Initialize the converter
converter = NLToSQLBigQuery(
    bq_config=bq_config,
    openai_config=openai_config,
    metadata=config['table_metadata']
)

# Process a natural language query
results = converter.process_natural_language_query(
    "Show me the top 10 customers by revenue"
)
```

### Example Queries

Using the Shakespeare public dataset:

```python
# Example queries
queries = [
    "What are the top 10 most frequent words in all of Shakespeare's works?",
    "Show me the total word count for each corpus, ordered by date",
    "Find all works that contain the word 'love' more than 100 times"
]

for query in queries:
    results = converter.process_natural_language_query(query)
    print(f"\nQuery: {query}")
    print(f"SQL: {results['sql_query']}")
    print(f"Results: {results['results']}")
```

## Public Dataset Examples

### Shakespeare Dataset
```yaml
bigquery:
  project_id: "bigquery-public-data"
  dataset_id: "samples"
  table_name: "shakespeare"
```

### London Bicycles Dataset
```yaml
bigquery:
  project_id: "bigquery-public-data"
  dataset_id: "london_bicycles"
  table_name: "cycle_hire"
```

### New York Citibike Dataset
```yaml
bigquery:
  project_id: "bigquery-public-data"
  dataset_id: "new_york_citibike"
  table_name: "citibike_trips"
```

## Error Handling

The code includes comprehensive error handling:

```python
try:
    results = converter.process_natural_language_query(query)
except ConfigurationError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Error processing query: {e}")
```

## Logging

Logs are automatically generated with timestamps and log levels:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **BigQuery Authentication Error**
   - Ensure credentials path is correct
   - Verify service account has proper permissions
   - Check if BigQuery API is enabled

2. **OpenAI API Error**
   - Verify API key is correct
   - Check API quota and limits
   - Ensure proper network connectivity

3. **Query Generation Issues**
   - Try providing more context in table metadata
   - Adjust temperature setting in OpenAI config
   - Make natural language query more specific

### Getting Help

- Open an issue in the GitHub repository
- Check the logs for detailed error messages
- Refer to the [BigQuery documentation](https://cloud.google.com/bigquery/docs)
- Consult the [OpenAI API documentation](https://platform.openai.com/docs)

## Best Practices

1. **Security**
   - Never commit API keys or credentials
   - Use environment variables for sensitive data
   - Regularly rotate API keys

2. **Performance**
   - Cache frequently used queries
   - Implement proper error handling
   - Use appropriate timeout values

3. **Maintenance**
   - Keep dependencies updated
   - Monitor API usage
   - Review and update table metadata regularly
