# -*- coding: utf-8 -*-
"""
Created on Tue May 14 08:10:37 2024

@author: S.T.Hwang
"""

 # 함수 작성
def stats_for_alives(date0):
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


# 함수 작성
def pa_return_for_alives(date0):
  kr_cols= df_Daily_NAV.loc[date0].filter(regex=r'^KR')
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

def stats_for_redeemed(input_date):
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
def stats_for_redeemed_old(input_date):
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


def hist_for_redeemded(input_date):
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

  n, bins, patches = plt.hist(ror_for_redeemed, bins=10, edgecolor='black', alpha=0.7, density=False)

  plt.xlabel('Per Annum Return')
  plt.ylabel('Frequency Ratio(freq/total)')
  plt.title('Histogram of Redeemed ELS in Rate of Return p.a.')

  # 각 막대의 높이를 총 데이터 수로 나누고, 백분율로 변환하여 y축 레이블에 표시
  total_data_count = len(ror_for_redeemed)
  plt.gca().set_yticklabels(['{:.0f}%'.format((height / total_data_count) * 100) for height in plt.gca().get_yticks()])

  # x축 눈금을 %로 표시하기
  plt.gca().xaxis.set_major_formatter(ticker.PercentFormatter(xmax=1))

  plt.show()

  # 파일로 출력
  # 연도월일 형식으로 변환
  formatted_date = input_date.strftime('%Y%m%d')
  # 파일 이름 생성
  file_name = f'/content/drive/MyDrive/hist_for_redeemed_{formatted_date}.xlsx'
  ror_for_redeemed.to_excel(file_name)

  return ror_for_redeemed


def get_issue_amount(df, date):
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



def info_for_redeemed(df,input_date):
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


def info_for_redeemed_old(df,input_date):
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


# 새로운 함수 작성
def sharpe_ratio_for_redeemed(df,rf, input_date):
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


