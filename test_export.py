import os

import pytest

import export_gpx
from export_gpx import Point


@pytest.fixture
def sqlite_db():
    return "./TrackTest.swm2"


@pytest.fixture
def tracks():
    track1 = [Point(2, 2, 100, 20, 0), Point(2, 3, 200, 25, 0)]
    track2 = [Point(5, 3, 1000, 20.34, 0), Point(5, 4, 2000, 25, 0)]
    return [track1, track2]


def test_load_points(sqlite_db):
    tracks = export_gpx.load_points_from_sqlite(sqlite_db)
    assert tracks is not None
    assert len(tracks) == 2
    assert len(tracks[1]) == 9
    assert len(tracks[0]) == 54


def test_create_gpx(tracks):
    xml = export_gpx.create_gpx(tracks)
    # TODO


def test_sqlite2gpx(sqlite_db):
    outfile = "/tmp/delme.gpx"  # TODO use tempfile
    export_gpx.sqlite2gpx(sqlite_db, outfile)
    assert os.path.isfile(outfile)
    assert os.path.getsize(outfile) >= 5 * 1024  # should not be empty
