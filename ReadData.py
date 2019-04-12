import pandas as pd
from pandas import Series
import matplotlib.pyplot as plt

class Reading():
	def __init__(self, light, sound, ms):
		self.light = light
		self.sound = sound
		self.time = ms

def valence_arousal_to_engagement(valence, arousal):
	valence = int(valence)
	arousal = int(arousal)
	if valence == 1 and arousal == 1: return "No"
	elif valence == 1 and arousal == 2: return "No"
	elif valence == 1 and arousal == 3: return "No"
	elif valence == 1 and arousal == 4: return "No"
	elif valence == 1 and arousal == 5: return "No"
	elif valence == 2 and arousal == 1: return "No"
	elif valence == 2 and arousal == 2: return "No"
	elif valence == 2 and arousal == 3: return "Somewhat"
	elif valence == 2 and arousal == 4: return "Yes"
	elif valence == 2 and arousal == 5: return "Yes"
	elif valence == 3 and arousal == 1: return "No"
	elif valence == 3 and arousal == 2: return "Somewhat"
	elif valence == 3 and arousal == 3: return "Somewhat"
	elif valence == 3 and arousal == 4: return "Yes"
	elif valence == 3 and arousal == 5: return "Yes"
	elif valence == 4 and arousal == 1: return "No"
	elif valence == 4 and arousal == 2: return "Yes"
	elif valence == 4 and arousal == 3: return "Yes"
	elif valence == 4 and arousal == 4: return "Yes"
	elif valence == 4 and arousal == 5: return "Yes"
	elif valence == 5 and arousal == 1: return "No"
	elif valence == 5 and arousal == 2: return "Somewhat"
	elif valence == 5 and arousal == 3: return "Somewhat"
	elif valence == 5 and arousal == 4: return "Yes"
	elif valence == 5 and arousal == 5: return "Yes"
		
combined_df = pd.DataFrame()
lux_array = []
sound_array = []
valence_array = []
arousal_array = []
time_array = []
for i in range(1,8):
	excel_path = "Excel/" + str(i) + ".xlsx"
	phone_path = "Phone/" + str(i) + ".csv"

	#Phone data
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
			time_array.append(10*(len(time_array)+1))
			sound_sum = 0
			lux_sum = 0
			previous = row["Time"]
			readings = 0

		else:
			sound_sum += row["SOUND LEVEL (dB)"]
			lux_sum += row["LIGHT (lux)"]

		readings += 1
		
	#Excel data
	excel = pd.read_excel(excel_path)
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

#Convert valence and arousal to engagement
engagement_array = []
for i in range(len(valence_array)):
	engagement = valence_arousal_to_engagement(valence_array[i], arousal_array[i])
	engagement_array.append(engagement)

#Combine DataFrames
combined_df["Time"] = Series(time_array)
combined_df["Light"] = Series(lux_array)
combined_df["Sound"] = Series(sound_array)
combined_df["Engagement"] = Series(engagement_array)

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
