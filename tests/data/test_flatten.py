import pytest

# from data.flatten import *
from data.flatten import player_game_dyndb_to_s3

def test_player_game_dyndb_to_s3():
  tests = [
    # TEST Empty params
    { 
      'kwargs': {},
      'result': [
        's3://ads-datasets/wordle-player/flat/game-turns.csv',
        's3://ads-datasets/wordle-player/parquet/game-turns.parquet',
        's3://ads-datasets/wordle-player/flat/valid-word-attempts.csv',
        's3://ads-datasets/wordle-player/parquet/valid-word-attempts.parquet',
      ],
    },
    # TEST Default params
    { 
      'kwargs': {
        'table_name': 'PlayerGame', 
        'attr_list': ['turns', 'gameId'], 
        'out_bucket_path': 's3://ads-datasets/wordle-player', 
      },
      'result': [
        's3://ads-datasets/wordle-player/flat/game-turns.csv',
        's3://ads-datasets/wordle-player/parquet/game-turns.parquet',
        's3://ads-datasets/wordle-player/flat/valid-word-attempts.csv',
        's3://ads-datasets/wordle-player/parquet/valid-word-attempts.parquet',
      ],
    }
  ]

  for test in tests:
    # Grab test params
    kwargs = test.get('kwargs', {})
    result = test.get('result', None)

    # Call function
    retval = player_game_dyndb_to_s3(**kwargs)

    # Compare return value with expected
    assert(len(retval) == len(result))
    assert(set(retval) == set(result))
