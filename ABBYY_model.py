from ABBYY import CloudOCR
import os
import Levenshtein
from datetime import datetime

photo_list = os.listdir("C:/Users/akezh/Desktop/another_dataset/")
ground_truth = os.listdir('C:/Users/akezh/Desktop/another_dataset/groundtruth')

ocr_engine = CloudOCR(application_id='c4fd7c86-c31b-4f28-ae71-a9c9218f91aa', password='/3VxHSlRea+NCA7HjBDfw+9O')

photo_num = 484
accuracy_ave = 0

with open('ABBYY_report.txt', 'a') as f:
    f.write("=============================================================\n")
    f.write("Report on testing ABBYY OCR (" + str(datetime.now()) + "):\n")

for photo in photo_list:
    if photo == 'groundtruth' or photo_num == 500:
        break

    png = open('C:/Users/akezh/Desktop/another_dataset/' + str(photo_num) + '_bn.png', 'rb')
    file = {png.name: png}
    result = ocr_engine.process_and_download(file, exportFormat='txt', language='English')

    actual_text = result['txt'].read().decode('utf-8')

    with open('C:/Users/akezh/Desktop/another_dataset/groundtruth/' + str(photo_num) + '_bn.txt', 'r',
              encoding='utf-8') as f:
        lines = f.readlines()
        pre_text = str().join(lines)

    predicted_text = pre_text

    distance = Levenshtein.distance(actual_text, predicted_text)

    try:
        accuracy = 1 - (distance / len(actual_text))

    except Exception:
        print('Empty picture found on' + str(photo_num))
        with open('ABBYY_report.txt', 'a') as f:
            f.write('Empty picture found on image num.' + str(photo_num) + ';\n')

    if photo_num % 10 == 0:
        print("Accuracy on image num. " + str(photo_num) + ": " + str(round(accuracy * 100, 2)) + '%')

    if accuracy < 0:
        photo_num = photo_num + 1
        continue

    accuracy_ave = accuracy_ave + accuracy

    with open('ABBYY_report.txt', 'a') as f:
        f.write("Accuracy on image num. " + str(photo_num) + ": " + str(round(accuracy * 100, 2)) + '%;\n')

    photo_num = photo_num + 1


print('Average accuracy on ' + str(photo_num) + ' pictures dataset: ' +
      str(round((accuracy_ave / photo_num) * 100, 2)) + '%')
with open('ABBYY_report.txt', 'a') as f:
    f.write('Total average accuracy on ' + str(photo_num) + ' pictures dataset: ' +
            str(round((accuracy_ave / photo_num) * 100, 2)) + '%.\n')



