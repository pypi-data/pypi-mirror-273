# -*- coding: utf-8 -*-
"""
Created on Tue May 14 07:57:04 2024

@author: S.T.Hwang
"""

def colab_ppt(file):
    # file_out_ppt= '/content/drive/MyDrive/PPT_Output.xlsx'

    import pandas as pd
    import numpy as np

    df=pd.read_excel(file,skiprows=32,usecols=None)


    df_Daily_NAV=df.iloc[2:,2:] # Daily NAVs 만을 발췌
    df_Daily_NAV=df_Daily_NAV.fillna(0) # NaN을 0으로 바꾸기
    df_Daily_NAV = df_Daily_NAV.apply(pd.to_numeric, errors='coerce') # 모든 열을 숫자로 변환

    # 연속된 0인 행 삭제
    remove_consecutive_zeros(df_Daily_NAV)

    # 일자를 인덱스 정보로 불러오고 포맷변경
    Biz_Dates=df.iloc[-len(df_Daily_NAV):,1]
    Biz_Dates=pd.to_datetime(Biz_Dates, format='%Y%m%d')


    # ELS 발행정보 정보 읽어오기
    df_Issuance_Info=pd.read_excel(file, nrows=35) # 처음 35행만 읽어오기
    Notional_Amount = df_Issuance_Info.iloc[12,2:] # 발행총액 정보를 읽어옴
    Notional_Amount = Notional_Amount.apply(int) # 숫자 데이터로 변환
    # Series 이름제거
    Notional_Amount = Notional_Amount.reset_index(drop=True)
    KR_Code=df_Issuance_Info.iloc[7,2:] # 발행코드 정보를 읽어옴

    # 날짜를 인덱스로 설정하기
    df_Daily_NAV = df_Daily_NAV.set_index(Biz_Dates)
    df_Daily_NAV.index.name = 'Biz_Dates'

    df_Daily_NAV = df_Daily_NAV.rename(columns=KR_Code) #칼럼 이름 주기

    # 발행 정보를 분석하기 위한 새로운 데이터프레임 만들기
    issued_date=df_Issuance_Info.iloc[13,2:] # 각 종목의 발행일자가 저장됨
    issued_date = pd.to_datetime(issued_date) # 날짜형식으로 변환
    # 인덱스를 초기화하여 시리즈 재설정
    issued_date = issued_date.reset_index(drop=True)
    Notional_Amount = Notional_Amount.reset_index(drop=True)
    df_issued_summary=pd.DataFrame(data={'발행일':issued_date,'발행총액':Notional_Amount})
    df_issued_summary.index=KR_Code
    df_issued_summary.index.name='KR code'

    # 발행 총액을 곱하여 Market Cap 계산
    # 발행 총액 연산을 위해 numpy array 포맷으로 변환

    np_Notional_Amount=np.array(Notional_Amount)
    np_df_Daily_NAV=np.array(df_Daily_NAV)
    df_Daily_NAV_Market_Cap=pd.DataFrame(data=np_df_Daily_NAV*np_Notional_Amount,index=Biz_Dates,columns=KR_Code)/10000
    df_Daily_NAV_Market_Cap.index.name = 'Biz_Dates' # 인덱스 이름지정
    df_Daily_NAV_Market_Cap.columns.name = 'KR_Code' # 칼럼 이름 지정
    # 날짜별 시장가치의 총합임
    df_Daily_NAV_Market_Cap['날짜별발행잔액'] = df_Daily_NAV_Market_Cap.sum(axis=1)
    # 행에서 0이 아닌 종목들의 수를 새로운 칼럼으로 만들어주기
    # 첫 번째 열에 0이 아닌 데이터의 개수를 계산하여 새로운 열 추가
    df_Daily_NAV.insert(0, 'non_zero_count', df_Daily_NAV.astype(bool).sum(axis=1))

    df_Num_ELS = df_Daily_NAV.iloc[0:,0]
    Max_Num_ELS = df_Num_ELS.max()

    ##########################################
    ########### EW indexing
    ###########################################
    # KR코드에 해당한 열만 추출하여 각 행의 총합을 A칼럼으로 추가...전체NAV합계
    df_Daily_NAV['A'] = df_Daily_NAV.filter(regex='^KR').sum(axis=1) #

    # 신규발행 합계 열(B) 만들기...신규발행NAV합계
    df_Daily_NAV['B'] = df_Daily_NAV[df_Daily_NAV.shift(1).eq(0)].filter(regex='^KR').sum(axis=1)

    # C칼럼 만들기...기존발행NAV합계
    df_Daily_NAV['C']=df_Daily_NAV.A-df_Daily_NAV.B

    # 상환종목합계 만들기...상환종목NAV합계
    df_Daily_NAV['D'] = df_Daily_NAV[df_Daily_NAV.shift(-1).eq(0)].filter(regex='^KR').sum(axis=1)

    # F 칼럼 만들기...전체빼기상환종목NAV합계
    df_Daily_NAV['F']=df_Daily_NAV.A-df_Daily_NAV.D

    # E 칼럼 만들기
    # C칼럼과 F칼럼의 데이터에 자연로그 취하기
    df_Daily_NAV['C_log'] = np.log(df_Daily_NAV['C'])
    df_Daily_NAV['F_log_shifted'] = np.log(df_Daily_NAV['F'].shift(1))
    # E칼럼 계산하기
    df_Daily_NAV['E'] = df_Daily_NAV['C_log'] - df_Daily_NAV['F_log_shifted']
    # 불필요한 열 제거하기
    df_Daily_NAV = df_Daily_NAV.drop(['C_log', 'F_log_shifted'], axis=1)

    # G칼럼 만들기...EW Index 값
    # 첫 번째 행의 G값을 1로 설정
    df_Daily_NAV.at[df_Daily_NAV.index[0], 'G'] = 1
    # G칼럼 계산하기
    for i in range(1, len(df_Daily_NAV)):
        df_Daily_NAV.at[df_Daily_NAV.index[i], 'G'] = df_Daily_NAV.at[df_Daily_NAV.index[i - 1], 'G'] + df_Daily_NAV.at[df_Daily_NAV.index[i], 'E']

    # 평균 NAV 수익율 칼럼(H) 작성
    df_Daily_NAV['H']=(df_Daily_NAV['A']/df_Daily_NAV['non_zero_count']-10000)/10000

    ##########################################
    ########### Market cap indexing
    ###########################################
    df_Daily_NAV_Market_Cap['A'] = df_Daily_NAV_Market_Cap.filter(regex='^KR').sum(axis=1)

    # 신규발행 합계 열(B) 만들기
    df_Daily_NAV_Market_Cap['B'] = df_Daily_NAV_Market_Cap[df_Daily_NAV_Market_Cap.shift(1).eq(0)].filter(regex='^KR').sum(axis=1)

    # C칼럼 만들기
    df_Daily_NAV_Market_Cap['C']=df_Daily_NAV_Market_Cap.A-df_Daily_NAV_Market_Cap.B

    # 상환종목합계 만들기
    df_Daily_NAV_Market_Cap['D'] = df_Daily_NAV_Market_Cap[df_Daily_NAV_Market_Cap.shift(-1).eq(0)].filter(regex='^KR').sum(axis=1)

    # F 칼럼 만들기
    df_Daily_NAV_Market_Cap['F']=df_Daily_NAV_Market_Cap.A-df_Daily_NAV_Market_Cap.D

    ######################## E 칼럼 만들기 #############################
    # C칼럼과 F칼럼의 데이터에 자연로그 취하기
    df_Daily_NAV_Market_Cap['C_log'] = np.log(df_Daily_NAV_Market_Cap['C'])
    df_Daily_NAV_Market_Cap['F_log_shifted'] = np.log(df_Daily_NAV_Market_Cap['F'].shift(1))
    # E칼럼 계산하기
    df_Daily_NAV_Market_Cap['E'] = df_Daily_NAV_Market_Cap['C_log'] - df_Daily_NAV_Market_Cap['F_log_shifted']
    # 불필요한 열 제거하기
    df_Daily_NAV_Market_Cap = df_Daily_NAV_Market_Cap.drop(['C_log', 'F_log_shifted'], axis=1)

    ######################## G 칼럼 만들기 #############################
    # 첫 번째 행의 G값을 1로 설정
    df_Daily_NAV_Market_Cap.at[df_Daily_NAV_Market_Cap.index[0], 'G'] = 1
    # G칼럼 계산하기
    for i in range(1, len(df_Daily_NAV_Market_Cap)):
        df_Daily_NAV_Market_Cap.at[df_Daily_NAV_Market_Cap.index[i], 'G'] = \
        df_Daily_NAV_Market_Cap.at[df_Daily_NAV_Market_Cap.index[i - 1], 'G'] +\
        df_Daily_NAV_Market_Cap.at[df_Daily_NAV_Market_Cap.index[i], 'E']

     ##########################################
     ########### 산 자 분석
     ###########################################

     # 인덱스에 함수 적용하여 새로운 열들 추가
    for index, row in df_Daily_NAV.iterrows():
        result,min_Ret_index,max_Ret_index = stats_for_alives(df_Daily_NAV,index)  # 인덱스에 함수 적용
        for column_name, value in result.items():
            df_Daily_NAV.at[index, f'Alive_{column_name}'] = value  # 새로운 열들 추가
        df_Daily_NAV.at[index, 'min_Return_KR_code'] = min_Ret_index
        df_Daily_NAV.at[index, 'min_Return_issued_date']=df_issued_summary.at[min_Ret_index,'발행일'].strftime('%Y-%m-%d')
        df_Daily_NAV.at[index, 'max_Return_KR_code'] = max_Ret_index
        df_Daily_NAV.at[index, 'max_Return_issued_date']=df_issued_summary.at[max_Ret_index,'발행일'].strftime('%Y-%m-%d')

    # monthly data 추출
    df_alive_stats=df_Daily_NAV.resample('M').last().iloc[:,-12:]
    # 날짜 포맷 변경
    df_alive_stats.index = pd.to_datetime(df_alive_stats.index)
    df_alive_stats.index = df_alive_stats.index.strftime('%Y-%m-%d')

     ##########################################
     ########### 죽은 자 분석
     ###########################################

    # 매월 말일의 인덱스 선택
    monthly_end_index = df_Daily_NAV.resample('M').last().index

    # 빈 데이터프레임 생성
    df_for_redeemed = pd.DataFrame(index=monthly_end_index)

    for date in monthly_end_index:
        date_str = date.strftime('%Y-%m-%d')  # 날짜를 문자열로 변환
        D,ABS,PA,pos_ret_abs,neg_ret_abs,pos_ret_pa,neg_ret_pa,min_duration,max_duration,min_pa_return,max_pa_return = stats_for_redeemed(df_Daily_NAV,date_str)
        if D is not None:
            for column_name, value in D.items():
                df_for_redeemed.at[date, f'Durations_{column_name}'] = value  # 새로운 열들 추가
            for column_name, value in ABS.items():
                df_for_redeemed.at[date, f'abs_ret_{column_name}'] = value  # 새로운 열들 추가
            for column_name, value in PA.items():
                df_for_redeemed.at[date, f'p.a._ret_{column_name}'] = value  # 새로운 열들 추가
            for column_name, value in pos_ret_abs.items():
                df_for_redeemed.at[date, f'(+)abs_ret_{column_name}'] = value  # 새로운 열들 추가
            for column_name, value in neg_ret_abs.items():
                df_for_redeemed.at[date, f'(-)abs_ret_{column_name}'] = value  # 새로운 열들 추가
            for column_name, value in pos_ret_pa.items():
                df_for_redeemed.at[date, f'(+)p.a._ret_{column_name}'] = value  # 새로운 열들 추가
            for column_name, value in neg_ret_pa.items():
                df_for_redeemed.at[date, f'(-)p.a._ret_{column_name}'] = value  # 새로운 열들 추가
            df_for_redeemed.at[date, 'min_duration_KR_code'] = min_duration
            df_for_redeemed.at[date, 'min_duration_issued_date']=df_issued_summary.at[min_duration,'발행일'].strftime('%Y-%m-%d')
            df_for_redeemed.at[date, 'max_duration_KR_code'] = max_duration
            df_for_redeemed.at[date, 'max_duration_issued_date']=df_issued_summary.at[max_duration,'발행일'].strftime('%Y-%m-%d')
            df_for_redeemed.at[date, 'min_pareturn_KR_code'] = min_pa_return
            df_for_redeemed.at[date, 'min_pareturn_issued_date']=df_issued_summary.at[min_pa_return,'발행일'].strftime('%Y-%m-%d')
            df_for_redeemed.at[date, 'max_pareturn_KR_code'] = max_pa_return
            df_for_redeemed.at[date, 'max_pareturn_issued_date']=df_issued_summary.at[max_pa_return,'발행일'].strftime('%Y-%m-%d')

    # 날짜 포맷 변경
    df_for_redeemed.index = pd.to_datetime(df_for_redeemed.index)
    df_for_redeemed.index = df_for_redeemed.index.strftime('%Y-%m-%d')


     ##########################################
     ########### 특정 날짜에서 발행된 종목수, 발행금액 보기
     ###########################################

    # 발행 정보를 분석하기 위한 새로운 데이터프레임 만들기
    issued_date=df_Issuance_Info.iloc[13,2:]
    issued_date = pd.to_datetime(issued_date) # 날짜형식으로 변환
    # 인덱스를 초기화하여 시리즈 재설정
    issued_date = issued_date.reset_index(drop=True)
    Notional_Amount = Notional_Amount.reset_index(drop=True)
    df_issued_summary=pd.DataFrame(data={'발행일':issued_date,'발행총액':Notional_Amount})
    df_issued_summary.index=KR_Code
    df_issued_summary.index.name='KR code'

    # df_Daily_NAV의 날짜 인덱스를 기반으로 새로운 열 생성
    df_Daily_NAV[['발행된ELS종목수', '발행총액_합계']] = df_Daily_NAV.index.to_series().apply(
        lambda date: pd.Series(get_issue_amount(df_issued_summary, date)))
    df_Daily_NAV[['발행된ELS종목수', '발행총액_합계']]
    # 발행총액을 10억 단위로 변환
    df_Daily_NAV['발행총액(10억)'] = df_Daily_NAV['발행총액_합계'] / 1e+9

    ##########################################
    ########### 특정 날짜에서 상환된 종목수, 발행금액 보기
    ###########################################

    # df_Daily_NAV의 날짜 인덱스를 기반으로 새로운 열 생성
    # 날짜마다 상환되는 것을 계산하느라 시간 많이 걸림
    df_Daily_NAV[['상환된ELS종목수', '상환된발행액_합계(10억)']] = df_Daily_NAV.index.to_series().apply(
        lambda date: pd.Series(info_for_redeemed(df_Daily_NAV_Market_Cap,df_issued_summary,date)))
    df_Daily_NAV[['상환된ELS종목수', '상환된발행액_합계(10억)']]

    ##########################################
    ########### Sharpe Ratio
    ###########################################

    rf=0.05 # 금리 세팅

    # 매월 말일의 인덱스 선택
    monthly_end_index = df_Daily_NAV.resample('M').last().index

    # 빈 데이터프레임 생성
    df_Sharpe_for_redeemed = pd.DataFrame(index=monthly_end_index)

    for date in monthly_end_index:
        date_str = date.strftime('%Y-%m-%d')  # 날짜를 문자열로 변환
        results=sharpe_ratio_for_redeemed(df_Daily_NAV,rf,date_str).describe()
        for column_name, value in results.items():
              df_Sharpe_for_redeemed.at[date, f'SharpeR_{column_name}'] = value  # 새로운 열들 추가


    ##########################################
    ########### PPT 자료 작성하기: Colab
    ###########################################
    from pandas_datareader import data as pdr
    import yfinance as yfin

    file_out_ppt= '/content/drive/MyDrive/PPT_Output.xlsx'

    # Daily info 정리하기
    df_Daily_NAV_summary=df_Daily_NAV.iloc[:, [0] + list(range(-17, 0))] # 처음과 마지막 17개의 칼럼만 추출
    imsi=df_Daily_NAV_Market_Cap['날짜별발행잔액']/1e+9
    df_Daily_NAV_summary.loc[:, '시장가치잔액(10억)'] = imsi


    # 칼럼 위치 조정
    # 'non_zero_count' 칼럼을 삭제한 후, 맨 뒤에서 두 번째 위치에 다시 삽입
    cols = list(df_Daily_NAV_summary.columns)
    cols.remove('non_zero_count')  # non_zero_count 칼럼을 제외한 나머지 칼럼들의 순서를 정함
    cols.insert(-1, 'non_zero_count')  # non_zero_count 칼럼을 원하는 위치에 삽입
    df_Daily_NAV_summary = df_Daily_NAV_summary[cols]  # 새로운 칼럼 순서로 데이터프레임을 재구성

    # 중복칼럼 삭제
    df_Daily_NAV_summary.drop(columns=['발행총액_합계'],inplace=True)

    # Column Rename
    df_Daily_NAV_summary = df_Daily_NAV_summary.rename(columns={'non_zero_count': '잔존 ELS 종목수'})

    # 날짜 포맷 변경
    df_Daily_NAV_summary.index = pd.to_datetime(df_Daily_NAV_summary.index)
    df_Daily_NAV_summary.index = df_Daily_NAV_summary.index.strftime('%Y-%m-%d')
    df_daily_stats=df_Daily_NAV_summary.drop(columns=['Alive_25%','Alive_75%'])
    df_daily_stats['EW Index']=df_Daily_NAV['G']
    df_daily_stats['Market Cap Index']=df_Daily_NAV_Market_Cap['G']
    last_two_columns = df_daily_stats.iloc[:, -2:]  # 마지막 두 개의 칼럼 선택
    df_daily_stats.drop(df_daily_stats.columns[-2:], axis=1, inplace=True)  # 마지막 두 개의 칼럼 삭제
    df_daily_stats = pd.concat([last_two_columns, df_daily_stats], axis=1)  # 마지막 두 개의 칼럼을 맨 앞으로 이동
    last_six_columns = df_daily_stats.iloc[:, -6:]  # 마지막 여섯 개의 칼럼 선택
    df_daily_stats.drop(df_daily_stats.columns[-6:], axis=1, inplace=True)  # 마지막 여섯 개의 칼럼 삭제
    df_daily_stats = pd.concat([df_daily_stats.iloc[:, :2], last_six_columns, df_daily_stats.iloc[:, 2:]], axis=1)  # 칼럼 삽입

    # Monthly info 정리하기
    df_monthly_stats_for_redeemed=df_for_redeemed
    selected_columns = df_monthly_stats_for_redeemed.iloc[:, 22:26]
    df_monthly_stats_for_redeemed.drop(df_monthly_stats_for_redeemed.columns[22:26], axis=1, inplace=True)
    df_monthly_stats_for_redeemed = pd.concat([df_monthly_stats_for_redeemed.iloc[:, :4], selected_columns, df_monthly_stats_for_redeemed.iloc[:, 4:]], axis=1)
    selected_columns = df_monthly_stats_for_redeemed.iloc[:, -4:]
    df_monthly_stats_for_redeemed.drop(df_monthly_stats_for_redeemed.columns[-4:], axis=1, inplace=True)
    df_monthly_stats_for_redeemed = pd.concat([df_monthly_stats_for_redeemed.iloc[:, :11], selected_columns, df_monthly_stats_for_redeemed.iloc[:, 11:]], axis=1)
    df_monthly_stats_for_redeemed['SharpeR_mean']=df_Sharpe_for_redeemed['SharpeR_mean']
    df_monthly_stats_for_redeemed['SharpeR_std']=df_Sharpe_for_redeemed['SharpeR_std']


    with pd.ExcelWriter(file_out_ppt) as writer:
        df_daily_stats_01=df_daily_stats[['발행된ELS종목수','발행총액(10억)']]
        df_daily_stats_01_summary=df_daily_stats_01.describe().loc[['min','mean', '50%','max']]
        df_daily_stats_01_summary.to_excel(writer, sheet_name='#1. 발행종목수&금액')
        df_daily_stats_01.to_excel(writer, sheet_name='#1. 발행종목수&금액',startrow=10)

        df_daily_stats_02=df_daily_stats[['EW Index','Market Cap Index']]
        df_daily_stats_02_summary=df_daily_stats_02.describe().loc[['min','mean', '50%','max']]
        df_daily_stats_02_summary.to_excel(writer, sheet_name='#2. ELS Index')
        df_daily_stats_02.to_excel(writer, sheet_name='#2. ELS Index',startrow=10)

        df_daily_stats_04=df_daily_stats[['EW Index','잔존 ELS 종목수']]
        df_daily_stats_04_summary=df_daily_stats_04.describe().loc[['min','mean', '50%','max']]
        df_daily_stats_04_summary.to_excel(writer, sheet_name='#4. EW&해당ELS')
        df_daily_stats_04.to_excel(writer, sheet_name='#4. EW&해당ELS',startrow=10)

        # 데이터프레임 생성
        total_issued=df_daily_stats_01_summary.iloc[3,0]
        df_t_issued = pd.DataFrame({'A':['발행된ELS종목수'],'B':[total_issued]})
        df_t_issued.to_excel(writer, sheet_name='#5.상환비율', startrow=0, startcol=1, index=False, header=None)

        df_daily_stats_05=df_monthly_stats_for_redeemed[['Durations_count']]
        df_daily_stats_05.rename(columns={'Durations_count':'조기/만기상환갯수'},inplace=True)
        df_daily_stats_05['조기/만기상환비율']=df_daily_stats_05['조기/만기상환갯수']/total_issued
        df_daily_stats_05=df_daily_stats_05.loc[:, ['조기/만기상환비율', '조기/만기상환갯수']]
        df_daily_stats_05.to_excel(writer, sheet_name='#5.상환비율',startrow=10)


        df_daily_stats_06=df_daily_stats_05['조기/만기상환비율']
        df_daily_stats_06 = pd.concat([df_daily_stats_06, df_monthly_stats_for_redeemed['p.a._ret_mean']], axis=1)
        df_daily_stats_06.rename(columns={'p.a._ret_mean':'평균 연환산 수익율'},inplace=True)
        df_t_issued.to_excel(writer, sheet_name='#6.상환비율&연환산수익율', startrow=0, startcol=1, index=False, header=None)
        df_daily_stats_06.to_excel(writer, sheet_name='#6.상환비율&연환산수익율',startrow=10)

        df_daily_stats_06_01 =pd.concat([df_daily_stats_06, df_monthly_stats_for_redeemed[['Durations_mean','(+)abs_ret_count']]], axis=1)
        df_daily_stats_06_01['+상환비율']=df_daily_stats_06_01['(+)abs_ret_count']/total_issued
        df_daily_stats_06_01.drop(columns=['(+)abs_ret_count'],inplace=True)
        df_daily_stats_06_01 =pd.concat([df_daily_stats_06_01, df_monthly_stats_for_redeemed[['min_pareturn_KR_code','max_pareturn_KR_code']]], axis=1)
        df_t_issued.to_excel(writer, sheet_name='#6.참고', startrow=0, startcol=1, index=False, header=None)
        df_daily_stats_06_01.to_excel(writer, sheet_name='#6.참고',startrow=10)

        #############################################################
        ############## 상환된 자료 분석 #############################
        #############################################################
        # 데이터의 마지막 인덱 날짜를 찾기
        final_date=df_daily_stats.index[-1]
        out=hist_for_redeemded(df_Daily_NAV,final_date)
        out_stats=out.describe().loc[['min','mean', '50%','max']]
        df_out_stats=pd.DataFrame(out_stats)
        df_out_stats.rename(columns={'p.a.return':'연환산 수익율'},inplace=True)
        min_redeemed_code=out.idxmin()
        max_redeemed_code=out.idxmax()
        df_out_stats['해당 KR Code 값']=[min_redeemed_code,np.nan,np.nan,max_redeemed_code]
        df_stats_07=pd.DataFrame(out)
        df_stats_07.rename(columns={'p.a.return':'연환산 수익율'},inplace=True)
        df_final_date = pd.DataFrame({'A':['기준일'],'B':[final_date]})
        df_final_date.to_excel(writer, sheet_name='#7.상환완료된 ELS 연환산수익율 분포', startrow=0, startcol=0, index=False, header=None)
        df_out_stats.to_excel(writer,sheet_name='#7.상환완료된 ELS 연환산수익율 분포',startrow=2)
        df_stats_07.to_excel(writer,sheet_name='#7.상환완료된 ELS 연환산수익율 분포',startrow=10)

        # Worst Performer 분석
        NAVs = df_Daily_NAV.loc[df_Daily_NAV[min_redeemed_code] != 0, min_redeemed_code]
        df_Worst=pd.DataFrame(NAVs)/10000
        df_Worst.rename(columns={ min_redeemed_code:'ELS % NAV'},inplace=True)
        # 날짜 포맷 변경
        df_Worst.index = pd.to_datetime(df_Worst.index)
        df_Worst.index = df_Worst.index.strftime('%Y-%m-%d')

        df_Issuance_Info.columns=df_Issuance_Info.iloc[7,:] # 칼럼 네이밍
        Issuers=df_Issuance_Info.iloc[9][min_redeemed_code] #발행사 정보
        Underlyings=list(df_Issuance_Info.iloc[24:28][min_redeemed_code]) #기초자산 정보
        Worst_info=[]
        Worst_info.append(min_redeemed_code)
        Worst_info.append(Issuers)
        Worst_info.extend(Underlyings) # 리스트 병합
        df_Worst_info=pd.DataFrame(data=Worst_info)
        df_Worst_info.index=['KR Code','발행증권사','기초자산1','기초자산2','기초자산3','기초자산4']
        df_final_date.to_excel(writer, sheet_name='#8.Worst-Performer', startrow=0, startcol=0, index=False, header=None)
        df_Worst_info.to_excel(writer, sheet_name='#8.Worst-Performer', startrow=2,header=None)
        df_Worst.to_excel(writer, sheet_name='#8.Worst-Performer', startrow=10)

        # Best Performer 분석
        NAVs = df_Daily_NAV.loc[df_Daily_NAV[max_redeemed_code] != 0, max_redeemed_code]
        df_Best=pd.DataFrame(NAVs)/10000
        df_Best.rename(columns={ max_redeemed_code:'ELS % NAV'},inplace=True)
        # 날짜 포맷 변경
        df_Best.index = pd.to_datetime(df_Best.index)
        df_Best.index = df_Best.index.strftime('%Y-%m-%d')

        Issuers=df_Issuance_Info.iloc[9][max_redeemed_code] #발행사 정보
        Underlyings=list(df_Issuance_Info.iloc[24:28][max_redeemed_code]) #기초자산 정보
        Best_info=[]
        Best_info.append(max_redeemed_code)
        Best_info.append(Issuers)
        Best_info.extend(Underlyings) # 리스트 병합
        df_Best_info=pd.DataFrame(data=Best_info)
        df_Best_info.index=['KR Code','발행증권사','기초자산1','기초자산2','기초자산3','기초자산4']
        df_final_date.to_excel(writer, sheet_name='#9.Best-Performer', startrow=0, startcol=0, index=False, header=None)
        df_Best_info.to_excel(writer, sheet_name='#9.Best-Performer', startrow=2,header=None)
        df_Best.to_excel(writer, sheet_name='#9.Best-Performer', startrow=10)

        #############################################################
        ############## Outstanding 자료 분석 ########################
        #############################################################
        df_Alives=pa_return_for_alives(df_Daily_NAV,final_date) # 새로 작성한 함수 호출

        out1=df_Alives['연환산수익율']
        out_stats1=out1.describe().loc[['min','mean', '50%','max']]
        df_out_stats_1=pd.DataFrame(out_stats1)
        min_code=out1.idxmin()
        max_code=out1.idxmax()
        df_out_stats_1['해당 KR Code 값']=[min_code,np.nan,np.nan,max_code]
        df_stats_10=pd.DataFrame(out1)
        df_final_date.to_excel(writer, sheet_name='#10.살아있는 ELS 수익율 분포', startrow=0, startcol=0, index=False, header=None)
        df_out_stats_1.to_excel(writer,sheet_name='#10.살아있는 ELS 수익율 분포',startrow=2)
        df_stats_10.to_excel(writer,sheet_name='#10.살아있는 ELS 수익율 분포',startrow=10)

        # Worst Performer 분석
        NAVs = df_Daily_NAV.loc[df_Daily_NAV[min_code] != 0, min_code]
        df_Worst_alive=pd.DataFrame(NAVs)/10000
        df_Worst_alive.rename(columns={ min_code:'ELS % NAV'},inplace=True)
        # 날짜 포맷 변경
        df_Worst_alive.index = pd.to_datetime(df_Worst_alive.index)
        df_Worst_alive.index = df_Worst_alive.index.strftime('%Y-%m-%d')

        Issuers=df_Issuance_Info.iloc[9][min_code] #발행사 정보
        Underlyings=list(df_Issuance_Info.iloc[24:28][min_code]) #기초자산 정보
        Worst_alive_info=[]
        Worst_alive_info.append(min_code)
        Worst_alive_info.append(Issuers)
        Worst_alive_info.extend(Underlyings) # 리스트 병합
        df_Worst_alive_info=pd.DataFrame(data=Worst_alive_info)
        df_Worst_alive_info.index=['KR Code','발행증권사','기초자산1','기초자산2','기초자산3','기초자산4']
        df_final_date.to_excel(writer, sheet_name='#11.Worst-Performer', startrow=0, startcol=0, index=False, header=None)
        df_Worst_alive_info.to_excel(writer, sheet_name='#11.Worst-Performer', startrow=2,header=None)
        df_Worst_alive.to_excel(writer, sheet_name='#11.Worst-Performer', startrow=10)

        # Best Performer 분석
        NAVs = df_Daily_NAV.loc[df_Daily_NAV[max_code] != 0, max_code]
        df_alive_Best=pd.DataFrame(NAVs)/10000
        df_alive_Best.rename(columns={ max_code:'ELS % NAV'},inplace=True)
        # 날짜 포맷 변경
        df_alive_Best.index = pd.to_datetime(df_alive_Best.index)
        df_alive_Best.index = df_alive_Best.index.strftime('%Y-%m-%d')

        Issuers=df_Issuance_Info.iloc[9][max_code] #발행사 정보
        Underlyings=list(df_Issuance_Info.iloc[24:28][max_code]) #기초자산 정보
        Best_alive_info=[]
        Best_alive_info.append(max_code)
        Best_alive_info.append(Issuers)
        Best_alive_info.extend(Underlyings) # 리스트 병합
        df_Best_alive_info=pd.DataFrame(data=Best_alive_info)
        df_Best_alive_info.index=['KR Code','발행증권사','기초자산1','기초자산2','기초자산3','기초자산4']
        df_final_date.to_excel(writer, sheet_name='#12.Best-Performer', startrow=0, startcol=0, index=False, header=None)
        df_Best_alive_info.to_excel(writer, sheet_name='#12.Best-Performer', startrow=2,header=None)
        df_alive_Best.to_excel(writer, sheet_name='#12.Best-Performer', startrow=10)

        #############################################################
        ################# 기초자산 불러오기 ########################
        #############################################################
        import datetime
        # 조회날짜 설정
        start=df_daily_stats.index[0]
        date_str = final_date
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')  # 문자열을 datetime 객체로 변환합니다.
        date_obj_plus_one_day = date_obj + datetime.timedelta(days=1)  # 날짜에 하루를 더해줍니다.
        end=date_obj_plus_one_day.strftime('%Y-%m-%d')

        yfin.pdr_override()
        tickers=['^KS200','^HSCE','^N225','^SPX','^STOXX50E','TSLA','AMD','NVDA','005930.KS','005380.KS']

        data = {}
        for t in tickers:
            data[t]=pdr.get_data_yahoo(t,start=start,end=end)['Close']
        df_underlyings=pd.DataFrame(data)

        # 없는 데이터 채우기
        df_underlyings = df_underlyings.fillna(method='ffill') # 빈 데이터는 앞데이터로
        df_underlyings = df_underlyings.fillna(method='bfill') # 앞에도 없으면 뒤데이터로

        # 날짜 포맷 변경
        df_underlyings.index = pd.to_datetime(df_underlyings.index)
        df_underlyings.index = df_underlyings.index.strftime('%Y-%m-%d')

        # 통계량 작성
        out_stats_underlying=df_underlyings.describe().loc[['min','mean', '50%','max']]
        df_out_stats_underlying=pd.DataFrame(out_stats_underlying)

        # 엑셀 쉬트에 집어넣기
        df_underlyings.to_excel(writer, sheet_name='#13.Underlyings', startrow=10)
        df_out_stats_underlying.to_excel(writer, sheet_name='#13.Underlyings')


        #############################################################
        ################# #3번째 웍쉿 작성  ########################
        #############################################################
        df_daily_stats_03=df_daily_stats[['EW Index']]
        df_daily_stats_03_summary=df_daily_stats_03.describe().loc[['min','mean', '50%','max']]

        # 데이터 타입 확인 및 변환
        df_daily_stats_03.index = df_daily_stats_03.index.astype(str)
        df_underlyings.index = df_underlyings.index.astype(str)

        # 인덱스 정렬
        df_daily_stats_03 = df_daily_stats_03.sort_index()
        df_underlyings = df_underlyings.sort_index()

        # 인덱스 이름 확인 및 변경
        df_daily_stats_03 = df_daily_stats_03.rename_axis('date')
        df_underlyings = df_underlyings.rename_axis('date')

        # 각 주가를 정규화시키기
        df_underlyings=df_underlyings.iloc[:, :5] #첫 5개의 칼럼만 발췌
        df_normalized = df_underlyings / df_underlyings.iloc[0,:]

        # 정규화된 주가의 통계량 구하기
        out_stats_underlying=df_normalized.describe().loc[['min','mean', '50%','max']]
        df_out_stats_underlying=pd.DataFrame(out_stats_underlying)

        # 통계량 병합
        df_daily_stats_03_summary=pd.concat([df_daily_stats_03_summary, df_out_stats_underlying], axis=1, join='inner')
        df_daily_stats_03_summary.to_excel(writer, sheet_name='#3. ELS&GEI')

        # 병합
        merged_df = df_daily_stats_03.merge(df_normalized, left_index=True, right_index=True, how='inner')
        merged_df.to_excel(writer, sheet_name='#3. ELS&GEI',startrow=10)

    # 웍쉬트 위치 변경

    from openpyxl import load_workbook

    # 엑셀 파일을 로드합니다.
    workbook = load_workbook(file_out_ppt)
    sheets = workbook.sheetnames
    last_sheet = workbook[sheets[-1]]  # 마지막 워크시트 객체 가져오기

    # 마지막 워크시트를 세 번째 위치로 이동시킵니다.
    workbook.move_sheet(last_sheet, offset=-11)

    # 변경 사항을 저장합니다.
    workbook.save(file_out_ppt)

    return None

