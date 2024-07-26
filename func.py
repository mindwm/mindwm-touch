import os
import sys
import re
sys.path.append(os.path.abspath('mindwm-sdk-python/neomodel'))
sys.path.append(os.path.abspath('mindwm-sdk-python/'))

from parliament import Context, event

import neomodel_data
import MindWM
import pprint

from cloudevents.http import from_http
from cloudevents import abstract, conversion
from neomodel import db




@event
def main(context: Context):

    event = from_http(context.request.headers, context.request.data)
    te = MindWM.TouchEvent.from_json(conversion.to_json(event))

    update_query = f"""
    MATCH (n)
    WHERE ID(n) IN {te.data.ids}
    CALL apoc.path.expandConfig(n, {{
      relationshipFilter: "<",
      minLevel: 1,
      bfs: true
    }}) YIELD path
    UNWIND nodes(path) as node
    UNWIND relationships(path) as r
    SET node.atime = timestamp()
    SET r.atime = timestamp()
    RETURN DISTINCT node, r
    """
    pprint.pprint(update_query)
    pprint.pprint(db.cypher_query(update_query), stream=sys.stderr)


    return "", 200
