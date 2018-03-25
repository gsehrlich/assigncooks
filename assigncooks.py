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
        raw_polls    = grabcsv(poll_file)

        cls.cooks = list(raw_balances)
        cls.dates = list(raw_polls[list(raw_polls)[0]])

        cls.balance = { cook : int(raw_balances[cook]['balance']) for cook in cls.cooks }

    @classmethod
    def load_cooking_balance(cls):
        """
        Get cooks' cooking balances from a file or online and store
        them.
        """
        # TODO: IMPLEMENT CORRECTLY
        cls.load_sample_cooking_balance()

    # TEMPORARY
    @classmethod
    def load_sample_cooking_balance(cls):
        """
        Get cooks' cooking balances from a made-up file and store them.
        Also store the list of cooks.
        """
        cls.cooks, balance = np.loadtxt("sample_balance.txt", delimiter="\t",
                                    dtype=str, unpack=True)
        cls.balance = {cls.cooks[i]: float(balance[i])
                        for i in xrange(len(cls.cooks))}

    @classmethod
    def create_maximal_schedule(cls):
        """
        Get cooks' availabilities from a file or online. Store a
        schedule specifying which cooks are available on each day.
        """
        # TODO: IMPLEMENT CORRECTLY
        cls.create_sample_cooking_balalnce()

    @classmethod
    def create_sample_cooking_balance(cls):
        """
        Get cooks' availabilities from a made-up file. Store a schedule
        specifying which cooks are available on each day. Also store the
        list of dates.
        """
        filename = "sample_availability.txt"

        # Use the first line to get the calendar
        with open(filename) as f:
            dates = f.readline().strip("\n#").split("\t")
            cls.dates = dates[1:]    # Get rid of the cook column

        availability_arr = np.loadtxt(filename, delimiter="\t", dtype=str)
        availability_dict = {availability_arr[0, i]: availability_arr[1:, i]
                                for i in xrange(len(availability_arr))}

        # TODO: figure out what to do if a cook isn't in the poll. This
        # defaults to giving them no availability.

        # TODO: figure out what to do if a cook's name is spelled dif-
        # ferently on the poll than on the balance sheet. Currently this
        # will throw a KeyError if the cook's balance-sheet name isn't
        # on the poll.

        cls.maximal_schedule = {
            date: [cook for cook in cls.cooks
                    if date in availability_dict[cook]]
            for date in cls.dates
            }

    def calc_max_dates(self):
        """
        Will calculate the dates which have the maximum number of cooks assigned to them.
        """

        self.max_dates = []
        max_peeps = 0
        for date in self.dates:
            cur_peeps = len(self.current_assignment[date])
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
            c = 0
            for date in self.dates:
                if cook in self.current_assignment[date]:
                    c += 1
            if c > max_cookings:
                max_cookings = c
                self.max_cooks = [cook]
            elif c == max_cookings:
                self.max_cooks.append(cook)

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

    def remove_placement(placement_to_remove):
        """
        Remove the provided placement from self.schedule.
        """
        cook, date = placement_to_remove
        self.schedule[date].remove[cook]

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

    def objective(self):
        """
        Calculate how good the current schedule is. Return the
        result.
        """
        raise NotImplementedError()

    def __init__(self, base_schedule=None, changes=()):
        """
        Create a schedule based on `base_schedule` with changes given
        by `changes`. If `base_schedule` is not given, cooks are
        randomly removed from the maximal schedule to create the
        schedule.
        """
        if self.cooking_balance is None:
            self.load_cooking_balance()
        if self.maximal_schedule is None:
            self.create_maximal_schedule()

        if base_schedule is None:
            self.create_schedule()
        else:
            self.schedule = base_schedule.schedule
            for change in changes:
                # make the changes
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