############################################################################
############################################################################
############################################################################

def remove_consecutive_zeros(df):
    import pandas as pd
    # 첫 번째 행이 모두 0인 경우 삭제
    if (df.iloc[0] == 0).all():
        df.drop(df.index[0], inplace=True)
        # 재귀적으로 함수 호출하여 다음 첫 번째 행이 모두 0인 경우도 확인하고 삭제
        remove_consecutive_zeros(df)


def stats_for_alives(df_Daily_NAV,date0):
    import pandas as pd
    kr_cols= df_Daily_NAV.loc[date0].filter(regex=r'^KR')
    # 해당 칼럼에서 값이 0이 아닌 칼럼을 추출
    DD = kr_cols[kr_cols != 0] # 살아있는 넘들의 NAV
    if not DD.empty:
      Ret = (DD-10000)/100 # 리턴값(100% 환산값)
      Ret = Ret.astype('float64')
      # Ret_D 시리즈에서 최소값과 최대값에 해당하는 인덱스 찾기
      min_Ret_index = Ret.idxmin()
      max_Ret_index = Ret.idxmax()
      return Ret.describe(),min_Ret_index,max_Ret_index

    else:
      return None,None,None


def pa_return_for_alives(df_Daily_NAV,final_date):
    import pandas as pd
    kr_cols= df_Daily_NAV.loc[final_date].filter(regex=r'^KR')
    # 해당 칼럼에서 값이 0이 아닌 칼럼을 추출
    DD = kr_cols[kr_cols != 0] # 살아있는 넘들의 NAV
    df_alives=pd.DataFrame(DD)
    df_alives.rename(columns={},inplace=True) # 칼럼이름 지우기
    df_alives.columns=['조회된 날짜'] # 이름 새로 짓기
  
    for code in df_alives.index:
      first_date = df_Daily_NAV[code][df_Daily_NAV[code] != 0].first_valid_index()
      duration = (pd.to_datetime(final_date) - first_date).days
      df_alives.at[code,'발행일']=first_date
      df_alives.at[code,'Duration']=duration
      Ret= (df_alives.at[code,'조회된 날짜']-10000)/10000
      Ret_pa=(1+Ret)**(365/duration)-1
      df_alives.at[code,'절대수익율']=Ret
      df_alives.at[code,'연환산수익율']=Ret_pa

    return df_alives


