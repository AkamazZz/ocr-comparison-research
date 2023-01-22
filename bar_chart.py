import numpy as np
import matplotlib.pyplot as plt

data = {'ABBYY Finereader': 72.65, 'EasyOCR': 90.28, 'TesseractOCR': 96.23}
courses = list(data.keys())
values = list(data.values())

fig = plt.figure(figsize=(10, 5))

# creating the bar plot
plt.bar(courses, values, color=['maroon', 'green', 'blue'],
        width=0.4)

plt.xlabel("Name of OCR engines")
plt.ylabel("Accuracy percentage %")
plt.title("Comparison of accuracy of OCR (Optical Character Recognition) engines")
plt.show()