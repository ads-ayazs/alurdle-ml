import awswrangler as wr
import os
import pandas as pd


# Constants
DYNDB_TABLE_NAME = 'PlayerGame'
DYNDB_TABLE_ATTRIBUTES = ['turns', 'gameId']
DYNDB_SCAN_LIMIT=1000

S3_BUCKET_PATH="s3://ads-datasets/wordle-player"
S3_FLD_CSV="flat"
S3_FLD_PQT="parquet"

FILENAME_GAMETURNS_CSV = "game-turns.csv"
FILENAME_GAMETURNS_PQT = "game-turns.parquet"
FILENAME_VALIDWORDATTEMPTS_CSV = "valid-word-attempts.csv"
FILENAME_VALIDWORDATTEMPTS_PQT = "valid-word-attempts.parquet"


def player_game_dyndb_to_s3(
  table_name=DYNDB_TABLE_NAME, 
  attr_list=DYNDB_TABLE_ATTRIBUTES,
  out_bucket_path = S3_BUCKET_PATH):

  """Flatten PlayerGame JSON data from DynamoDB into CSV and parquet on S3.

  Args:
      table_name(str): Source table name in DynamoDB.
      attr_list(array of str): Names of attributes to select from the source table.
      out_bucket_path: Path to the S3 bucket where output files will be written.

  Returns:
      filenames(array of str): List of files written in S3.
  """

  out_files = []

  # Validate input variables
  if not table_name:
    return out_files
  if not attr_list:
    return out_files
  if not out_bucket_path:
    return out_files

  # Get the DynDB table
  tbl = wr.dynamodb.get_table(table_name=DYNDB_TABLE_NAME)
  if tbl.item_count < 1:
    return out_files

  # Sample only the attributes that we want to extract
  try:
    resp = tbl.scan(
        Select='SPECIFIC_ATTRIBUTES', 
        AttributesToGet=attr_list, 
        Limit=DYNDB_SCAN_LIMIT,
    )
  except:
    return out_files

  # Normalize the data (shallow)
  items = resp["Items"]
  df = pd.json_normalize(items)

  # Write the turn data to s3
  try:
    s3_file_path = os.path.join(out_bucket_path, S3_FLD_CSV, FILENAME_GAMETURNS_CSV)
    result = wr.s3.to_csv(df, s3_file_path, index=False)
    out_files.extend(result['paths'])

    s3_file_path = os.path.join(out_bucket_path, S3_FLD_PQT, FILENAME_GAMETURNS_PQT)
    result = wr.s3.to_parquet(df, s3_file_path)
    out_files.extend(result['paths'])
  except:
    pass

  # Normalize the data into the columns that we want to extract
  df = pd.json_normalize(items, record_path=['turns'], meta=['gameId'], errors='ignore')
  df = df.drop(columns=['tryResult'])

  # Write the turn data to s3
  try:
    s3_file_path = os.path.join(out_bucket_path, S3_FLD_CSV, FILENAME_VALIDWORDATTEMPTS_CSV)
    result = wr.s3.to_csv(df, s3_file_path, index=False)
    out_files.extend(result['paths'])

    s3_file_path = os.path.join(out_bucket_path, S3_FLD_PQT, FILENAME_VALIDWORDATTEMPTS_PQT)
    result = wr.s3.to_parquet(df, s3_file_path)
    out_files.extend(result['paths'])
  except:
    pass

  return out_files

####

if __name__ == '__main__':
  files_written = player_game_dyndb_to_s3()
  for f in files_written:
    print(f)