def stats_for_redeemed(df_Daily_NAV,input_date):
    import pandas as pd
    
    # date가 인덱스에 있는지 확인
    if input_date not in df_Daily_NAV.index: # 인덱스에 없는 날짜라면
        input_date=df_Daily_NAV.index[df_Daily_NAV.index < input_date].max() # 가장 가까운 앞 날짜 추출
    else: # 인덱스에 있다면 그냥 날짜객체로 반환
        input_date=pd.Timestamp(input_date)

    # 특정일을 나타내는 행에서 그 값이 0인 것들중 칼럼 이름이 KR로 시작하는 것들을 Series로 추출함
    zeros=df_Daily_NAV.loc[input_date][df_Daily_NAV.loc[input_date] == 0].filter(regex='^KR')

    # 빈 데이터프레임 생성
    df_redeemed = pd.DataFrame(columns=zeros.index)

    for col in zeros.index:
        non_zero_values = df_Daily_NAV.loc[df_Daily_NAV[col] != 0, col]
        last_non_zero_index = non_zero_values.index[-1]
        # 만일 최종일의 날짜가 입력값보다 크면 상환된 종목이 아님을 의미한다.
        # 추가로 len(non_zero_values)이 0이어도 대상이 아니다.
        if (last_non_zero_index > input_date) or (len(non_zero_values)==0):
            df_redeemed.drop(columns=[col],inplace=True) # 해당 코드 삭제
            continue # 다음 칼럼으로 이동

        first_non_zero_index = non_zero_values.index[0]
        first_non_zero_value = 10000 # 10000으로 통일
        last_non_zero_value = non_zero_values.iloc[-1]
        duration = (last_non_zero_index - first_non_zero_index).days
        Ret_abs=last_non_zero_value/first_non_zero_value-1
        Ret_pa=(1+Ret_abs)**(365/duration)-1
        df_redeemed[df_redeemed.columns[df_redeemed.columns.get_loc(col)]] =\
        [first_non_zero_value, last_non_zero_value, duration, Ret_abs, Ret_pa]

    if not df_redeemed.empty:
        ret_abs=df_redeemed.iloc[3] # abs return의 정보
        ret_abs=pd.Series(ret_abs)

        ret_pa=df_redeemed.iloc[4] # per annum return의 정보
        ret_pa=pd.Series(ret_pa)

        durations=df_redeemed.iloc[2]
        durations=pd.Series(durations)

        # 양수와 음수의 경우를 따로 집계
        pos_ret_abs = ret_abs[ret_abs > 0]
        neg_ret_abs = ret_abs[ret_abs < 0]

        pos_ret_pa = ret_pa[ret_pa > 0]
        neg_ret_pa = ret_pa[ret_pa < 0]

        # durations 시리즈에서 최솟값과 최댓값에 해당하는 인덱스 찾기
        min_duration_index = durations.idxmin()
        max_duration_index = durations.idxmax()

        # ret_pa 시리즈에서 최솟값과 최댓값에 해당하는 인덱스 찾기
        min_ret_pa_index = ret_pa.idxmin()
        max_ret_pa_index = ret_pa.idxmax()

    else: # df_redeemed가 비어있다면 아무것도 출력하지 않음
        return None,None,None, None, None,None,None,None,None,None,None

    return (durations.describe()[['count', 'mean', 'std','50%']],
            ret_abs.describe()[['mean', 'std','50%']],
            ret_pa.describe()[['mean', 'std','50%']],
            pos_ret_abs.describe()[['count','mean', 'std']],
            neg_ret_abs.describe()[['count','mean', 'std']],
            pos_ret_pa.describe()[['count','mean', 'std']],
            neg_ret_pa.describe()[['count','mean', 'std']],
            min_duration_index,
            max_duration_index,
            min_ret_pa_index,
            max_ret_pa_index)

