import requests
from datetime import datetime
from pytz import timezone


def powerball(date=False):
    count = 1
    result = []
    if not date:
        KST = datetime.now(timezone('Asia/Seoul'))
        date = f"{KST.year}-{KST.strftime('%m')}-{KST.strftime('%d')}"
    while True:
        payload = {"view": "action", "action": "ajaxPowerballLog", "actionType": "dayLog", "date": date, "page": str(count)}
        c = 0
        while c <= 3:
            try:
                resp = requests.post("https://www.powerballgame.co.kr/", data=payload).json()
                break
            except:
                c += 1
        else:
            return False
        if resp['endYN'] == 'Y':
            break
        count += 1
        for r in resp['content']:
            result.append({"today_round": int(r['todayRound']), "round": int(r['round']), "powerball": {"powerball": int(r['powerball']), "powerball_section": r['powerballPeriod'].split(' ')[0], "powerball_odd_even": r['powerballOddEven'], "powerball_under_over": r['powerballUnderOver']}, "ball": {"ball": list(map(int, r['number'].split(', '))), 'ball_sum': int(r['numberSum']), "ball_section": r['numberSumPeriod'].split(" ")[0], 'ball_size': r['numberPeriod'].split(" ")[0], 'ball_odd_even': r['numberOddEven'], 'ball_under_over': r['numberUnderOver']}})
    return result


def powerladder(date=False):
    pb = powerball(date)
    result = []
    for r in pb:
        first_number = int(r['ball']['ball'][0])
        start = "우" if first_number % 2 == 0 else "좌"
        line = 3 if first_number <= 14 else 4
        end = "홀" if (start == "우" and line == 3) or (start == "좌" and line == 4) else "짝"
        result.append({"today_round": r["today_round"], "result": [start, line, end]})
    return result


if __name__ == "__main__":
    print(powerball())
    print(powerladder("2022-03-13"))
