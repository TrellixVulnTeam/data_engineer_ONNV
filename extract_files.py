import gzip
import json
import os
import shutil
import tarfile
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
from uuid import uuid4
from ua_parser import user_agent_parser

ROOT_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'
TARFILE_PATH = ROOT_PATH + 'ds-devtask-events.tar'
EVENTS_PATH = ROOT_PATH + 'events'


@dataclass
class BrowserRecorderEventsRecorded:
    uuid: str
    test_case_id: str
    browser: Optional[str]
    device: Optional[str]
    starting_url: str
    event_type: str
    timestamp: str
    operating_system: Optional[str]


def export_proper_events():
    events = []
    browser_metadata = {}
    system_data = {}

    for payload in serialize_files_to_json():
        metadata = payload['properties']['metadata']
        if not payload['properties'].get('events'):
            print(payload)
            system_data[metadata['test_case_id']] = (
                payload['properties']['device_data']['operating_system']
            )
            continue

        for event in payload['properties']['events']:
            test_case_id = metadata['test_case_id']
            if event['type'] == 'pageLoaded':
                browser_metadata[test_case_id] = event['userAgent']
            created_at = datetime.fromtimestamp(
                event['timestamp'] / 1000.0
            ).isoformat()

            events.append(BrowserRecorderEventsRecorded(
                uuid=str(uuid4()), test_case_id=test_case_id, browser=None,
                device=None, starting_url=metadata['starting_url'],
                event_type=event['type'], timestamp=created_at, operating_system=None,
            ))

    _parse_user_agents(events, browser_metadata)
    for event in events:
        event.operating_system = system_data.get(event.test_case_id, '')
    print(system_data)
    with open(ROOT_PATH + 'serialized_events.json', 'w') as outfile:
        json.dump([asdict(event) for event in events], outfile)


def _parse_user_agents(events, browser_metadata):
    """Populate missing browser metadata using user agent from other event."""
    for event in events:
        parsed_ua = user_agent_parser.Parse(browser_metadata[event.test_case_id])
        event.browser = parsed_ua['user_agent']['family']
        event.device = parsed_ua['device']['family']


def extract_files(tarfile_path=TARFILE_PATH):
    with tarfile.open(tarfile_path) as datafile:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(datafile)
    for file_ in find_files('.gz'):
        with gzip.open(file_, 'rb') as infile:
            txt_file = file_.replace('.gz', '.txt')
            with open(txt_file, 'wb') as outfile:
                shutil.copyfileobj(infile, outfile)


def serialize_files_to_json():
    """
    Make extracted files json serializable and
    export them to json readable format.
    """
    serialized_jsons = []
    txt_files = find_files('.txt')
    for file_ in txt_files:
        with open(file_, 'rb') as infile:
            contents = infile.readlines()
            for json_payload in contents:
                serialized_jsons.append(json.loads(json_payload))

    with open(ROOT_PATH + 'raw_events_data.json', 'w') as outfile:
        json.dump([data for data in serialized_jsons], outfile)

    return serialized_jsons


def find_files(file_type, path=EVENTS_PATH):
    """Find and return list of files for given type in given path."""
    type_files = []
    for root, _, files in os.walk(path):
        for file_ in files:
            if file_type in file_:
                type_files.append(os.path.join(root, file_))

    return type_files


if __name__ == '__main__':
    export_proper_events()
