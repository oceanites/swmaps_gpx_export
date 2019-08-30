import pytest

import export_gpx
from export_gpx import Point


@pytest.fixture
def sqlite_db():
    return "/home/thomas/ocell/Terrestrische Datenaufnahme/swmaps_gpx_export/Project 1.swm2"


@pytest.fixture
def tracks():
    track1 = [Point(2, 2, 100, 20, 0), Point(2, 3, 200, 25, 0)]
    track2 = [Point(5, 3, 1000, 20.34, 0), Point(5, 4, 2000, 25, 0)]
    return [track1, track2]


def test_load_points(sqlite_db):
    tracks = export_gpx.load_points_from_sqlite(sqlite_db)
    assert tracks is not None
    assert len(tracks) == 5
    sum = 0
    for track in tracks:
        sum += len(track)
    assert sum == 299


def test_create_gpx(tracks):
    xml = export_gpx.create_gpx(tracks)
    # TODO

def test_sqlite2gpx(sqlite_db):
    export_gpx.sqlite2gpx(sqlite_db)