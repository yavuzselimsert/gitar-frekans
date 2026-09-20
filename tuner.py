import numpy as np
import sounddevice as sd


# Standard guitar tuning frequencies
STRINGS = {
    "E (Low, 6th string)": 82.41,
    "A (5th string)": 110.00,
    "D (4th string)": 146.83,
    "G (3rd string)": 196.00,
    "B (2nd string)": 246.94,
    "E (High, 1st string)": 329.63,
}


SAMPLE_RATE = 44100
DURATION = 0.5

# Number of consecutive failed detections before
# the tuner considers the signal to be lost.
MAX_SIGNAL_LOSS = 4


def yin_frekans_tespit(signal, sample_rate):
    """
    Estimate the fundamental frequency using the YIN algorithm.
    """

    signal = signal.flatten()

    # Remove DC offset
    signal = signal - np.mean(signal)

    # Ignore very weak signals
    if np.max(np.abs(signal)) < 0.01:
        return None

    max_tau = min(len(signal) // 2, 2000)

    # Difference function
    difference = np.zeros(max_tau)

    for tau in range(1, max_tau):
        difference[tau] = np.sum(
            (signal[:-tau] - signal[tau:]) ** 2
        )

    # Cumulative Mean Normalized Difference Function
    cmndf = np.ones(max_tau)

    running_sum = 0.0

    for tau in range(1, max_tau):
        running_sum += difference[tau]

        if running_sum == 0:
            cmndf[tau] = 1
        else:
            cmndf[tau] = (
                difference[tau] * tau / running_sum
            )

    # YIN threshold
    threshold = 0.15

    candidates = np.where(
        cmndf[2:] < threshold
    )[0]

    if len(candidates) == 0:
        return None

    tau = candidates[0] + 2

    # Parabolic interpolation for improved accuracy
    if 1 < tau < max_tau - 1:
        y1 = cmndf[tau - 1]
        y2 = cmndf[tau]
        y3 = cmndf[tau + 1]

        denominator = 2 * (2 * y2 - y1 - y3)

        if denominator != 0:
            tau = tau + (y3 - y1) / denominator

    if tau <= 0:
        return None

    frequency = sample_rate / tau

    return frequency


def find_nearest_string(frequency):
    """
    Find the guitar string closest to the detected frequency.
    """

    string_name = min(
        STRINGS,
        key=lambda string: abs(
            STRINGS[string] - frequency
        )
    )

    target_frequency = STRINGS[string_name]

    return string_name, target_frequency


def calculate_cents(frequency, target_frequency):
    """
    Calculate the pitch deviation in cents.
    """

    return 1200 * np.log2(
        frequency / target_frequency
    )


def get_tuning_status(cents):
    """
    Determine the tuning status from the cents deviation.
    """

    if abs(cents) <= 5:
        return "IN TUNE"

    if cents < -50:
        return "TOO FLAT"

    if cents < 0:
        return "FLAT"

    if cents > 50:
        return "TOO SHARP"

    return "SHARP"


def display_tuner(
    string_name,
    frequency,
    target_frequency,
    cents
):
    """
    Display the tuner interface in the terminal.
    """

    status = get_tuning_status(cents)

    width = 48
    gauge_width = 31

    # Limit the gauge to ±50 cents
    clamped_cents = max(-50, min(50, cents))

    gauge_position = int(
        (clamped_cents + 50)
        / 100
        * (gauge_width - 1)
    )

    gauge = ["-"] * gauge_width

    # Center marker
    gauge[gauge_width // 2] = "|"

    # Needle
    gauge[gauge_position] = "O"

    gauge = "".join(gauge)

    def line(text=""):
        print(
            "|" +
            text.center(width) +
            "|"
        )

    # Clear terminal
    print("\033[2J\033[H", end="")

    print("+" + "-" * width + "+")
    line("GUITAR TUNER")
    print("+" + "-" * width + "+")

    line()

    line(f"String: {string_name}")
    line(f"Frequency: {frequency:.2f} Hz")
    line(f"Target: {target_frequency:.2f} Hz")
    line(f"Deviation: {cents:+.1f} cents")

    line()

    line("FLAT")
    line("<" + gauge + ">")
    line("SHARP")

    line()

    line(status)

    line()

    print("+" + "-" * width + "+")
    print()
    print("Ctrl+C to exit")


def list_input_devices():
    """
    Display available audio input devices.
    """

    devices = sd.query_devices()

    print("\nAvailable audio input devices:\n")

    input_devices = []

    for device_index, device in enumerate(devices):

        if device["max_input_channels"] > 0:

            print(
                f"  {len(input_devices) + 1}: "
                f"{device['name']}"
            )

            input_devices.append(device_index)

    return input_devices


def main():
    input_devices = list_input_devices()

    device_number = int(
        input("\nSelect input device number: ")
    )

    # Convert the displayed number to the
    # actual sounddevice device index.
    device_index = input_devices[device_number - 1]

    print("\nStarting tuner...")
    print("Press Ctrl+C to exit.\n")

    last_valid_measurement = None
    signal_loss_count = 0

    try:

        while True:

            # Record audio
            audio = sd.rec(
                int(DURATION * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32",
                device=device_index
            )

            sd.wait()

            # Estimate fundamental frequency
            frequency = yin_frekans_tespit(
                audio,
                SAMPLE_RATE
            )

            # ---------------------------------
            # NO VALID SIGNAL
            # ---------------------------------

            if frequency is None:

                signal_loss_count += 1

                # Keep displaying the last valid
                # measurement for short signal gaps.
                if (
                    last_valid_measurement is not None
                    and signal_loss_count < MAX_SIGNAL_LOSS
                ):
                    continue

                # If there has been no valid
                # measurement yet, simply wait.
                if last_valid_measurement is None:
                    continue

                # Keep the previous tuner display.
                # The interface should not jump
                # back and forth when the signal
                # briefly disappears.
                continue

            # ---------------------------------
            # VALID SIGNAL
            # ---------------------------------

            signal_loss_count = 0

            string_name, target_frequency = (
                find_nearest_string(frequency)
            )

            cents = calculate_cents(
                frequency,
                target_frequency
            )

            last_valid_measurement = (
                string_name,
                frequency,
                target_frequency,
                cents
            )

            display_tuner(
                string_name,
                frequency,
                target_frequency,
                cents
            )

    except KeyboardInterrupt:
        print("\n\nTuner stopped.")


if __name__ == "__main__":
    main()