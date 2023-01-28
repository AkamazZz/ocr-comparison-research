import os
import pytesseract
from PIL import Image
import Levenshtein
from datetime import datetime
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
photo_list = os.listdir("C:/Users/akezh/Desktop/dataset/original/")
ground_truth = os.listdir('C:/Users/akezh/Desktop/dataset/original groundtruth/')

photo_num = 0
accuracy_ave = 0
binarized_accuracy_ave = 0
with open('tesseract_report.txt', 'a') as f:
    f.write("=============================================================\n")
    f.write("Report on testing Tesseract OCR (" + str(datetime.now()) + "):\n")

for photo in photo_list:
    image = Image.open('C:/Users/akezh/Desktop/dataset/original/'+str(photo_num)+'_bn.png')
    binarized_image = Image.open('C:/Users/akezh/Desktop/binarized/'+str(photo_num)+'_bn.png')

    text = pytesseract.image_to_string(image)
    binarized_image_text = pytesseract.image_to_string(binarized_image)

    # Recognized text from OCR.
    actual_text = text
    binarized_actual_text = binarized_image_text
    print(actual_text)
    with open('C:/Users/akezh/Desktop/dataset/original groundtruth/'+str(photo_num)+'_bn.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        pre_text = str().join(lines)

    # Actual text from ground truth.
    predicted_text = pre_text
    print(predicted_text)
    # Calculate Levenshtein distance
    distance = Levenshtein.distance(actual_text, predicted_text)
    # Calculate prediction accuracy
    binarized_distance = Levenshtein.distance(binarized_actual_text, predicted_text)
    try:
        accuracy = 1 - (distance / len(actual_text))
        binarized_accuracy = 1 - (distance / len(binarized_actual_text))
    except Exception:
        print('Empty picture found on' + str(photo_num))
        with open('tesseract_report.txt', 'a') as f:
            f.write('Empty picture found on image num. ' + str(photo_num) + ';\n')

    if photo_num % 10 == 0:
        print("Accuracy on image num. "+str(photo_num)+": " + '{"initial_image": '+str(round(accuracy * 100, 2)) + ', "binarized_image": ' + str(round(binarized_accuracy * 100, 2)) + '}' + ' percent (%);')

    accuracy_ave = accuracy_ave + accuracy
    binarized_accuracy_ave = binarized_accuracy_ave + binarized_accuracy
    with open('tesseract_report.txt', 'a') as f:
        f.write("Accuracy on image num. "+str(photo_num)+": " + '{"initial_image": '+str(round(accuracy * 100, 2)) + ', "binarized_image": ' + str(round(binarized_accuracy * 100, 2)) + '}' + 'percent (%);\n')

    photo_num = photo_num + 1


print('Average accuracy on ' + str(photo_num) + ' pictures dataset: ' +
      str(round((accuracy_ave / photo_num) * 100, 2)) + '%, on binarized image: ' +
      str(round((binarized_accuracy_ave / photo_num) * 100, 2)) + '%.')
with open('tesseract_report.txt', 'a') as f:
    f.write('Total average accuracy on ' + str(photo_num) + ' pictures dataset: ' +
            str(round((accuracy_ave / photo_num) * 100, 2)) + '%.' + '%, on binarized image: ' +
            str(round((binarized_accuracy_ave / photo_num) * 100, 2)) + '%.\n')
