import marimo

__generated_with = "0.14.7"
app = marimo.App(width="medium")


@app.cell
def _(duration_s, mo, modulator_hz, source_hz, wobble):
    mo.md(
        f"""
    # Let's Make Some Noise

    Source Hz: {source_hz}

    Modulator Hz: {modulator_hz}

    Wobble: {wobble}

    Duration: {duration_s}
    """
    )
    return


@app.cell
def _(mo):
    source_hz = mo.ui.slider(start=200.0, stop=600.0, show_value=True)
    modulator_hz=mo.ui.slider(0, 100.0, show_value=True)
    wobble=mo.ui.slider(0, 1.0, 0.01, show_value=True)
    duration_s=mo.ui.slider(1.0, 10.0, show_value=True)
    return duration_s, modulator_hz, source_hz, wobble


@app.cell
def _(duration_s, make_audio, modulator_hz, source_hz, wobble):
    audio_data = make_audio(source_hz.value, modulator_hz.value, wobble.value, duration_s.value)
    return (audio_data,)


@app.cell
def _(audio_data, plt):
    print(audio_data)
    plt.plot(audio_data[:2000])
    return


@app.cell
def _(SAMPLE_RATE, audio_data, mo):
    audio = mo.audio(audio_data, rate=SAMPLE_RATE)
    audio
    return


@app.cell
def _(SAMPLE_RATE, np):
    def make_audio(source_hz: float, modulator_hz: float, wobble: float, duration_s: float) -> np.array:
        # Create a linear time sample
        n_samples = np.arange(SAMPLE_RATE * duration_s) / SAMPLE_RATE
        # Convert the time series into a uniform sine wave
        # Aka monotonal sound
        source = np.sin(2 * np.pi * source_hz * n_samples)
        # Create modulator at a different frequency
        source2 = np.sin(2 * np.pi * modulator_hz * n_samples)
        modulator = 0.5 * (1.0 + wobble * source2)
        # Modulate with constructive and destructive interference
        return source * modulator
    return (make_audio,)


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np

    SAMPLE_RATE = 22050
    return SAMPLE_RATE, mo, np, plt


if __name__ == "__main__":
    app.run()
