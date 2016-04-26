def date_parse(date_string):
    from datetime import datetime, date
    date_ar = [int(x) for x in date_string.split("/")]
    date_len = len(date_ar)
    now_year = date.today().year
    if date_len == 0:
        return None
    elif date_len == 1:
        import calendar
        return date(
                now_year,
                date_ar[0],
                calendar.monthrange(now_year, date_ar[0])[1]
                )
    elif date_len == 2:
        return date(now_year, date_ar[0], date_ar[1])
    elif date_len == 3:
        return date(date_ar[0], date_ar[1], date_ar[2])
    elif date_len == 4:
        return datetime(
                date_ar[0],
                date_ar[1],
                date_ar[2],
                date_ar[3])
    elif date_len == 5:
        return datetime(
                date_ar[0],
                date_ar[1],
                date_ar[2],
                date_ar[3],
                date_ar[4])
    elif date_len == 6:
        return datetime(
                date_ar[0],
                date_ar[1],
                date_ar[2],
                date_ar[3],
                date_ar[4],
                date_ar[5])