# 함수 작성
def stats_for_redeemed_old(df_Daily_NAV,input_date):
    import pandas as pd
    # date가 인덱스에 있는지 확인
    if input_date not in df_Daily_NAV.index: # 인덱스에 없는 날짜라면
        input_date=df_Daily_NAV.index[df_Daily_NAV.index < input_date].max() # 가장 가까운 앞 날짜 추출
    else: # 인덱스에 있다면 그냥 날짜객체로 반환
        input_date=pd.Timestamp(input_date)

    # 특정일을 나타내는 행에서 그 값이 0인 것들중 칼럼 이름이 KR로 시작하는 것들을 Series로 추출함
    zeros=df_Daily_NAV.loc[input_date][df_Daily_NAV.loc[input_date] == 0].filter(regex='^KR')

    # 빈 데이터프레임 생성
    df_redeemed = pd.DataFrame(columns=zeros.index)

    for col in zeros.index:
        non_zero_values = df_Daily_NAV.loc[df_Daily_NAV[col] != 0, col]
        last_non_zero_index = non_zero_values.index[-1]
        # 만일 최종일의 날짜가 입력값보다 크면 상환된 종목이 아님을 의미한다.
        # 추가로 len(non_zero_values)이 0이어도 대상이 아니다.
        if (last_non_zero_index > input_date) or (len(non_zero_values)==0):
            df_redeemed.drop(columns=[col],inplace=True) # 해당 코드 삭제
            continue # 다음 칼럼으로 이동

        first_non_zero_index = non_zero_values.index[0]
        first_non_zero_value = 10000 # 10000으로 통일
        last_non_zero_value = non_zero_values.iloc[-1]
        duration = (last_non_zero_index - first_non_zero_index).days
        Ret_abs=last_non_zero_value/first_non_zero_value-1
        Ret_pa=(1+Ret_abs)**(365/duration)-1
        df_redeemed[df_redeemed.columns[df_redeemed.columns.get_loc(col)]] =\
        [first_non_zero_value, last_non_zero_value, duration, Ret_abs, Ret_pa]

    if not df_redeemed.empty:
        ret_abs=df_redeemed.iloc[3] # abs return의 정보
        ret_abs=pd.Series(ret_abs)

        ret_pa=df_redeemed.iloc[4] # per annum return의 정보
        ret_pa=pd.Series(ret_pa)

        durations=df_redeemed.iloc[2]
        durations=pd.Series(durations)

        # 양수와 음수의 경우를 따로 집계
        pos_ret_abs = ret_abs[ret_abs > 0]
        neg_ret_abs = ret_abs[ret_abs < 0]

        pos_ret_pa = ret_pa[ret_pa > 0]
        neg_ret_pa = ret_pa[ret_pa < 0]

        # durations 시리즈에서 최솟값과 최댓값에 해당하는 인덱스 찾기
        min_duration_index = durations.idxmin()
        max_duration_index = durations.idxmax()

        # ret_abs 시리즈에서 최솟값과 최댓값에 해당하는 인덱스 찾기
        min_ret_abs_index = ret_abs.idxmin()
        max_ret_abs_index = ret_abs.idxmax()

    else: # df_redeemed가 비어있다면 아무것도 출력하지 않음
        return None,None,None, None, None,None,None,None,None,None,None

    return (durations.describe()[['count', 'mean', 'std','50%']],
            ret_abs.describe()[['mean', 'std','50%']],
            ret_pa.describe()[['mean', 'std','50%']],
            pos_ret_abs.describe()[['count','mean', 'std']],
            neg_ret_abs.describe()[['count','mean', 'std']],
            pos_ret_pa.describe()[['count','mean', 'std']],
            neg_ret_pa.describe()[['count','mean', 'std']],
            min_duration_index,
            max_duration_index,
            min_ret_abs_index,
            max_ret_abs_index)


