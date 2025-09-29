import pandas as pd
import zipfile

zip_path = r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc\domestic-E07000222-Warwick.zip"
certificates_csv = "certificates.csv"
recommendations_csv = "recommendations.csv"

with zipfile.ZipFile(zip_path) as z:
    with z.open(certificates_csv) as f1:
        df_cert = pd.read_csv(f1)
        cert_len = len(df_cert)
    with z.open(recommendations_csv) as f2:
        df_rec = pd.read_csv(f2)
        rec_len = len(df_rec)

#print(certificats_df.head())
#print(recommendations_df.head())

print("certificate_csv length:", cert_len, "recommendations_csv length:", rec_len)
print("difference:", cert_len - rec_len)