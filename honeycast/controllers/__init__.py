from collections import namedtuple

Message = namedtuple("Message", ["source_id", "destination_id", "namespace", "data"])
