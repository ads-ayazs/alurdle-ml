import awswrangler as wr
import pytest


# from data.flatten import *
from data.flatten import player_game_dyndb_to_s3

def test_player_game_dyndb_to_s3():
  tests = [
    # TEST Empty params
    { 
      'kwargs': {},
      'result': [
        's3://ads-datasets/wordle-player/parquet/game-turns/game-turns.parquet',
        's3://ads-datasets/wordle-player/parquet/valid-word-attempts/valid-word-attempts.parquet',
      ],
      'cleanup': []
    },
    # TEST 1 Default params
    { 
      'kwargs': {
        'table_name': 'PlayerGame', 
        'out_bucket_path': 's3://ads-datasets/test-out/1', 
      },
      'result': [
        's3://ads-datasets/test-out/1/game-turns/game-turns.parquet',
        's3://ads-datasets/test-out/1/valid-word-attempts/valid-word-attempts.parquet',
      ],
      'cleanup': [
        's3://ads-datasets/test-out/1'
      ]
    },
  ]

  for test in tests:
    # Grab test params
    kwargs = test.get('kwargs', {})
    result = test.get('result', None)
    cleanup = test.get('cleanup', [])

    # Cleanup from previous test run
    for fpath in cleanup:
      wr.s3.delete_objects(fpath)

    # Call function
    retval = player_game_dyndb_to_s3(**kwargs)

    # Compare return value with expected
    assert(len(retval) == len(result))
    assert(set(retval) == set(result))

    # Verify that the output files exist
    for fpath in retval:
      assert(wr.s3.does_object_exist(fpath))
  