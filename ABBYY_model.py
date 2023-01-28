from ABBYY import CloudOCR
import os
import Levenshtein
from datetime import datetime
try:
    photo_list = os.listdir("C:/Users/akezh/Desktop/dataset/original/")
    ground_truth = os.listdir('C:/Users/akezh/Desktop/dataset/original groundtruth/')

    ocr_engine = CloudOCR(application_id='a1afb19f-8f33-4d68-b4d8-80d03ec2f387', password='HpKPoz4WVEhlxR08QazVJxII')

    photo_num = 0
    accuracy_ave = 0
    binarized_accuracy_ave = 0
    with open('ABBYY_report.txt', 'a') as f:
        f.write("=============================================================\n")
        f.write("Report on testing ABBYY OCR (" + str(datetime.now()) + "):\n")

    for photo in photo_list:
        actual_text = ''
        binarized_actual_text = ''
        if photo_num == 250:
            break

        # Original image
        png = open('C:/Users/akezh/Desktop/dataset/original/' + str(photo_num) + '_bn.png', 'rb')
        file = {png.name: png}
        result = ocr_engine.process_and_download(file, exportFormat='txt', language='English')
        actual_text = result['txt'].read().decode('utf-8')
        # Binarized image
        binarized_png = open('C:/Users/akezh/Desktop/binarized/' + str(photo_num) + '_bn.png', 'rb')
        binarized_file = {png.name: binarized_png}
        binarized_result = ocr_engine.process_and_download(binarized_file, exportFormat='txt', language='English')
        binarized_actual_text = binarized_result['txt'].read().decode('utf-8')

        with open('C:/Users/akezh/Desktop/dataset/original groundtruth/' + str(photo_num) + '_bn.txt', 'r',
                  encoding='utf-8') as f:
            lines = f.readlines()
            pre_text = str().join(lines)

        predicted_text = pre_text
        distance = Levenshtein.distance(actual_text, predicted_text)
        binarized_distance = Levenshtein.distance(binarized_actual_text, predicted_text)

        try:
            accuracy = 1 - (distance / len(actual_text))
            binarized_accuracy = 1 - (binarized_distance / len(binarized_actual_text))
            if photo_num % 10 == 0:
                print("Accuracy on image num. " + str(photo_num) + ": " + '{"initial_image": '
                      + str(round(accuracy * 100, 2)) + ', "binarized_image": '
                      + str(round(binarized_accuracy * 100, 2)) + '}' + ' percent (%);')

            if accuracy < 0 or binarized_accuracy < 0:
                photo_num = photo_num + 1
                continue

            accuracy_ave = accuracy_ave + accuracy
            binarized_accuracy_ave = binarized_accuracy_ave + binarized_accuracy

            with open('ABBYY_report.txt', 'a') as f:
                f.write("Accuracy on image num. " + str(photo_num) + ": " + '{"initial_image": ' + str(
                    round(accuracy * 100, 2)) + ', "binarized_image": ' + str(
                    round(binarized_accuracy * 100, 2)) + '}' + ' percent (%);\n')
            photo_num = photo_num + 1
        except Exception:
            print('Empty picture found on: ' + str(photo_num))
            with open('ABBYY_report.txt', 'a') as f:
                f.write('Empty picture found on image num.' + str(photo_num) + ';\n')



except KeyboardInterrupt:
    print(str(binarized_accuracy_ave) + 'bin;' + str(accuracy_ave) + 'init;')
    exit(0)
except Exception:
    print(str(binarized_accuracy_ave) + 'bin;' + str(accuracy_ave) + 'init;')
    exit(0)
finally:
    with open('ABBYY_report.txt', 'a') as f:
        f.write('Total average accuracy on (' + str(datetime.now()) + ') ' + str(photo_num) + ' pictures dataset: ' +
                str(round((accuracy_ave / photo_num) * 100, 2)) + '%.' + '%, on binarized image: ' +
                str(round((binarized_accuracy_ave / photo_num) * 100, 2)) + '%.\n')
    print('Average accuracy on ' + str(photo_num) + ' pictures dataset: ' +
          str(round((accuracy_ave / photo_num) * 100, 2)) + '%, on binarized image: ' +
          str(round((binarized_accuracy_ave / photo_num) * 100, 2)) + '%.')

