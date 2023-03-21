
import faust
from timing_parser.timing_parser import TimingParser

app = faust.App('myapp', broker='kafka://localhost:29092')
topic = app.topic('tsl-monitor-timings')

timing_parser = TimingParser()

@app.agent(topic)
async def consolidate(messages):
    async for message in messages:
        timing_parser.parse_message(message)


if __name__ == '__main__':
    app.main()