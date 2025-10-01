#Author: Adeoluwa (Ade) Olateru-Olagbegi
#Project: Hospital Check-In Analytics Dashboard
#Date: 08/15/2025
#Description: This program analyzes hospital check-in data to calculate
#patient volumes, wait times, and error counts. It then generates an Excel
#report with both detailed logs and a daily summary.

import pandas as pd

def generate_checkin_report(input_file, output_file):
    """
    Reads a hospital check-in dataset (CSV), processes it to calculate 
    useful metrics, and exports the results into an Excel file with 
    multiple sheets.
    """
    
    #Step1: Load hospital check-in data from CSV
    df = pd.read_csv(input_file)

    #Step2: Convert check-in and appointment times to proper datetime objects
    df["CheckIn_Time"] = pd.to_datetime(df["CheckIn_Time"])
    df["Appointment_Time"] = pd.to_datetime(df["Appointment_Time"])

    #Step3: Calculate wait times in minutes for each patient
    df["Wait_Time_Minutes"] = (
        (df["Appointment_Time"] - df["CheckIn_Time"]).dt.total_seconds() / 60
    )

    #Step4: Create a daily summary (total check-ins, avg wait time, errors)
    daily_summary = df.groupby("Date").agg({
        "Patient_ID": "count",
        "Wait_Time_Minutes": "mean",
        "Error_Flag": "sum"
    }).reset_index()

    #Step5: Rename columns for clarity
    daily_summary.rename(columns={
        "Patient_ID": "Total_CheckIns",
        "Wait_Time_Minutes": "Avg_Wait_Time",
        "Error_Flag": "Data_Errors"
    }, inplace=True)

    #Step6: Export logs + summary to Excel
    with pd.ExcelWriter(output_file) as writer:
        df.to_excel(writer, sheet_name="Detailed Logs", index=False)
        daily_summary.to_excel(writer, sheet_name="Daily Summary", index=False)

    return daily_summary


#Test
sample_data = {
    "Date": ["2025-08-10", "2025-08-10", "2025-08-11", "2025-08-11", "2025-08-12"],
    "Patient_ID": [101, 102, 103, 104, 105],
    "Name": ["Chinedu Okafor", "Amaka Adeyemi", "Tunde Balogun", "Ngozi Obi", "Bolu Adebayo"],
    "CheckIn_Time": [
        "2025-08-10 08:00",
        "2025-08-10 08:15",
        "2025-08-11 09:05",
        "2025-08-11 09:20",
        "2025-08-12 10:10"
    ],
    "Appointment_Time": [
        "2025-08-10 08:30",
        "2025-08-10 08:50",
        "2025-08-11 09:20",
        "2025-08-11 09:50",
        "2025-08-12 10:40"
    ],
    "Error_Flag": [0, 1, 0, 0, 1]
}

#Save the test dataset as CSV
pd.DataFrame(sample_data).to_csv("hospital_checkins.csv", index=False)

#Run the report and generate Excel
summary = generate_checkin_report("hospital_checkins.csv", "hospital_report.xlsx")

#Print summary in terminal
print("Hospital Check-In Summary:\n", summary)