import csv
import logging
import os
import pickle
from typing import Optional

import pandas as pd
from django.contrib import messages
from django.shortcuts import render
from sklearn.preprocessing import StandardScaler

from bloodDataAnalysisWebApp.settings import BASE_DIR
from .forms import SampleBulkUploadForm
from .models import Sample, SampleBulkUpload

initial_sampno = "AE00001"


def index(request):
    print("test")
    return render(request, 'ml_api/index.html')


def generate_next_sampno(previous_sampno: Optional[str]) -> str:
    head = previous_sampno.rstrip('0123456789')
    tail = previous_sampno[len(head):]
    next_number = "{:05d}".format(int(tail) + 1)
    next_sampno = "{}{}".format(head, next_number)
    return next_sampno


def save_new_samples_from_csv(file_path: str) -> str:
    # do try catch accordingly
    # open csv file, read lines
    with open(file_path, 'r') as fp:
        samples = csv.reader(fp, delimiter=',')
        row = 0
        for sample in samples:
            if row == 0:
                headers = sample
                row = row + 1
            else:
                # generate sampno
                last_sampno_row = Sample.objects.all().values('sampno').order_by('-sampno')
                next_sampno = generate_next_sampno(last_sampno_row[0].get("sampno")
                                                   ) if last_sampno_row else initial_sampno

                # create a dictionary of sample details
                new_sample_details = {'sampno': next_sampno}
                for i in range(len(headers)):
                    new_sample_details[headers[i]] = sample[i]

                # create an instance of Sample model
                new_sample = Sample()
                new_sample.__dict__.update(new_sample_details)
                new_sample.save()
                row = row + 1
        fp.close()
    return next_sampno


def upload_file_view(request):
    result = "empty"
    if request.method == 'GET':
        form = SampleBulkUploadForm()
        return render(request, 'ml_api/upload.html', {'form': form})
    else:
        try:
            form = SampleBulkUploadForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data['csv_file']
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'File is not CSV type')
                    return render(request, '')
                # If file is too large
                if csv_file.multiple_chunks():
                    messages.error(request, 'Uploaded file is too big (%.2f MB)' % (csv_file.size(1000 * 1000),))
                    return render(request, '')

                # save and upload file
                # form.save()
                new_sample_bulk_upload = SampleBulkUpload(csv_file=request.FILES['csv_file'])
                new_sample_bulk_upload.save()
                # get the path of the file saved in the server
                file_path = os.path.join(BASE_DIR, new_sample_bulk_upload.csv_file.url[1:])  # cut first slash /

                # a function to read the file contents and save the sample details
                sampno = save_new_samples_from_csv(file_path)
                df = pd.DataFrame.from_records(Sample.objects.filter(sampno=sampno).values())
                df = df.drop(columns=['id', 'sampno'])
                result = get_result_from_predictions(df)

        except Exception as e:
            logging.getLogger('error_logger').error('Unable to upload file. ' + repr(e))
            messages.error(request, 'Unable to upload file. ' + repr(e))
        return render(request, 'ml_api/upload.html', {'form': form, 'result': result})


def get_result_from_predictions(df):
    model = pickle.load(open("./ml_api/MLmodel.sav", 'rb'))
    scaler = StandardScaler()
    x = scaler.transform(df)
    prediction = model.predict(x)
    if prediction == 0:
        result = "Normal"
    elif prediction == 1:
        result = "Ovary"
    elif prediction == 2:
        result = "Liver"
    else:
        result = "No valid prediction"
    return result
