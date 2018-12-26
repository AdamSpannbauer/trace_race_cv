import argparse
from trace_race import TraceRace

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--width", default=500, type=int,
                help='Display width')
ap.add_argument("-c", "--color", default="pink",
                help="Crayon color. Options: ['blue', 'green', 'pink', 'red', 'yellow']")
args = vars(ap.parse_args())

# set up and play trace race
my_trace_race = TraceRace(crayon_color=args["color"], frame_width=args["width"])
my_trace_race.play()
