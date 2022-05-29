import os
import glob

from django.db import models

from bloodDataAnalysisWebApp.settings import BASE_DIR


class Sample(models.Model):
    sampno = models.CharField(max_length=7)
    afp = models.FloatField()
    angiopoietin_2 = models.FloatField()
    axl = models.FloatField()
    ca_125 = models.FloatField()
    ca_15_3 = models.FloatField()
    ca19_9 = models.FloatField()
    cd44 = models.FloatField()
    cea = models.FloatField()
    cyfra_21_1 = models.FloatField()
    dkk1 = models.FloatField()
    endoglin = models.FloatField()
    fgf2 = models.FloatField()
    follistatin = models.FloatField()
    galectin_3 = models.FloatField()
    g_csf = models.FloatField()
    gdf15 = models.FloatField()
    he4 = models.FloatField()
    hgf = models.FloatField()
    il_6 = models.FloatField()
    il_8 = models.FloatField()
    kallikrein_6 = models.FloatField()
    leptin = models.FloatField()
    mesothelin = models.FloatField()
    midkine = models.FloatField()
    myeloperoxidase = models.FloatField()
    nse = models.FloatField()
    opg = models.FloatField()
    opn = models.FloatField()
    par = models.FloatField()
    prolactin = models.FloatField()
    segfr = models.FloatField()
    sfas = models.FloatField()
    shbg = models.FloatField()
    sHER2_sEGFR2_sErbB2 = models.FloatField()
    sPECAM_1 = models.FloatField()
    tgfa = models.FloatField()
    thrombospondin_2 = models.FloatField()
    timp_1 = models.FloatField()
    timp_2 = models.FloatField()


class SampleBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to='ml_api/bulkupload/')

    def __str__(self):
        return f"File id: {self.id}"

    def delete(self, using=None, keep_parents=False):  # temp solution
        folder = os.path.join(BASE_DIR, 'ml_api/bulkupload')
        files = glob.glob(f"{folder}/.*")
        try:
            for f in files:
                os.remove(f)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (f, e))
