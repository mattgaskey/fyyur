from flask import current_app

def add_to_index(index, model):
  if not current_app.elasticsearch:
    return
  payload = {}
  for field in model.__searchable__:
    payload[field] = getattr(model, field)
  current_app.elasticsearch.index(index=index, id=model.id, body=payload)

def remove_from_index(index, model):
  if not current_app.elasticsearch:
    return
  current_app.elasticsearch.delete(index=index, id=model.id)

def query_index(index, query):
  if not current_app.elasticsearch:
    return [], 0
  search = current_app.elasticsearch.search(
    index=index,
    body={
      'query': {
        'bool': {
          'should': [
            {'match': {'name': {'query': query, 'fuzziness': 'AUTO'}}},
            {'wildcard': {'name': f'*{query}*'}}
          ]
        }
      }
    }
  )
  ids = [int(hit['_id']) for hit in search['hits']['hits']]
  return ids, search['hits']['total']['value']