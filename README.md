# Trace Race CV

<p align='center'>
  <img src='readme/trace_race_mp.png' width=30%>
</p>

A computer vision based version of the Mario Party mini-game 'Trace Race' (pictured below).  Game will implement object tracking for players to choose how they want to trace the course.

<p align='center'>
  <img src='readme/trace_race_example.gif' width=50%>
</p>

## Installation

* Clone repo and navigate to trace_race_cv directory

```bash
$ git clone https://github.com/AdamSpannbauer/trace_race_cv.git
$ cd trace_race_cv.git
```

* Install trace_race package

```bash
$ pip3 install .
```

*If you don't already have OpenCV installed, install with below command.*

```bash
$ pip3 install opencv-contrib-python
```

## Usage

* Execute `play_trace_race.py`

```bash
$ python3 play_trace_race.py
```

*Optionally add crayon color choice*

```bash
$ python3 play_trace_race.py --color blue
```
