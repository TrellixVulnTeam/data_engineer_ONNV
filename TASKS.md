## Tasks

1. Get familiar with the data structure in this repository.
2. Right now it is impossible to parse these files using JSON parser. Transform these files into JSON-parseable format.
3. Right now browser events are bundled into a higher-order event type called BrowserRecorderEventsRecorded. Extract these browser events, strip all unnecessary information from them and for every test case id provide browser & device metadata inside every browser event (if not ambiguous). You can find browser & device metadata in a different type of event. Maintain time information inside event payload. The resulting file should be JSON-parseable list of browser events (you can use BrowserEventRecorded "event" type as a name for new events). **Please note that information about browser & device metadata may be located inside another file!**
4. Transform dataset: group events by test case ID and order them into one, linear stream of events.
5. Transform dataset: group events by starting URL and order them into one, linear stream of events.
6. In 4 & 5 you've ordered events using a timestamp. What timestamp have you used and why?
7. Prepare a small report about how many events have been gathered for every starting URL in the dataset and every test case ID in the dataset. You should use some chart library (like matplotlib) to present results. You can also use Jupyter Notebooks. Make the solution generic enough to support recalculation of this report as new data arrives.
8. (Optional) Generate [Parquet](https://parquet.apache.org/) representation of grouped representations of files to make it [Athena](https://aws.amazon.com/athena/)-indexable.
