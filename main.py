from pathlib import Path
from math import gcd
import random
import sys

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

from rich.console import Console
from rich.panel import Panel
from rich.prompt import FloatPrompt
from rich.table import Table


SAMPLE_RATE = 48000
CHANNELS = 2
OUTPUT_PEAK = 0.90

MIN_VELOCITY = 0.80
MAX_VELOCITY = 1.00

MIN_PITCH = -0.5
MAX_PITCH = 0.5

TIMING_VARIATION = 0.03

console = Console()


# Paths

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

SAMPLE_FOLDER = BASE_DIR / "footsteps"
OUTPUT_FILE = BASE_DIR / "generated_footsteps.wav"


# Audio

def load_audio(filename):
    ## Loads a WAV file, resamples it when necessary, and returns stereo float32 audio.

    audio, sample_rate = sf.read(filename, dtype="float32", always_2d=True)

    # Convert sample rate

    if sample_rate != SAMPLE_RATE:
        divisor = gcd(sample_rate, SAMPLE_RATE)

        audio = resample_poly(
            audio,
            SAMPLE_RATE // divisor,
            sample_rate // divisor,
            axis=0
        ).astype(np.float32)

    # Convert channels

    if audio.shape[1] == 1:
        audio = np.repeat(audio, 2, axis=1)

    elif audio.shape[1] > 2:
        audio = audio[:, :2]

    return audio


def pitch_shift(audio, semitones):
    ## Changes pitch through playback-rate alteration.

    pitch_factor = 2 ** (semitones / 12.0)
    new_length = int(len(audio) / pitch_factor)

    if new_length <= 0:
        return audio

    old_positions = np.arange(len(audio))
    new_positions = np.linspace(0, len(audio) - 1, new_length)
    result = np.zeros((new_length, audio.shape[1]), dtype=np.float32)

    for channel in range(audio.shape[1]):
        result[:, channel] = np.interp(
            new_positions,
            old_positions,
            audio[:, channel]
        )

    return result


def place_audio(output, sample, time_seconds, gain=1.0):
    ## Places and mixes a sample at the requested position in the output timeline.

    start = int(time_seconds * SAMPLE_RATE)

    if start < 0 or start >= len(output):
        return

    end = min(start + len(sample), len(output))
    output[start:end] += sample[:end - start] * gain


# Shuffle bag

class ShuffleBag:
    ## Uses every available sample once before reshuffling the pool.

    def __init__(self, items):
        self.items = items
        self.bag = []
        self.previous = None

    def refill(self):
        self.bag = list(range(len(self.items)))
        random.shuffle(self.bag)

        #### Avoid repeating the final sample of the previous bag.

        if self.previous is not None and len(self.bag) > 1 and self.bag[-1] == self.previous:
            self.bag[-1], self.bag[0] = self.bag[0], self.bag[-1]

    def next(self):
        if not self.bag:
            self.refill()

        index = self.bag.pop()
        self.previous = index

        return self.items[index]


# Interface

def get_positive_float(label, default, allow_zero=False):
    while True:
        value = FloatPrompt.ask(label, default=default)

        if value > 0 or (allow_zero and value == 0):
            return value

        console.print("[red]Value must be greater than zero.[/red]")


def configuration_menu(sample_count):
    console.clear()

    console.print(
        Panel.fit(
            "[bold]FOOTSTEP GENERATOR[/bold]\n"
            "[dim]Procedural footstep track renderer[/dim]",
            border_style="cyan"
        )
    )

    console.print(
        f"\n[green]✓[/green] Found [bold]{sample_count}[/bold] "
        f"WAV samples in [cyan]footsteps/[/cyan]\n"
    )

    duration = get_positive_float(
        "[bold]Duration[/bold] [dim](seconds)[/dim]",
        60.0
    )

    tail_duration = get_positive_float(
        "[bold]Tail duration[/bold] [dim](seconds)[/dim]",
        10.0,
        allow_zero=True
    )

    step_interval = get_positive_float(
        "[bold]Step interval[/bold] [dim](seconds)[/dim]",
        0.52
    )

    table = Table(title="Render Settings", show_header=False, border_style="cyan")
    table.add_column("Setting", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Duration", f"{duration:.2f} s")
    table.add_row("Tail duration", f"{tail_duration:.2f} s")
    table.add_row("Step interval", f"{step_interval:.3f} s")
    table.add_row("Output duration", f"{duration + tail_duration:.2f} s")

    console.print()
    console.print(table)
    console.print()

    return duration, tail_duration, step_interval


# Renderer

def render(samples, duration, tail_duration, step_interval):
    total_duration = duration + tail_duration

    output = np.zeros(
        (int(total_duration * SAMPLE_RATE), CHANNELS),
        dtype=np.float32
    )

    bag = ShuffleBag(samples)

    current_time = 0.0
    step_count = 0

    while current_time < duration:
        sample = bag.next()

        velocity = random.uniform(MIN_VELOCITY, MAX_VELOCITY)
        pitch = random.uniform(MIN_PITCH, MAX_PITCH)

        processed = pitch_shift(sample["audio"], pitch)
        place_audio(output, processed, current_time, velocity)

        interval = step_interval + random.uniform(-TIMING_VARIATION, TIMING_VARIATION)
        current_time += max(interval, 0.001)

        step_count += 1

    # Normalize

    peak = np.max(np.abs(output))

    if peak > OUTPUT_PEAK:
        output *= OUTPUT_PEAK / peak

    return output, step_count


# Main

def main():
    files = sorted(SAMPLE_FOLDER.glob("*.wav"))

    if not files:
        console.print(
            Panel(
                "[red bold]No WAV samples found.[/red bold]\n\n"
                "Place your footstep samples inside the [cyan]footsteps/[/cyan] folder.",
                title="Error",
                border_style="red"
            )
        )

        input("\nPress Enter to exit...")
        return

    duration, tail_duration, step_interval = configuration_menu(len(files))

    console.print("[bold]Loading samples...[/bold]")

    samples = []

    for file in files:
        samples.append(
            {
                "name": file.name,
                "audio": load_audio(file)
            }
        )

    console.print("[green]✓[/green] Samples loaded")
    console.print("[bold]Generating track...[/bold]")

    output, step_count = render(
        samples,
        duration,
        tail_duration,
        step_interval
    )

    console.print("[bold]Exporting WAV...[/bold]")

    sf.write(
        OUTPUT_FILE,
        output,
        SAMPLE_RATE,
        subtype="PCM_24"
    )

    console.print(
        Panel.fit(
            f"[green bold]Render complete[/green bold]\n\n"
            f"Output: [cyan]{OUTPUT_FILE.name}[/cyan]\n"
            f"Steps generated: [bold]{step_count}[/bold]\n"
            f"Duration: [bold]{duration + tail_duration:.2f} s[/bold]\n"
            f"Sample rate: [bold]{SAMPLE_RATE:,} Hz[/bold]\n"
            f"Format: [bold]24-bit WAV[/bold]",
            border_style="green"
        )
    )

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()