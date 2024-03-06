# tests/test_iocs.py

import json
import pytest
from typer.testing import CliRunner

from ioc_storage import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__,
    __version__,
    cli,
    ioc_storage
)


runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


@pytest.fixture
def mock_json_file(tmp_path):
    ioc = [{'link': 'http://example.com', 'source': 'example'}]
    db_file = tmp_path / 'ioc.json'
    with db_file.open('w') as db:
        json.dump(ioc, db, indent=4)
    return db_file


test_data1 = {
    "link": 'http://example1.com',
    'source': 'example1',
    "ioc": {
        "link": 'http://example1.com',
        'source': 'example1',
    },
}

test_data2 = {
    "link": 'http://example2.com',
    'source': 'example2',
    "ioc": {
        "link": 'http://example2.com',
        'source': 'example2',
    },
}


@pytest.mark.parametrize(
    'link, source, expected',
    [
        pytest.param(
            test_data1['link'],
            test_data1['source'],
            (test_data1['ioc'], SUCCESS)
        ),
        pytest.param(
            test_data2['link'],
            test_data2['source'],
            (test_data2['ioc'], SUCCESS)
        )
    ]
)
def test_add(mock_json_file, link, source, expected):
    iocer = ioc_storage.IOCer(mock_json_file)
    assert iocer.add(link, source) == expected
    read = iocer._db_handler.read_iocs()
    assert len(read.ioc_list) == 2
