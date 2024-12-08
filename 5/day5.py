#!/usr/bin/python3

def valid_report(priority: list[tuple[int, int]], report: list[int]) -> bool:
    for index, value in enumerate(report):
        rules = [low for high, low in priority if high == value]
        for low in rules:
            if low in report and report.index(low) < index:
                return False
    return True

def make_valid(priority: list[tuple[int, int]], report: list[int]):
    while not valid_report(priority, report):
        for index, value in enumerate(report):
            rules = [low for high, low in priority if high == value]
            for low in rules:
                if low in report and report.index(low) < index:
                    report.remove(value)
                    report.insert(report.index(low), value)
    return report

def main():
    page_prio = []
    with open("day5.input", "r") as file:
        lines = file.read().strip().split("\n\n")

    page_prio = lines[0].split("\n")
    reports = lines[1].split("\n")

    page_prio = [tuple(map(int, x.split("|"))) for x in page_prio]
    reports = [list(map(int, x.split(","))) for x in reports]

    print(f"Total Reports: {len(reports)}")

    correct_reports = [ report for report in reports if valid_report(page_prio, report)]
    print(f"Total correct reports: {len(correct_reports)}")

    mids = [report[int(len(report)/2)] for report in correct_reports]
    print(f"Sum of correct mids: {sum(mids)}")

    #Part 2
    bad_reports = [ report for report in reports if not valid_report(page_prio, report)]
    print(f"Total bad reports: {len(bad_reports)}")

    mids = [report[int(len(report)/2)] for report in [make_valid(page_prio,bad_report) for bad_report in bad_reports]]
    print(f"Sum of bad mids: {sum(mids)}")

if __name__ == "__main__":
    main()