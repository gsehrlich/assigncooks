#!usr/bin/env python27

import sys, os
import numpy as np
from numpy.random import randint

class Schedule(object):
	balance = None
	maximal_assignment = None
	
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
		"""
		cls.cooks, balance = np.loadtxt("sample_balance.txt", delimiter="\t",
									dtype=str, unpack=True)
		cls.balance = {cls.cooks[i]: float(balance[i])
						for i in xrange(len(cls.cooks))}

	@classmethod
	def create_maximal_assignment(cls):
		"""
		Get cooks' availabilities from a file or online. Store a
		schedule specifying which cooks are available on each day.
		"""
		# TODO: IMPLEMENT CORRECTLY
		cls.create_sample_cooking_balalnce()

	@classmethod
	def create_sample_cooking_balalnce(cls):
		"""
		Get cooks' availabilities from a made-up file. Store a schedule
		specifying which cooks are available on each day.
		"""
		filename = "sample_availability.txt"

		# Use the first line to get the calendar
		with open(filename) as f:
			dates = f.readline().strip("\n#").split("\t")
			dates = dates[1:]	# Get rid of the cook column

		availability_arr = np.loadtxt(filename, delimiter="\t", dtype=str)
		availability_dict = {availability_arr[0, i]: availability_arr[1:, i]
								for i in xrange(len(availability_arr))}

		cls.maximal_assignment = {
			date: [cook for cook in cooks if date in availbility_dict[cook]]
			for date in dates
			}

	@classmethod
	def create_assignment(cls):
		"""
		Starting with the maximal assignment, remove cooks until there
		are two cooks per day. Return the result.
		"""
		# count how many times each cook appears
		score = {cook: sum(
			[1 if cook in cls.maximal_assignment[date] else 0
			for date in cls.maximal_assignment])
			for cook in cooks}

		# count how many more times each cook appears than their balance
		for cook in cooks:
			score[cook] -= balance[cook]

		# randomly remove cooks whose score is the highest one by one,
		# updating the score, until there are two cooks per slot
		assignment = dict([cls.maximal_assignment])
		dates_with_too_many_cooks = Schedule.dates_with_too_many_cooks(
			assignment)
		while dates_with_too_many_cooks:
			most_ahead_amount = max(score.values())
			most_ahead_cooks = [cook for cook in cooks
								if score[cook] == most_ahead_amount]
			cook_to_remove = most_ahead_cooks[randint(len(most_ahead_cooks))]

			dates_where_cook_assigned = [
				date for date in dates_with_too_many_cooks
				if cook_to_remove in assignment[date]
				]
			date_to_remove_from = dates_where_cook_assigned[randint(
				len(dates_where_cook_assigned))]
			assignment[date_to_remove_from].remove(cook_to_remove)

		return assignment

	@staticmethod
	def dates_with_too_many_cooks(assignment):
		dates = []
		for cook in cooks:
			if len(assignment[cook]) > 2:
				dates.append(assignment[cook])
		return dates

	def objective(self):
		"""
		Calculate how good the current assignment is. Return the
		result.
		"""
		raise NotImplementedError()

	def __init__(self, base_schedule=None, changes=()):
		"""
		Create a schedule based on `base_schedule` with changes given
		by `changes`. If `base_schedule` is not given, cooks are
		randomly removed from the maximal assignment to create the
		schedule.
		"""
		if self.cooking_balance is None:
			Schedule.load_cooking_balance()
		if self.maximal_assignment is None:
			Schedule.create_maximal_assignment()

		if base_schedule is None:
			self.assignment = Schedule.create_assignment()
		else:
			self.assignment = base_schedule.assignment
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
		Print the assignment nicely.
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

def main():
	"""
	Create the list of possible assignments, then evolve the list until
	some of them are good enough. Save the result in an output
	directory given either by the first command-line argument or during
	execution.
	"""
	# check ommand-line arguments
	if len(sys.argv) == 2:
		dirname = sys.argv[1]
	if len(sys.argv) == 3:
		dirname = sys.argv[1]
		seed = int(sys.argv[2])
	# if none provided, ask for dirname at beginning of execution
	elif len(sys.argv) < 2:
		dirname = raw_input("Directory name for output schedules? ")
	# if too many arguments are created, display a help message
	else:
		print "Usage: 'python assigncooks.py output_directory_name"

	# For platform independence, don't allow creation of the directory
	# if it has the same name as an existing file.
	if os.path.exists(dirname):
		print("A file or directory exists with the same name. Please "
			"choose a different name.")
		sys.exit(1)
	else:
		os.mkdir(dirname)

	schedules = []
	good_enough_schedules = None
	while good_enough_schedules is None:
		raise NotImplementedError()
		good_enough_schedules = good_enough(schedules)

	# save to file
	i = 0
	for schedule, score in good_enough_schedules():
		schedule.save_to_file(os.path.join(
			dirname, "schedule%02d_score_%d" % (i, score)))
		i += 1

	print "Schedules saved to directory '%s'" % dirname

def evolve():
	"""
	Attempt to create a better assignment than those in the assignments
	list. Choose an assignment to evolve, then randomly evolve it, then
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

if __name__ == "__main__": main()