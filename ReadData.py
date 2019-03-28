import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt

excel_path = "Excel/Quinten_3-12-2019.xlsx"
phone_path = "Phone/quinten_3-12.csv"

class Reading():
	def __init__(self, light, sound, ms):
		self.light = light
		self.sound = sound
		self.time = ms

combined_df = pd.DataFrame()

lux_array = []
sound_array = []

phone = pd.read_csv(phone_path)
previous = 0
readings = 0
for index, row in phone.iterrows():
	if index == 0:
		sound_sum = 0
		lux_sum = 0

	if row["Time"] > previous + 10000:
		sound_array.append(round(sound_sum / readings * 1.0, 1))
		lux_array.append(round(lux_sum / readings * 1.0, 1))
		sound_sum = 0
		lux_sum = 0
		previous = row["Time"]
		readings = 0

	else:
		sound_sum += row["SOUND LEVEL (dB)"]
		lux_sum += row["LIGHT (lux)"]

	readings += 1


excel = pd.read_excel(excel_path)
valence_array = []
arousal_array = []
for index, row in excel.iterrows():
	arousal_array.append(row["Arousal"])
	valence_array.append(row["Valence"])

if len(lux_array) > len(arousal_array):
	cut_len = len(lux_array)
else:
	cut_len = len(arousal_array)

lux_array = lux_array[:cut_len]
sound_array = sound_array[:cut_len]
arousal_array = arousal_array[:cut_len]
valence_array = valence_array[:cut_len]

combined_df["Light"] = Series(lux_array)
combined_df["Sound"] = Series(sound_array)
combined_df["Arousal"] = Series(arousal_array)
combined_df["Valence"] = Series(valence_array)

combined_df = combined_df[(combined_df.T != 0).any()]
combined_df = combined_df.dropna(how="any")

# combined_df.plot(kind="scatter", x="Valence", y="Sound", color="Green",)
# combined_df.plot(kind="scatter", x="Valence", y="Light", color="Yellow", )
# plt.show()
#
# combined_df.plot(kind="scatter", x="Arousal", y="Sound", color="Red", )
# combined_df.plot(kind="scatter", x="Arousal", y="Light", color="Blue",)
# plt.show()

print combined_df

combined_df.to_csv("data.csv", index=False)
