import streamlit as st
import pandas as pd

st.title('Excel File Uploader')

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    df = df[~df['Remark By'].isin(['FGPANGANIBAN', 'KPILUSTRISIMO', 'BLRUIZ', 'MMMEJIA'])]
    
    st.write(df)
    st.write("## Overall Summary Table")
    
    overall_summary_table = pd.DataFrame(columns=[
        'Day', 'ACCOUNTS', 'TOTAL DIALED', 'PENETRATION RATE (%)', 'CONNECTED #', 
        'CONNECTED RATE (%)', 'CONNECTED ACC', 'PTP ACC', 'PTP RATE', 'CALL DROP #', 'CALL DROP RATIO #'
    ])
    
    for date, group in df.groupby(df['Date'].dt.date):
        
        accounts = group[(group['Remark Type'] == 'Predictive') | ((group['Remark Type'] == 'Follow Up') & (group['Remark By'] == 'SYSTEM'))]['Account No.'].nunique()
        total_dialed = group[  (group['Remark Type'] == 'Predictive') | ((group['Remark Type'] == 'Follow Up') & (group['Remark By'] == 'SYSTEM')) ]['Account No.'].count()

        connected = group[(group['Call Status'] == 'CONNECTED') & (group['Remark Type'].isin(['Predictive']))]['Account No.'].count()
        connected_rate = (connected / total_dialed * 100) if total_dialed != 0 else None
        connected_acc = group[(group['Call Status'] == 'CONNECTED') & (group['Remark Type'].isin(['Predictive']))]['Account No.'].nunique()

        penetration_rate = (total_dialed / accounts * 100) if accounts != 0 else None
       
        ptp_acc = group[(group['Status'].str.contains('PTP', na=False)) & (group['PTP Amount'] != 0)]['Account No.'].nunique()
        ptp_rate = (ptp_acc / connected_acc * 100) if connected_acc != 0 else None

        call_drop_count = group[(group['Call Status'] == 'DROPPED') & (group['Remark Type'] == 'Predictive')]['Account No.'].count()
        call_drop_ratio = (call_drop_count / connected * 100) if connected != 0 else None
        
        overall_summary_table = pd.concat([overall_summary_table, pd.DataFrame([{
            'Day': date,
            'ACCOUNTS': accounts,
            'TOTAL DIALED': total_dialed,
            'PENETRATION RATE (%)': f"{round(penetration_rate)}%" if penetration_rate is not None else None,
            'CONNECTED #': connected,
            'CONNECTED RATE (%)': f"{round(connected_rate)}%" if connected_rate is not None else None,
            'CONNECTED ACC': connected_acc,
            'PTP ACC': ptp_acc,
            'PTP RATE': f"{round(ptp_rate)}%" if ptp_rate is not None else None,
            'CALL DROP #': call_drop_count,
            'CALL DROP RATIO #': f"{round(call_drop_ratio)}%" if call_drop_ratio is not None else None,
        }])], ignore_index=True)
    
    st.write(overall_summary_table)
    
    st.write("## Summary Table by Cycle")
    
    for cycle, cycle_group in df.groupby('Service No.'):
        st.write(f"### Cycle: {cycle}")
        
        summary_table = pd.DataFrame(columns=[
            'Day', 'ACCOUNTS', 'TOTAL DIALED', 'PENETRATION RATE (%)', 'CONNECTED #', 
            'CONNECTED RATE (%)', 'CONNECTED ACC', 'PTP ACC', 'PTP RATE', 'CALL DROP #', 'CALL DROP RATIO #'
        ])
        
        for date, group in cycle_group.groupby(cycle_group['Date'].dt.date):
            accounts = group[(group['Remark Type'] == 'Predictive') | ((group['Remark Type'] == 'Follow Up') & (group['Remark By'] == 'SYSTEM'))]['Account No.'].nunique()
            total_dialed = group[  (group['Remark Type'] == 'Predictive') | ((group['Remark Type'] == 'Follow Up') & (group['Remark By'] == 'SYSTEM')) ]['Account No.'].count()

            connected = group[(group['Call Status'] == 'CONNECTED') & (group['Remark Type'].isin(['Predictive']))]['Account No.'].count()
            connected_rate = (connected / total_dialed * 100) if total_dialed != 0 else None
            connected_acc = group[(group['Call Status'] == 'CONNECTED') & (group['Remark Type'].isin(['Predictive', 'Follow Up']))]['Account No.'].nunique()

            penetration_rate = (total_dialed / accounts * 100) if accounts != 0 else None

            ptp_acc = group[(group['Status'].str.contains('PTP', na=False)) & (group['PTP Amount'] != 0)]['Account No.'].nunique()
            ptp_rate = (ptp_acc / connected_acc * 100) if connected_acc != 0 else None

            call_drop_count = group[(group['Call Status'] == 'DROPPED') & (group['Remark Type'] == 'Predictive')]['Account No.'].count()
            call_drop_ratio = (call_drop_count / connected * 100) if connected != 0 else None
            
            summary_table = pd.concat([summary_table, pd.DataFrame([{
                'Day': date,
                'ACCOUNTS': accounts,
                'TOTAL DIALED': total_dialed,
                'PENETRATION RATE (%)': f"{round(penetration_rate)}%" if penetration_rate is not None else None,
                'CONNECTED #': connected,
                'CONNECTED RATE (%)': f"{round(connected_rate)}%" if connected_rate is not None else None,
                'CONNECTED ACC': connected_acc,
                'PTP ACC': ptp_acc,
                'PTP RATE': f"{round(ptp_rate)}%" if ptp_rate is not None else None,
                'CALL DROP #': call_drop_count,
                'CALL DROP RATIO #': f"{round(call_drop_ratio)}%" if call_drop_ratio is not None else None,
            }])], ignore_index=True)
        
        st.write(summary_table)
