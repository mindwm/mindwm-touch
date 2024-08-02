from cloudevents.http import CloudEvent
from parliament import Context
import random

import unittest

func = __import__("func")

class TestFunc(unittest.TestCase):

  def test_func(self):
    # Create a CloudEvent
    # - The CloudEvent "id" is generated if omitted. "specversion" defaults to "1.0".
    traceId = ''.join(random.choice('0123456789abcdef') for n in range(32))
    spanId = ''.join(random.choice('0123456789abcdef') for n in range(16))
    attributes = {
        "type": "dev.knative.function",
        "source": "https://knative.dev/python.event",
        "traceparent": f"00-{traceId}-{spanId}-01",
    }
    data = {"message": "Hello World!"}
    event = CloudEvent(attributes, data)
    context = Context(req=None)
    context.cloud_event = event

    body = func.main(context)
    self.assertEqual(body.data,  event.data)

if __name__ == "__main__":
  unittest.main()
