import zipfile
from pathlib import Path
import pandas as pd

# === CONFIG ===
ZIP_PATH = Path(r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc\domestic-E07000222-Warwick.zip")
CERT_FILE = "certificates.csv"
REC_FILE  = "recommendations.csv"
SCHEMA_FILE = "columns.csv"

# Optional outputs (set to None to skip)
OUT_DIR = Path(r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc")
OUT_TALL = OUT_DIR / "warwick_cert_with_recs_TALL.parquet"
OUT_WIDE = OUT_DIR / "warwick_cert_with_recs_WIDE.parquet"


def load_schema_from_zip(zf: zipfile.ZipFile, schema_name: str, for_filename: str):
    with zf.open(schema_name) as f:
        schema = pd.read_csv(f)
    schema = schema[schema["filename"] == for_filename].copy()
    if schema.empty:
        raise ValueError(f"No schema rows for {for_filename} in {schema_name}")
    dtypes, date_cols = {}, []
    for col, kind in zip(schema["column"], schema["datatype"].str.lower()):
        if kind in {"date", "datetime"}:
            date_cols.append(col)
        elif kind == "integer":
            dtypes[col] = "Int64"
        elif kind in {"float", "decimal"}:
            dtypes[col] = "float64"
        elif kind == "string":
            dtypes[col] = "string"
        else:
            dtypes[col] = "string"
    return dtypes, date_cols


def norm_strings(df: pd.DataFrame) -> pd.DataFrame:
    for c in df.columns:
        if pd.api.types.is_string_dtype(df[c]):
            df[c] = df[c].str.strip().replace({"": pd.NA})
    return df


def main():
    with zipfile.ZipFile(ZIP_PATH) as z:
        # --- load certs with schema + dates ---
        cert_dtypes, cert_dates = load_schema_from_zip(z, SCHEMA_FILE, CERT_FILE)
        with z.open(CERT_FILE) as f:
            df_cert = pd.read_csv(
                f,
                dtype=cert_dtypes,
                parse_dates=cert_dates if cert_dates else None,
                dayfirst=False,                 # ISO in EPC exports
                keep_default_na=True,
                na_values=["", "NA", "N/A"]
            )
        df_cert = norm_strings(df_cert)
        df_cert = df_cert[~df_cert["LMK_KEY"].isna()].drop_duplicates().reset_index(drop=True)
        df_cert["LMK_KEY"] = df_cert["LMK_KEY"].astype("string")

        # Assert 1 cert per property (true in your Warwick slice)
        assert df_cert["LMK_KEY"].is_unique, "Expected one certificate per LMK_KEY in this file."

        # --- load recommendations (no dates) ---
        rec_dtypes, _ = load_schema_from_zip(z, SCHEMA_FILE, REC_FILE)
        with z.open(REC_FILE) as f:
            df_rec = pd.read_csv(
                f,
                dtype=rec_dtypes,
                keep_default_na=True,
                na_values=["", "NA", "N/A"]
            )
        df_rec = norm_strings(df_rec)
        df_rec["LMK_KEY"] = df_rec["LMK_KEY"].astype("string")

    # --- Coverage summary ---
    cert_keys = set(df_cert["LMK_KEY"])
    rec_keys  = set(df_rec["LMK_KEY"].dropna())
    print(f"Certificates (properties): {len(df_cert):,}")
    print(f"Recommendations rows: {len(df_rec):,} across {len(rec_keys):,} properties")
    print(f"Properties with NO recs: {len(cert_keys - rec_keys):,}")

    # --- TALL: one row per recommendation, cert columns repeated ---
    tall = df_cert.merge(df_rec, on="LMK_KEY", how="left", suffixes=("_cert", "_rec"))
    print(f"TALL table rows: {len(tall):,}")

    # --- WIDE: one row per LMK_KEY, recs aggregated ---
    rec_cols = [
        "IMPROVEMENT_ITEM", "IMPROVEMENT_SUMMARY_TEXT", "IMPROVEMENT_DESCR_TEXT",
        "IMPROVEMENT_ID", "IMPROVEMENT_ID_TEXT", "INDICATIVE_COST"
    ]
    rec_cols = [c for c in rec_cols if c in df_rec.columns]

    # JSON list (machine-friendly)
    agg_json = (
        df_rec.groupby("LMK_KEY")[rec_cols]
              .apply(lambda g: g.dropna(how="all").to_dict(orient="records"))
              .rename("RECOMMENDATIONS_JSON")
              .reset_index()
    )

    # Readable string (quick eyes-on)
    def fmt_row(r):
        name = r.get("IMPROVEMENT_ID_TEXT") or r.get("IMPROVEMENT_SUMMARY_TEXT")
        cost = r.get("INDICATIVE_COST")
        if pd.notna(name) and pd.notna(cost):
            return f"{name} ({cost})"
        return name or ""
    agg_text = (
        df_rec.assign(_txt=df_rec[rec_cols].apply(fmt_row, axis=1))
              .groupby("LMK_KEY")["_txt"]
              .apply(lambda s: "; ".join(sorted(set([x for x in s if x]))))
              .rename("RECOMMENDATIONS_TEXT")
              .reset_index()
    )

    wide = (
        df_cert
        .merge(agg_json, on="LMK_KEY", how="left")
        .merge(agg_text, on="LMK_KEY", how="left")
    )
    print(f"WIDE table rows: {len(wide):,} (one per LMK_KEY)")
    print("Coverage with any recommendations:", f"{wide['RECOMMENDATIONS_JSON'].notna().mean():.1%}")

    # --- Save (optional) ---
    if OUT_TALL:
        tall.to_parquet(OUT_TALL, index=False)
    if OUT_WIDE:
        wide.to_parquet(OUT_WIDE, index=False)
    if OUT_TALL or OUT_WIDE:
        print("Saved:")
        if OUT_TALL: print("  -", OUT_TALL)
        if OUT_WIDE: print("  -", OUT_WIDE)

    # Quick peek
    show_cols = [c for c in ["LMK_KEY", "ADDRESS1", "POSTCODE", "LODGEMENT_DATE", "CURRENT_ENERGY_RATING", "RECOMMENDATIONS_TEXT"] if c in wide.columns]
    print("\nSample WIDE rows:")
    print(wide[show_cols].head(10))


if __name__ == "__main__":
    pd.options.display.width = 180
    pd.options.display.max_columns = 120
    main()
