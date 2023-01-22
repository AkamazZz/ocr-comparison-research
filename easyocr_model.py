from datetime import datetime
import os
from easyocr import Reader
import Levenshtein

# Initialize the OCR reader with the desired language(s)
reader = Reader(['en'])

# Read the text from the image
photo_list = os.listdir("C:/Users/akezh/Desktop/another_dataset/")
ground_truth = os.listdir('C:/Users/akezh/Desktop/another_dataset/groundtruth')

photo_num = 0
accuracy_ave = 0

with open('easyocr_report.txt', 'a') as f:
    f.write("=============================================================\n")
    f.write("Report on testing EasyOCR (" + str(datetime.now()) + "):\n")

for photo in photo_list:
    if photo == 'groundtruth':
        break

    text = reader.readtext('C:/Users/akezh/Desktop/another_dataset/0_bn.png', detail=0)
    actual_text = str().join(text)

    with open('C:/Users/akezh/Desktop/another_dataset/groundtruth/'+str(photo_num)+'_bn.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        pre_text = str().join(lines)

    # Actual text from ground truth.
    predicted_text = pre_text
    # Calculate Levenshtein distance
    distance = Levenshtein.distance(actual_text, predicted_text)
    # Calculate prediction accuracy
    try:
        accuracy = 1 - (distance / len(actual_text))
    except Exception:
        print('Empty picture found on' + str(photo_num))
        with open('easyocr_report.txt', 'a') as f:
            f.write('Empty picture found on image num.' + str(photo_num) + ';\n')

    if photo_num % 10 == 0:
        print("Accuracy on image num. "+str(photo_num)+": " + str(round(accuracy * 100, 2)) + '%')

    accuracy_ave = accuracy_ave + accuracy

    with open('easyocr_report.txt', 'a') as f:
        f.write("Accuracy on image num. "+str(photo_num)+": " + str(round(accuracy * 100, 2)) + '%;\n')

    photo_num = photo_num + 1


print('Average accuracy on ' + str(photo_num) + ' pictures dataset: ' +
      str(round((accuracy_ave / photo_num) * 100, 2)) + '%')
with open('easyocr_report.txt', 'a') as f:
    f.write('Total average accuracy on ' + str(photo_num) + ' pictures dataset: ' +
            str(round((accuracy_ave / photo_num) * 100, 2)) + '%.\n')
