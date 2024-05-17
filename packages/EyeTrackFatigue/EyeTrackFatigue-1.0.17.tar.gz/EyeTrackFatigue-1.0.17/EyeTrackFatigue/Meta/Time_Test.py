import datetime
import pandas as pd
import joblib
from PyQt6.QtWidgets import *
from sklearn.metrics import accuracy_score, f1_score
from Input import read_csv_file
from Analise.ParsedData import ParsedData
now1 = datetime.datetime.now()
print(now1)

section = read_csv_file('Samples/five minutes short.csv')
metrics = ParsedData()
metrics.parse(section, 1, 1.0)
metrics.calc_metrics()

with open('Samples/MLP2.sav', 'rb') as file: 
    model = joblib.load(file)


chosen = ['x_mean', 'x_std', 'x_min', 'x_max', 'x_25', 'x_50', 'x_75', 'y_mean', 'y_std', 'y_min', 'y_max', 'y_25', 'y_50', 'y_75'] #, 'Saccades with amplitude < 6 degrees, per minute', 'Max Curve', 'Fixation time > 150 ms', 'Fixation time > 180 ms', '% of Fixations < 150 ms', '% of Fixations > 150 ms', '% of Fixations > 900 ms', '% of Fixations < 180 ms', '% of Fixations > 180 ms', 'Fixation time < 150 ms, per time', 'Fixation time > 150 ms, per time', '% of Fixations > 150 ms, per minute', '% of Fixations < 180 ms, per minute', 'Min Speed', 'Max Speed', 'Average Speed in interval (1s)', 'Max Speed in interval (1s)', 'Average Fixation Speed', 'Max Fixation Speed', 'Average Saccade Length', 'Min Saccade Length', 'Max Saccade Length']
data_row = metrics.get_df_row()[chosen]

predict_Y = model.evaluate(data_row)
print('Accuracy Score:', accuracy_score([1], predict_Y))
print('F1 Score:', f1_score([1], predict_Y))

now = datetime.datetime.now()
print(now)
print('Total time:', now - now1)

