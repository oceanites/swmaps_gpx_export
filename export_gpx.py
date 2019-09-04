import argparse
import sqlite3
from collections import namedtuple
from datetime import datetime
from typing import List, Tuple, Dict, Mapping, Sequence

import gpxpy
import gpxpy.gpx

Point = namedtuple("Point", "lat lon elevation time speed")


def load_track_name(sqlite_db: str) -> Dict[str, str]:
    db = sqlite3.connect(sqlite_db)
    cur = db.cursor()
    tracks = cur.execute("SELECT uuid, name FROM tracks").fetchall()
    tracks = {t[1]: t[0] for t in tracks}
    print(f"Found {len(tracks)} tracks in database.")
    return tracks


def load_points_from_sqlite(sqlite_db: str, track_names: Dict[str, str]) -> Dict[str, List]:
    """
    Tracks[Dict[Name, Points[lat, lon elv, time, speed]]
    """
    points = dict()
    db = sqlite3.connect(sqlite_db)
    cur = db.cursor()
    for track_name in track_names.keys():
        track_id = track_names[track_name]
        query = f"SELECT lat, lon, elv, time, speed FROM points WHERE fid = ?"
        track = cur.execute(query, (track_id,)).fetchall()
        points[track_name] = track

    return points


def create_gpx(tracks: Mapping[str, Sequence]):
    gpx = gpxpy.gpx.GPX()

    for name, track in tracks.items():
        gpx_track = gpxpy.gpx.GPXTrack(name=name)
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        for point in track:
            t = point[3]
            # '%Y-%m-%d %H:%M:%S.%f'
            t = datetime.utcfromtimestamp(t / 1000)
            gpx_segment.points.append(
                gpxpy.gpx.GPXTrackPoint(point[0], point[1], elevation=point[2], time=t,
                                        speed=point[4]))

    xml = gpx.to_xml()
    return xml


def sqlite2gpx(sqlite_db: str, output_gpx: str):
    track_names = load_track_name(sqlite_db)
    tracks = load_points_from_sqlite(sqlite_db, track_names)
    gpx = create_gpx(tracks)
    with open(output_gpx, "w") as gpx_file:
        gpx_file.writelines(gpx)
        print(f"Wrote GPX to {output_gpx}.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str,
                        help="Input SW Maps project SQLite database (ending: .swm2)")
    parser.add_argument("output", type=str, help="Ouput GPX path.")
    args = parser.parse_args()

    sqlite2gpx(args.input, args.output)