def hist_for_redeemded(df_Daily_NAV,input_date):
  import matplotlib.pyplot as plt
  import pandas as pd

  # date가 인덱스에 있는지 확인
  if input_date not in df_Daily_NAV.index: # 인덱스에 없는 날짜라면
      input_date=df_Daily_NAV.index[df_Daily_NAV.index < input_date].max() # 가장 가까운 앞 날짜 추출
  else: # 인덱스에 있다면 그냥 날짜객체로 반환
      input_date=pd.Timestamp(input_date)

  # 특정일을 나타내는 행에서 그 값이 0인 것들중 칼럼 이름이 KR로 시작하는 것들을 Series로 추출함
  zeros=df_Daily_NAV.loc[input_date][df_Daily_NAV.loc[input_date] == 0].filter(regex='^KR')

  # 빈 데이터프레임 생성
  df_redeemed = pd.DataFrame(columns=zeros.index)

  for col in zeros.index:
      non_zero_values = df_Daily_NAV.loc[df_Daily_NAV[col] != 0, col]
      last_non_zero_index = non_zero_values.index[-1]
      # 만일 최종일의 날짜가 입력값보다 크면 상환된 종목이 아님을 의미한다.
      # 추가로 len(non_zero_values)이 0이어도 대상이 아니다.
      if (last_non_zero_index > input_date) or (len(non_zero_values)==0):
          df_redeemed.drop(columns=[col],inplace=True) # 해당 코드 삭제
          continue # 다음 칼럼으로 이동

      first_non_zero_index = non_zero_values.index[0]
      first_non_zero_value = 10000 # 10000으로 통일
      last_non_zero_value = non_zero_values.iloc[-1]
      duration = (last_non_zero_index - first_non_zero_index).days
      Ret_abs=last_non_zero_value/first_non_zero_value-1
      Ret_pa=(1+Ret_abs)**(365/duration)-1
      df_redeemed[df_redeemed.columns[df_redeemed.columns.get_loc(col)]] =\
      [first_non_zero_value, last_non_zero_value, duration, Ret_abs, Ret_pa]

  ror_for_redeemed=df_redeemed.iloc[4,:]
  ror_for_redeemed.name='p.a.return'

  return ror_for_redeemed


