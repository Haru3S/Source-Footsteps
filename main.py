from pathlib import Path
import random

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly


# ============================================================
# SETTINGS
# ============================================================

# Folder containing your 12 footstep WAV files.
SAMPLE_FOLDER = Path("footsteps")

# Exported file.
OUTPUT_FILE = Path("generated_footsteps.wav")

# Length of the actual footstep sequence.
DURATION = 75.0

# Extra silence after the last possible step.
#
# This is useful when you later apply reverb because the
# exported track continues beyond the action instead of
# immediately ending.
TAIL_DURATION = 10.0

# Time between footsteps.
STEP_INTERVAL = 1.4

# Random variation in timing.
#
# Example:
# 0.03 means each step can move +/- 0.03 seconds.
TIMING_VARIATION = 0.03

# Volume/velocity range.
MIN_VELOCITY = 0.80
MAX_VELOCITY = 1.00

# Pitch variation in semitones.
#
# +/- 0.5 is intentionally subtle.
MIN_PITCH = -0.5
MAX_PITCH = 0.5

# Output settings.
SAMPLE_RATE = 48000
CHANNELS = 2

# Leave some headroom instead of normalizing all the way
# to digital maximum.
OUTPUT_PEAK = 0.90


# ============================================================
# AUDIO FUNCTIONS
# ============================================================

def load_audio(filename):
    """
    Load a WAV file and convert it to stereo float32.
    """

    audio, sample_rate = sf.read(
        filename,
        dtype="float32",
        always_2d=True
    )

    # --------------------------------------------------------
    # Convert sample rate if necessary
    # --------------------------------------------------------

    if sample_rate != SAMPLE_RATE:

        print(
            f"Resampling {filename.name}: "
            f"{sample_rate} Hz -> {SAMPLE_RATE} Hz"
        )

        # Determine integer ratio for scipy resample_poly.
        from math import gcd

        divisor = gcd(sample_rate, SAMPLE_RATE)

        up = SAMPLE_RATE // divisor
        down = sample_rate // divisor

        audio = resample_poly(
            audio,
            up,
            down,
            axis=0
        ).astype(np.float32)

    # --------------------------------------------------------
    # Convert channels
    # --------------------------------------------------------

    if audio.shape[1] == 1:

        # Mono -> stereo
        audio = np.repeat(audio, 2, axis=1)

    elif audio.shape[1] > 2:

        # If somehow given multichannel audio,
        # just use the first two channels.
        audio = audio[:, :2]

    return audio


def pitch_shift(audio, semitones):
    """
    Simple pitch shift.

    Changes the playback speed of the sample, which changes
    both pitch and sample duration.

    For subtle footstep variation this generally works well.
    """

    pitch_factor = 2 ** (semitones / 12.0)

    original_length = len(audio)

    new_length = int(
        original_length / pitch_factor
    )

    if new_length <= 0:
        return audio

    # Generate positions in original audio.
    old_positions = np.arange(original_length)

    new_positions = np.linspace(
        0,
        original_length - 1,
        new_length
    )

    result = np.zeros(
        (new_length, audio.shape[1]),
        dtype=np.float32
    )

    # Interpolate each channel.
    for channel in range(audio.shape[1]):

        result[:, channel] = np.interp(
            new_positions,
            old_positions,
            audio[:, channel]
        )

    return result


def place_audio(output, sample, time_seconds, gain=1.0):
    """
    Mix a sample into the output timeline.
    """

    start_sample = int(
        time_seconds * SAMPLE_RATE
    )

    if start_sample < 0:
        return

    if start_sample >= len(output):
        return

    end_sample = start_sample + len(sample)

    # Prevent writing beyond output.
    if end_sample > len(output):
        end_sample = len(output)

    amount = end_sample - start_sample

    if amount <= 0:
        return

    output[
        start_sample:end_sample
    ] += sample[:amount] * gain


# ============================================================
# SHUFFLE BAG
# ============================================================

