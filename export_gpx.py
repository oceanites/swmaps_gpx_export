import sqlite3
from collections import namedtuple
from datetime import datetime
from typing import List

import gpxpy
import gpxpy.gpx

Point = namedtuple("Point", "lat lon elevation time speed")


def load_points_from_sqlite(sqlite_db: str) -> List[List]:
    """
    Tracks[Points[lat, lon elv, time, speed]
    """
    points = list()
    db = sqlite3.connect(sqlite_db)
    cur = db.cursor()
    fids = cur.execute("SELECT DISTINCT fid FROM points").fetchall()
    fids = [fid[0] for fid in fids]
    for fid in fids:
        query = f"SELECT lat, lon, elv, time, speed FROM points WHERE fid = ?"
        track = cur.execute(query, (fid,)).fetchall()
        points.append(track)

    print(f"Found {len(fids)} tracks in database.")
    return points


def create_gpx(tracks):
    gpx = gpxpy.gpx.GPX()

    for track in tracks:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        for point in track:
            t = point[3]
            # '%Y-%m-%d %H:%M:%S.%f'
            t = datetime.utcfromtimestamp(t/1000)
            gpx_segment.points.append(
                gpxpy.gpx.GPXTrackPoint(point[0], point[1], elevation=point[2], time=t,
                                        speed=point[4]))

    xml = gpx.to_xml()
    return xml


def sqlite2gpx(sqlite_db: str):
    outfile = "/tmp/tracks.gpx"
    tracks = load_points_from_sqlite(sqlite_db)
    gpx = create_gpx(tracks)
    with open(outfile, "w") as gpx_file:
        gpx_file.writelines(gpx)
        print(f"Wrote GPX to {outfile}.")