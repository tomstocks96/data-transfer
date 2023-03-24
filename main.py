import json

import faust
from timing_parser.timing_parser import TimingParser

app = faust.App('tsl-lap-processor', broker='kafka://kafka:29092')
consume_topic = app.topic('tsl-monitor-timings')
produce_topic = app.topic('tsl-monitor-laps')

timing_parser = TimingParser()


@app.agent(consume_topic)
async def data_type_unify(messages):
    async for message in messages:
        message = timing_parser.parse_message(message)
        await produce_topic.send(value=json.dumps(message))

if __name__ == '__main__':
    app.main()