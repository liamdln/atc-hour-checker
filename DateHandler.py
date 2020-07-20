import datetime
import dateutil


def getDetails():
    happy = False

    while not happy:

        fromDate = getDate("Enter the date you want to measure from in format 'yyyy-mm-dd': ")
        toDate = getDate("Enter the date you want to measure to in format 'yyyy-mm-dd': ")

        if toDate <= fromDate:
            print("The date you want to measure to cannot be earlier than the date you want to measure from.")
        else:
            happy = True

    print("""Dates changed to {0} (from date) and {1} (to date).""".format(str(fromDate), str(toDate)))

    return dateutil.parser.isoparse(fromDate), dateutil.parser.isoparse(toDate)


def getDate(question):
    happy = False
    while not happy:

        measureDate = input(question)
        year, month, day = measureDate.split("-")
        try:
            datetime.datetime(int(year), int(month), int(day))
            happy = True
        except:
            print("Date is not valid.")
            happy = False

    return measureDate