def get_issue_amount(df, date):
    import pandas as pd
    # date가 문자열이라면 datetime 객체로 변환
    if isinstance(date, str):
        date = pd.to_datetime(date)
    # date가 datetime 객체가 아니라면 에러 메시지 출력
    elif not isinstance(date, pd.Timestamp):
        print("Error: 입력된 날짜가 올바르지 않습니다.")
        return None

    # 입력된 날짜 이전 또는 같은 발행일을 가진 행의 인덱스 가져오기
    idx = df[df['발행일'] <= date].index.tolist()

    # 발행금액 합계 초기화
    total_amount = 0
    total_sum = 0

    # 발행금액 합계와 계수 계산
    for i in idx:
        total_amount += df.at[i, '발행총액']
        total_sum += 1
    return total_sum,total_amount

def info_for_redeemed(df,df_issued_summary,input_date):
    import pandas as pd
    # date가 인덱스에 있는지 확인
    if input_date not in df.index: # 인덱스에 없는 날짜라면
        input_date=df.index[df.index < input_date].max() # 가장 가까운 앞 날짜 추출
    else: # 인덱스에 있다면 그냥 날짜객체로 반환
        input_date=pd.Timestamp(input_date)
    # 특정일을 나타내는 행에서 그 값이 0인 것들중 칼럼 이름이 KR로 시작하는 것들을 Series로 추출함
    zeros=df.loc[input_date][df.loc[input_date] == 0].filter(regex='^KR')

    # 빈 데이터프레임 생성
    df_redeemed = pd.DataFrame(columns=zeros.index)

    redeemed_amount=0
    redeemed_num=0

    for col in zeros.index:
        non_zero_values = df.loc[df[col] != 0, col]
        last_non_zero_index = non_zero_values.index[-1]
        # 만일 최종일의 날짜가 입력값보다 크면 상환된 종목이 아님을 의미한다.
        # 추가로 len(non_zero_values)이 0이어도 대상이 아니다.
        if (last_non_zero_index > input_date) or (len(non_zero_values)==0):
            df_redeemed.drop(columns=[col],inplace=True) # 해당 코드 삭제
            continue # 다음 칼럼으로 이동
        redeemed_amount += df_issued_summary.at[col,'발행총액'] # 해당 종목의 발행총액을 더해줌
        redeemed_num += 1

    return redeemed_num,redeemed_amount/1e+9

