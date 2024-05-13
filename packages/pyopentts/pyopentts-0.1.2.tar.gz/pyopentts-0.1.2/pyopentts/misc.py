def save_audio(wav_data, path):
    with open(path, "wb") as file:
        file.write(wav_data)
    print(f"Audio file saved as {path}")
