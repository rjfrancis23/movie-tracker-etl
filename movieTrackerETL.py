import os
from google.cloud import storage
import yaml
import requests
import pandas as pd
from google.cloud import bigquery

os.environ["GCLOUD_PROJECT"] = "upheld-now-404615"

with open('config.yml') as config:
    api_vars = yaml.safe_load(config)

def get_trending_data():
    headers = {
    'Content-Type': api_vars['content_type'],
    'trakt-api-version': api_vars['trakt_api_version'], 
    'trakt-api-key': api_vars['trakt_api_key']
    }

    response = requests.get(api_vars['trakt_url'], headers=headers).json()

    df = pd.DataFrame.from_dict(response)
    trending = pd.concat([df[['watchers']], pd.json_normalize(df['movie'])], axis=1)
    # watchers	title	year	tagline	overview	released	runtime	country	trailer	homepage	status	rating	votes	comment_count	updated_at	language	available_translations	genres	certification	ids.trakt	ids.slug	ids.imdb	ids.tmdb
    trending = trending[['watchers','title','year','runtime','rating','genres','certification','ids.trakt','ids.slug','ids.imdb','ids.tmdb']]
    trending.rename(columns={"ids.trakt": "ids_trakt", "ids.slug": "ids_slug", "ids.imdb": "ids_imdb", "ids.tmdb": "ids_tmdb"}, inplace=True)

    return trending

def upload_trending_data(bucket_name, source_file_name, destination_blob_name):
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)

  blob.upload_from_filename(source_file_name)

  print('File {} uploaded to {}.'.format(
      source_file_name,
      destination_blob_name))

def load_big_query(uri):
    # Construct a BigQuery client object.
    client = bigquery.Client()

    table_id = "upheld-now-404615.trending_movies.top_20_movies"

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField('watchers','INT64'),
            bigquery.SchemaField('title','STRING'),
            bigquery.SchemaField('year','INT64'),
            bigquery.SchemaField('runtime','INT64'),
            bigquery.SchemaField('rating','FLOAT64'),
            bigquery.SchemaField('genres',field_type='STRING', mode='REPEATED'),
            bigquery.SchemaField('certification','STRING'),
            bigquery.SchemaField('ids_trakt','INT64'),
            bigquery.SchemaField('ids_slug','STRING'),
            bigquery.SchemaField('ids_imdb','STRING'),
            bigquery.SchemaField('ids_tmdb','INT64')
        ],
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    uri = uri

    load_job = client.load_table_from_uri(
        uri,
        table_id,
        location="US",  # Must match the destination dataset location.
        job_config=job_config,
    )  # Make an API request.


    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)  # Make an API request.
    print("Loaded {} rows.".format(destination_table.num_rows))

trending = get_trending_data()
trending.to_json('trending.json', orient = 'records', lines=True)
upload_trending_data('test-bucket-franjoy23', 'trending.json', 'test-trending')
load_big_query('gs://test-bucket-franjoy23/test-trending')