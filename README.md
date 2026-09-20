# Guitar Tuner

![CI](https://github.com/yavuzselimsert/gitar-frekans/actions/workflows/ci.yml/badge.svg)

A real-time guitar tuner built in Python using digital signal processing techniques.

The project analyzes live audio from a microphone or audio interface, estimates the fundamental frequency of a guitar note using the **YIN algorithm**, and calculates the pitch deviation in **cents** to provide real-time tuning feedback.

> A small DSP project exploring the intersection of music, signal processing, and software.

## Features

* 🎸 Real-time guitar pitch detection
* 🎯 Automatic detection of the nearest standard-tuning string
* 📊 Pitch deviation displayed in cents
* 📟 Terminal-based tuner interface
* 🎙️ Support for microphones and external audio interfaces
* 🔌 Configurable audio input device
* 🧮 Theoretical guitar frequency and note calculator

## Demo

The tuner runs directly in the terminal and provides real-time pitch feedback.

## How It Works

The tuner processes incoming audio in short blocks and estimates the fundamental frequency of the guitar signal using the **YIN pitch detection algorithm**.

The detected frequency is then compared with the target frequency of the nearest guitar string.

Pitch deviation is calculated in cents using:

```text
cents = 1200 × log₂(f / f₀)
```

where:

* `f` is the detected frequency
* `f₀` is the target frequency

A deviation of:

* `0 cents` → perfectly in tune
* `-100 cents` → one semitone flat
* `+100 cents` → one semitone sharp

## Standard Tuning

| String | Note | Frequency |
| ------ | ---- | --------: |
| 6th    | E2   |  82.41 Hz |
| 5th    | A2   | 110.00 Hz |
| 4th    | D3   | 146.83 Hz |
| 3rd    | G3   | 196.00 Hz |
| 2nd    | B3   | 246.94 Hz |
| 1st    | E4   | 329.63 Hz |

## Project Structure

```text
gitar-frekans/
├── gitar.py
├── tuner.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `gitar.py`

Calculates the theoretical frequency and note name for a given guitar string and fret.

### `tuner.py`

Captures live audio, estimates the fundamental frequency using YIN, identifies the nearest guitar string, and displays the tuning deviation.

## Installation

### Requirements

* Python 3.10+
* A microphone or audio interface
* Electric guitar

Clone the repository:

```bash
git clone https://github.com/yavuzselimsert/gitar-frekans.git
cd gitar-frekans
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Frequency Calculator

Run:

```bash
python gitar.py
```

Enter a string number (`1–6`) and fret number (`0–24`) to calculate the corresponding note and theoretical frequency.

### Real-Time Tuner

Run:

```bash
python tuner.py
```

The program will list available audio input devices. Select the input connected to your guitar or audio interface.

The tuner will then continuously analyze the incoming signal.

Press `Ctrl+C` to exit.

## Technical Details

### YIN Pitch Detection

The tuner uses the YIN algorithm for fundamental frequency estimation.

The implementation includes:

1. Difference function
2. Cumulative Mean Normalized Difference Function (CMNDF)
3. Threshold-based period selection
4. Parabolic interpolation for improved frequency estimation

This approach allows the tuner to estimate the fundamental frequency directly from the time-domain audio signal.

### Cents Calculation

The difference between the detected frequency and the target frequency is expressed in cents, a logarithmic unit commonly used to describe musical pitch intervals.

This makes it possible to provide a continuous tuning indicator rather than simply reporting whether a note is correct or incorrect.

## Limitations

The current implementation is intentionally lightweight and has several limitations:

* Background noise can affect pitch detection.
* Very weak input signals may not produce a reliable frequency estimate.
* Audio interface and driver configuration can affect detection quality.
* The tuner currently assumes standard guitar tuning.
* Pitch detection can become less reliable with complex or heavily distorted signals.

## Potential Improvements

* Frequency smoothing and stability filtering
* Improved octave and harmonic rejection
* Pitch detection confidence estimation
* Automated tests using known reference frequencies
* Support for alternate tunings
* Graphical user interface
* Real-time guitar effects and DSP experiments
* C++/JUCE implementation for lower-latency processing
* Embedded implementation on a microcontroller

## Technologies

* **Python**
* **NumPy**
* **SoundDevice**
* **Digital Signal Processing**
* **YIN Pitch Detection**

## Motivation

This project started as a way to combine two of my interests: **electrical engineering and electric guitar**.

It serves as a practical introduction to audio signal processing, frequency estimation, and real-time systems while providing a useful tool for tuning an electric guitar.

---

**Author:** [Yavuz Selim Sert](https://github.com/yavuzselimsert)
