import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Daily Remark Summary", page_icon="📊", initial_sidebar_state="expanded")

# Apply dark mode
st.markdown(
    """
    <style>
    .reportview-container {
        background: #2E2E2E;
        color: white;
    }
    .sidebar .sidebar-content {
        background: #2E2E2E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Daily Remark Summary')

uploaded_file = st.sidebar.file_uploader("Upload Daily Remark File", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    df = df[~df['Remark By'].isin(['FGPANGANIBAN', 'KPILUSTRISIMO', 'BLRUIZ', 'MMMEJIA'])]
    
    st.write(df)
    col1, col2 = st.columns(2)

    with col1:
        st.write("## Overall Predictive Summary Table")
        
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
           
            ptp_acc = group[(group['Status'].str.contains('PTP', na=False)) & (group['PTP Amount'] != 0) & (group['Remark Type'].isin(['Predictive']))]['Account No.'].nunique()
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

    with col2:
        st.write("## Overall Manual Summary Table")
        
        overall_manual_table = pd.DataFrame(columns=[
            'Day', 'ACCOUNTS', 'TOTAL DIALED', 'PENETRATION RATE (%)', 'CONNECTED #', 
            'CONNECTED RATE (%)', 'CONNECTED ACC', 'PTP ACC', 'PTP RATE', 'CALL DROP #', 'CALL DROP RATIO #'
        ])
        
        for date, manual in df.groupby(df['Date'].dt.date):
            
            accounts = manual[(manual['Remark Type'] == 'Outgoing')]['Account No.'].nunique()
            total_dialed = manual[  (manual['Remark Type'] == 'Outgoing')]['Account No.'].count()

            connected = manual[(manual['Call Status'] == 'CONNECTED')]['Account No.'].count()
            connected_rate = (connected / total_dialed * 100) if total_dialed != 0 else None
            connected_acc = manual[(manual['Call Status'] == 'CONNECTED')]['Account No.'].nunique()

            penetration_rate = (total_dialed / accounts * 100) if accounts != 0 else None
           
            ptp_acc = manual[(manual['Status'].str.contains('PTP', na=False)) & (manual['PTP Amount'] != 0) & (manual['Remark Type'].isin(['Outgoing']))]['Account No.'].nunique()
            ptp_rate = (ptp_acc / connected_acc * 100) if connected_acc != 0 else None

            call_drop_count = manual[(manual['Call Status'] == 'DROPPED') & (manual['Remark Type'].isin(['Outgoing']))]['Account No.'].count()
            call_drop_ratio = (call_drop_count / connected * 100) if connected != 0 else None
            
            overall_manual_table = pd.concat([overall_manual_table, pd.DataFrame([{
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
        
        st.write(overall_manual_table)
    
    col3, col4 = st.columns(2)

    with col3:
        st.write("## Summary Table by Cycle Predictive")

        for cycle, cycle_group in df.groupby('Service No.'):
            st.write(f"Cycle: {cycle}")
            
            summary_table = pd.DataFrame(columns=[
                'Day', 'ACCOUNTS', 'TOTAL DIALED', 'PENETRATION RATE (%)', 'CONNECTED #', 
                'CONNECTED RATE (%)', 'CONNECTED ACC', 'PTP ACC', 'PTP RATE', 'CALL DROP #', 'CALL DROP RATIO #'
            ])
            
            for date, group in cycle_group.groupby(cycle_group['Date'].dt.date):
                accounts = group[(group['Remark Type'] == 'Predictive') | ((group['Remark Type'] == 'Follow Up') & (group['Remark By'] == 'SYSTEM'))]['Account No.'].nunique()
                total_dialed = group[  (group['Remark Type'] == 'Predictive') | ((group['Remark Type'] == 'Follow Up') & (group['Remark By'] == 'SYSTEM')) ]['Account No.'].count()

                connected = group[(group['Call Status'] == 'CONNECTED') & (group['Remark Type'].isin(['Predictive']))]['Account No.'].count()
                connected_rate = (connected / total_dialed * 100) if total_dialed != 0 else None
                connected_acc = group[(group['Call Status'] == 'CONNECTED') & (group['Remark Type'].isin(['Predictive']))]['Account No.'].nunique()

                penetration_rate = (total_dialed / accounts * 100) if accounts != 0 else None

                ptp_acc = group[(group['Status'].str.contains('PTP', na=False)) & (group['PTP Amount'] != 0) & (group['Remark Type'].isin(['Predictive']))]['Account No.'].nunique()
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

    with col4:
        st.write("## Summary Table by Cycle Manual")
        for manual_cycle, manual_cycle_group in df.groupby('Service No.'):
            st.write(f"Cycle: {manual_cycle}")
            
            summary_table = pd.DataFrame(columns=[
                'Day', 'ACCOUNTS', 'TOTAL DIALED', 'PENETRATION RATE (%)', 'CONNECTED #', 
                'CONNECTED RATE (%)', 'CONNECTED ACC', 'PTP ACC', 'PTP RATE', 'CALL DROP #', 'CALL DROP RATIO #'
            ])
            
            for date, group in manual_cycle_group.groupby(manual_cycle_group['Date'].dt.date):
                accounts = group[(group['Remark Type'] == 'Outgoing') ]['Account No.'].nunique()
                total_dialed = group[  (group['Remark Type'] == 'Outgoing')]['Account No.'].count()

                connected = group[(group['Call Status'] == 'CONNECTED') & (group['Remark Type'].isin(['Outgoing']))]['Account No.'].count()
                connected_rate = (connected / total_dialed * 100) if total_dialed != 0 else None
                connected_acc = group[(group['Call Status'] == 'CONNECTED') & (group['Remark Type'].isin(['Outgoing']))]['Account No.'].nunique()

                penetration_rate = (total_dialed / accounts * 100) if accounts != 0 else None

                ptp_acc = group[(group['Status'].str.contains('PTP', na=False)) & (group['PTP Amount'] != 0) & (group['Remark Type'].isin(['Outgoing']))]['Account No.'].nunique()
                ptp_rate = (ptp_acc / connected_acc * 100) if connected_acc != 0 else None

                call_drop_count = group[(group['Call Status'] == 'DROPPED') & (group['Remark Type'] == 'Outgoing')]['Account No.'].count()
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
