
def dbnum(num_str):
    try:
        return int(num_str)
    except ValueError as e:
        front = int(num_str[:-1])
        end_vals = {
            "{": 0,
            "J": -1,
            "K": -2,
            "L": -3,
            "M": -4,
            "N": -5,
            "O": -6,
            "P": -7,
            "Q": -8,
            "R": -9
        }
        back = end_vals[num_str[-1]]
        return -front * 10 + back

def parse(file_names, years):
    codestoState = {
        "02": "AK",
        "01": "AL",
        "05": "AR",
        "60": "AS",
        "04": "AZ",
        "06": "CA",
        "08": "CO",
        "09": "CT",
        "11": "DC",
        "10": "DE",
        "12": "FL",
        "13": "GA",
        "66": "GU",
        "15": "HI",
        "19": "IA",
        "16": "ID",
        "17": "IL",
        "18": "IN",
        "20": "KS",
        "21": "KY",
        "22": "LA",
        "25": "MA",
        "24": "MD",
        "23": "ME",
        "26": "MI",
        "27": "MN",
        "29": "MO",
        "28": "MS",
        "30": "MT",
        "37": "NC",
        "38": "ND",
        "31": "NE",
        "33": "NH",
        "34": "NJ",
        "35": "NM",
        "32": "NV",
        "36": "NY",
        "39": "OH",
        "40": "OK",
        "41": "OR",
        "42": "PA",
        "72": "PR",
        "44": "RI",
        "45": "SC",
        "46": "SD",
        "47": "TN",
        "48": "TX",
        "49": "UT",
        "51": "VA",
        "78": "VI",
        "50": "VT",
        "53": "WA",
        "55": "WI",
        "54": "WV",
        "56": "WY"
    }
    data = {}
    for name in file_names:
        with open(name, 'r') as db:
            for ln in db:
                state = codestoState[int(ln[1:3])]
                ori = ln[3:10]
                core_city = ln[22]
                is_agency = ln[43]
                population = dbnum(ln[44:53])
                county = ln[]
                
                city = ln[:]
                population = int(ln[:])

