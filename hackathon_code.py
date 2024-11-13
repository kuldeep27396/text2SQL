import os
from typing import Dict, Any
import json
from nl_to_sql_bigquery import NLToSQLBigQuery, BigQueryConfig, OpenAIConfig, load_config

def main():
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
        model=config['openai'].get('model', 'gpt-4'),
        temperature=config['openai'].get('temperature', 0.1),
        max_tokens=config['openai'].get('max_tokens', 500)
    )
    
    # Initialize the converter
    converter = NLToSQLBigQuery(
        bq_config=bq_config,
        openai_config=openai_config,
        metadata=config['table_metadata']
    )
    
    # Example queries to try
    example_queries = [
        "What are the top 10 most frequent words in all of Shakespeare's works?",
        "Show me the total word count for each corpus, ordered by date",
        "Find all works that contain the word 'love' more than 100 times",
    ]
    
    # Process each query
    for query in example_queries:
        print(f"\nProcessing query: {query}")
        try:
            results = converter.process_natural_language_query(query)
            print("\nGenerated SQL:")
            print(results['sql_query'])
            print("\nResults:")
            print(json.dumps(results['results'], indent=2)[:1000])  # Truncating for readability
        except Exception as e:
            print(f"Error processing query: {str(e)}")

if __name__ == "__main__":
    main()