def sharpe_ratio_for_redeemed(df,rf, input_date):
    import pandas as pd
    import numpy as np
    # date가 인덱스에 있는지 확인
    if input_date not in df.index: # 인덱스에 없는 날짜라면
        input_date=df.index[df.index < input_date].max() # 가장 가까운 앞 날짜 추출
    else: # 인덱스에 있다면 그냥 날짜객체로 반환
        input_date=pd.Timestamp(input_date)

    # 특정일을 나타내는 행에서 그 값이 0인 것들중 칼럼 이름이 KR로 시작하는 것들을 Series로 추출함
    zeros=df.loc[input_date][df.loc[input_date] == 0].filter(regex='^KR')

    # 빈 데이터프레임 생성
    Sharpe_redeemed = pd.Series(index=zeros.index)

    for col in zeros.index:
        non_zero_values = df.loc[df[col] != 0, col]
        last_non_zero_index = non_zero_values.index[-1]
        # 만일 최종일의 날짜가 입력값보다 크면 상환된 종목이 아님을 의미한다.
        # 추가로 len(non_zero_values)이 0이어도 대상이 아니다.
        if (last_non_zero_index > input_date) or (len(non_zero_values)==0):
            Sharpe_redeemed.drop(index=col,inplace=True) # 해당 코드 삭제
            continue # 다음 칼럼으로 이동
        # 로그 수익률 계산
        log_returns = np.log(non_zero_values / non_zero_values.shift(1))

        # 연간 로그 수익률의 평균과 표준편차 계산
        annual_mean_log_return = log_returns.mean() * 252  # 252는 주식 거래일 수
        annual_std_log_return = log_returns.std() * np.sqrt(252)  # 연간 표준편차 계산

        # sharpe ratio 계산
        sr=(annual_mean_log_return-rf)/annual_std_log_return
        Sharpe_redeemed[col] = sr

    return Sharpe_redeemed