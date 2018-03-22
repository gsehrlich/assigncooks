#!usr/bin/env python27

import sys, os
import numpy as np
from numpy.random import randint

class Schedule(object):
	cooking_balance = None
	maximal_assignment = None
	
	@classmethod
	def load_cooking_balance(cls):
		"""
		Get cooks' cooking balances from a file or online and store
		them.
		"""
		cls.cooking_balance = NotImplemented

	@classmethod
	def create_maximal_assignment(cls):
		"""
		Get cooks' availabilities from a file or online. Store a
		schedule specifying which cooks are available on each day.
		"""
		# do some stuff
		cls.maximal_assignment = NotImplemented

	@classmethod
	def create_assignment(cls):
		"""
		Starting with the maximal assignment, remove cooks until there
		are two cooks per day. Return the result.
		"""
		assignment = NotImplemented
		raise NotImplementedError()
		return assignment

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