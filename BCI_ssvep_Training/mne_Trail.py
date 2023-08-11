import mne
import emotiv

# Create an Emotiv object and connect it to the headset.
emotiv = emotiv.Emotiv()
emotiv.connect()

# Start collecting EEG data.
raw = mne.io.Raw(emotiv.raw_data_stream, sfreq=128)

# Analyze the EEG data.
power = mne.time_frequency.power_spectral_density(raw, fmin=1, fmax=40)

# Get the predicted box from the machine learning model.
predicted_box = model.predict(power)

# Print the predicted box.
print(predicted_box)
