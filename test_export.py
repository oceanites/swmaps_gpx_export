import os
import xml.etree.ElementTree as ET
import pytest

import export_gpx
from export_gpx import Point


@pytest.fixture
def sqlite_db():
    return "./TrackTest.swm2"


@pytest.fixture
def tracks():
    track = dict()
    track["Track1"] = [Point(2, 2, 100, 20, 0), Point(2, 3, 200, 25, 0)]
    track["Track2"] = [Point(5, 3, 1000, 20.34, 0), Point(5, 4, 2000, 25, 0)]
    return track


@pytest.fixture
def track_names(sqlite_db):
    track_names = export_gpx.load_track_name(sqlite_db)
    return track_names


def test_load_track_name(sqlite_db):
    names = export_gpx.load_track_name(sqlite_db)
    assert len(names) == 2
    assert all([n.startswith("Track") for n in names.keys()])


def test_load_points(sqlite_db, track_names):
    tracks = export_gpx.load_points_from_sqlite(sqlite_db, track_names)
    assert tracks is not None
    assert len(tracks) == 2
    assert len(tracks["Track3"]) == 9
    assert len(tracks["Track2"]) == 54


def test_create_gpx(tracks):
    gpx = export_gpx.create_gpx(tracks)
    assert gpx is not None
    # test if valid xml/gpx is produced
    parsed = ET.fromstring(gpx)
    assert parsed is not None


def test_sqlite2gpx(sqlite_db):
    outfile = "/tmp/delme.gpx"  # TODO use tempfile
    export_gpx.sqlite2gpx(sqlite_db, outfile)
    assert os.path.isfile(outfile)
    assert os.path.getsize(outfile) >= 5 * 1024  # should not be empty