class ShuffleBag:
    """
    Randomly uses every footstep before repeating the pool.

    This avoids things like:

        3, 3, 3, 7, 3

    which can happen with pure random.choice().
    """

    def __init__(self, items):
        self.items = items
        self.bag = []
        self.previous = None

    def refill(self):

        self.bag = list(range(len(self.items)))

        random.shuffle(self.bag)

        # Try to prevent the first sample of the new bag
        # from matching the final sample of the previous bag.
        if (
            self.previous is not None
            and len(self.bag) > 1
            and self.bag[-1] == self.previous
        ):
            self.bag[-1], self.bag[0] = (
                self.bag[0],
                self.bag[-1]
            )

    def next(self):

        if not self.bag:
            self.refill()

        index = self.bag.pop()

        self.previous = index

        return index, self.items[index]


# ============================================================
# MAIN GENERATOR
# ============================================================

def main():

    print()
    print("==============================")
    print("     FOOTSTEP GENERATOR")
    print("==============================")
    print()

    # --------------------------------------------------------
    # Find WAV files
    # --------------------------------------------------------

    files = sorted(
        SAMPLE_FOLDER.glob("*.wav")
    )

    if not files:
        print(
            f"ERROR: No WAV files found in "
            f"'{SAMPLE_FOLDER}'"
        )
        return

    print(
        f"Found {len(files)} footstep samples."
    )

    for file in files:
        print(f"  - {file.name}")

    print()

    # --------------------------------------------------------
    # Load all samples
    # --------------------------------------------------------

    print("Loading samples...")

    samples = []

    for file in files:

        audio = load_audio(file)

        samples.append(
            {
                "name": file.name,
                "audio": audio
            }
        )

    print("Samples loaded.")
    print()

    # --------------------------------------------------------
    # Create output timeline
    # --------------------------------------------------------

    total_duration = (
        DURATION + TAIL_DURATION
    )

    total_samples = int(
        total_duration * SAMPLE_RATE
    )

    output = np.zeros(
        (total_samples, CHANNELS),
        dtype=np.float32
    )

    # --------------------------------------------------------
    # Generate footsteps
    # --------------------------------------------------------

    bag = ShuffleBag(samples)

    current_time = 0.0
    step_number = 1

    print("Generating footsteps...")
    print()

    while current_time < DURATION:

        index, sample_data = bag.next()

        sample = sample_data["audio"]
        name = sample_data["name"]

        # ----------------------------------------------------
        # Velocity
        # ----------------------------------------------------

        velocity = random.uniform(
            MIN_VELOCITY,
            MAX_VELOCITY
        )

        # ----------------------------------------------------
        # Pitch
        # ----------------------------------------------------

        pitch = random.uniform(
            MIN_PITCH,
            MAX_PITCH
        )

        processed = pitch_shift(
            sample,
            pitch
        )

        # ----------------------------------------------------
        # Place sample
        # ----------------------------------------------------

        place_audio(
            output,
            processed,
            current_time,
            velocity
        )

        print(
            f"Step {step_number:03d} | "
            f"{current_time:7.3f}s | "
            f"{name:<20} | "
            f"Velocity {velocity:.2f} | "
            f"Pitch {pitch:+.2f} st"
        )

        # ----------------------------------------------------
        # Determine next step
        # ----------------------------------------------------

        interval = (
            STEP_INTERVAL
            + random.uniform(
                -TIMING_VARIATION,
                TIMING_VARIATION
            )
        )

        current_time += interval
        step_number += 1

    # --------------------------------------------------------
    # Protect against clipping
    # --------------------------------------------------------

    peak = np.max(
        np.abs(output)
    )

    if peak > OUTPUT_PEAK:

        scale = OUTPUT_PEAK / peak

        print()
        print(
            f"Peak was {peak:.3f}. "
            f"Scaling output by {scale:.3f}."
        )

        output *= scale

    # --------------------------------------------------------
    # Export
    # --------------------------------------------------------

    print()
    print("Exporting...")

    sf.write(
        OUTPUT_FILE,
        output,
        SAMPLE_RATE,
        subtype="PCM_24"
    )

    print()
    print("==============================")
    print("DONE")
    print("==============================")

    print(
        f"Output: {OUTPUT_FILE}"
    )

    print(
        f"Footstep duration: "
        f"{DURATION:.2f} seconds"
    )

    print(
        f"Tail: "
        f"{TAIL_DURATION:.2f} seconds"
    )

    print(
        f"Total WAV duration: "
        f"{total_duration:.2f} seconds"
    )

    print(
        f"Steps generated: "
        f"{step_number - 1}"
    )

    print()


if __name__ == "__main__":
    main()