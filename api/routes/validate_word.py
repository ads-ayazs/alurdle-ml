from crypt import methods
from flask import Blueprint, request
from models.validate_word import is_valid_word

blueprint = Blueprint('api', __name__, url_prefix='/validate')

@blueprint.route('/<string:try_word>', methods=['GET'])
def respond(try_word):
    if request.method == "GET":
      result = is_valid_word(try_word=try_word)

      return {
        f'{try_word}': f'{result}'
      }
