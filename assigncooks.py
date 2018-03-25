#!/usr/bin/env python3

import sys, os
import csv
import numpy as np
import random

def grabcsv(fname):
    if not os.path.exists(fname):
        print("File doesn't exist: " + fname)
        exit(1)

    lines = []
    with open(fname, 'r') as f:
        csv_reader = csv.reader(f)
        lines = [[entry.strip() for entry in line] for line in csv_reader]

    headers = { header : pos + 1 for pos , header in enumerate(lines[0][1:]) }
    dict_data = {
        line[0] : { header : line[headers[header]] for header in headers }
        for line in lines[1:]
    }
    return dict_data

class Schedule(object):
    cooks            = None
    dates            = None
    balance          = None
    maximal_schedule = None

    @classmethod
    def load_month(cls, date):
        """
        Loads the data files `data/date_balance.csv` and `data/date_poll.csv` into the class variables.
        """
        balance_file = "data/" + date + "_balance.csv"
        poll_file    = "data/" + date + "_poll.csv"
        raw_balances = grabcsv(balance_file)
        raw_poll     = grabcsv(poll_file)

        cls.cooks = list(raw_balances)
        cls.dates = list(raw_poll[list(raw_poll)[0]])

        cls.balance = { cook : int(raw_balances[cook]['balance']) for cook in cls.cooks }

        cls.maximal_schedule = {
            date : [cook for cook in cls.cooks
                         if cook in raw_poll and raw_poll[cook][date] == 'OK'
                   ]
            for date in cls.dates
        }
        return Schedule(cls.dates, cls.cooks, cls.balance, cls.maximal_schedule)

    def __init__(self, dates, cooks, balances, schedule):
        """
        Create a schedule based on the supplied arguments.
        All arguments are required.
        Calls `calc_init` to make sure all relevant instance variables are set.
        """
        self.dates = dates
        self.cooks = cooks
        self.cooking_balance = balances
        self.schedule = schedule
        self.calc_init()

    def calc_init(self):
        """
        Call methods which calculate various instance variables.
        This makes it easier to "renormalize" the state of the given Schedule, making sure all fields agree.
        """
        self.calc_max_cooks()
        self.calc_max_dates()
        self.calc_max_placements()

    def calc_max_dates(self):
        """
        Will calculate the dates which have the maximum number of cooks assigned to them.
        """

        self.max_dates = []
        max_peeps = 0
        for date in self.dates:
            cur_peeps = len(self.schedule[date])
            if cur_peeps > max_peeps:
                self.max_dates = [date]
                max_peeps = cur_peeps
            elif max_peeps == cur_peeps:
                self.max_dates.append(date)

    def calc_max_cooks(self):
        """
        Will calculate the cooks which have the maximum number of dates they're assigned on.
        """

        self.max_cooks = []
        max_cookings = 0

        for cook in self.cooks:
            c = self.cooking_balance[cook]
            for date in self.dates:
                if cook in self.schedule[date]:
                    c += 1
            if c > max_cookings:
                max_cookings = c
                self.max_cooks = [cook]
            elif c == max_cookings:
                self.max_cooks.append(cook)

    def calc_max_placements(self):
        """
        Calculates the maximal placements on the schedule as (date, cook) tuples.
        A placement is maximal if it is a cook which is max and a date which is max and is present in the schedule.
        """
        self.calc_max_dates()
        self.calc_max_cooks()
        self.max_placements = [
            (date, cook)
            for date in self.max_dates for cook in self.max_cooks
            if cook in self.schedule[date]
        ]

    def remove_placement(placement_to_remove):
        """
        Remove the provided placement from self.schedule.
        """
        cook, date = placement_to_remove
        self.schedule[date].remove[cook]

    def create_schedule(self):
        """
        Starting with the maximal schedule, remove cooks until there
        are two cooks per day. Return the result.
        """
        self.schedule = dict(self.maximal_schedule)

        scores = self.get_scores()
        self.calc_removable_placements()

        # remove cooks one by one according to a heuristic until the
        # schedule has two cooks on every date
        while self.remove_heuristic():
            continue

    def remove_heuristic(self):
        """
        Wrapper for specifying which heuristic to use for calculating and performing removals.
        """
        return self.random_removable_placement()

    def random_removable_placement(self):
        """
        The easiest heuristic. Randomly choose a placement to remove
        and return it.
        """

        if len(self.removable_placements) == 0:
            return False
        placement_to_remove = random.choice(self.removable_placements)
        self.remove_placement(placement_to_remove)

        date, cook = placement_to_remove
        if len(self.schedule[date]) <= 2:
            self.calc_random_removable_placements()
        return True

    def calc_random_removable_placements(self):
        """
        Generate the list of placements (i.e. (cook, date) pairs) that
        can be removed from the current schedule.
        """
        dates_with_too_many_cooks = [
            date for date in self.dates
            if len(self.schedule(date)) > 2
            ]
        self.removable_placements = [
            (cook, date) for date in dates_with_too_many_cooks
            for cook in self.schedule[date]
            ]

    def get_score(self):
        """
        Count how many times more times each cook appears on the
        schedule than they're supposed to (based on their balance).
        """
        scores = {}
        for cook in self.cooks:
            times_on_schedule = len(
                [date for date in self.dates
                if cook in self.schedule[date]]
                )
            scores[cook] = times_on_schedule - balance[cook]

        return scores

    def objective(self):
        """
        Calculate how good the current schedule is. Return the
        result.
        """
        raise NotImplementedError()

    def switch_filled(self, n):
        """
        Return a Schedule in which `n` cooks have been rotated in those
        `n` slots, making sure those cooks are available for the new
        slots.
        """
        raise NotImplementedError()
        changes = NotImplemented
        return Schedule(self, changes)

    def deschedule_cooks(self):
        """
        Return a Schedule in which the number of cooks on a slot has
        been reduced below 2.
        """
        raise NotImplementedError()
        changes = NotImplemented
        return Schedule(self, changes)

    def __str__(self):
        """
        Print the schedule nicely.
        """
        raise NotImpementedError()
        return ""

    def save_to_file(self, filename):
        """
        Make or overwrite the file with the given name with the string
        representation of the Schedule.
        """
        with open(filename, "w") as f:
            f.write(str(self))

def usage():
    """
    Print the usage of the file."
    """
    print("Usage: " + sys.argv[0] + " <date>")
    print()
    print("    where <date> is the date in `data/...` you want to build a schedule for.")
    sys.exit(1)

def main():
    """
    Create the list of possible schedules, then evolve the list until
    some of them are good enough. Save the result in an output
    directory given either by the first command-line argument or during
    execution.
    """
    if len(sys.argv) == 2:
        date = sys.argv[1]
    else:
        usage()
    schedule = Schedule.load_month(date)
    schedule.calc_max_dates()
    schedule.calc_max_cooks()
    print(schedule.max_cooks)
    print(schedule.max_dates)
    print(schedule.schedule)
    print(schedule.max_placements)

def evolve():
    """
    Attempt to create a better schedule than those in the schedule
    list. Choose an schedule to evolve, then randomly evolve it, then
    check whether it's an improvement. If it is, return it; else return
    None.
    """
    raise NotImplementedError()
    return None

def good_enough(schedules):
    """
    Decide whether the list of schedules is good enough that the search
    can stop. If so, return the list of good enough schedules, else
    False.
    """
    raise NotImplementedError()
    return False

if __name__ == "__main__":
    main()
