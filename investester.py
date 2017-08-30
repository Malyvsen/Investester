import numpy as np
import matplotlib.pyplot as plt



class Tester:
	def SingleTest(strategy, numSteps = 100, showPlot = True):
		'''strategy - a class: newOwned = strategy.apply(prevoiusOwned, previousValue, newValue); must have strategy.name'''
		value = np.array([1.0])
		for i in range(numSteps):
			value = np.append(value, value[-1] + np.random.normal())
		value = np.exp(value)

		freeBalance = np.array([0.0])
		owned = np.array([1.0])
		for i in range(numSteps):
			owned = np.append(owned, strategy.apply(owned[i], value[i], value[i + 1]))
			freeBalance = np.append(freeBalance, freeBalance[-1] + (owned[i] - owned[i + 1]) * value[i + 1])

		if showPlot:
			plt.plot(value, 'r-', label = 'value')
			plt.plot(owned, 'g-', label = 'owned')
			plt.plot(freeBalance + owned * value, 'b-', label = 'total balance')
			plt.legend()
			plt.title(strategy.name)
			plt.yscale('log')
			plt.show()

		return freeBalance[-1] + owned[-1] * value[-1]


	def MultiTest(self, strategiesList, numStepsList, numTestsPerStep = 100, showPlotPerTest = False):
		profit = [[0.0 for j in range(len(numStepsList))] for i in range(len(strategiesList))]
		for strategyID in range(len(strategiesList)):
			strategy = strategiesList[strategyID]
			for numStepsID in range(len(numStepsList)):
				numSteps = numStepsList[numStepsID]
				for step in range(numTestsPerStep):
					profit[strategyID][numStepsID] += self.SingleTest(strategy = strategy, numSteps = numSteps, showPlot = showPlotPerTest)
				profit[strategyID][numStepsID] /= numTestsPerStep


		graphParams = ['r-', 'g-', 'b-', 'c-', 'm-', 'y-', 'k-']
		for strategyID in range(len(strategiesList)):
			strategy = strategiesList[strategyID]
			plt.plot(profit[strategyID], graphParams[strategyID % len(graphParams)], label = strategy.name)
		plt.legend()
		plt.yscale('log')
		plt.show()




class KeepStrategy:
	name = 'keep'
	def apply(previousOwned, previousValue, newValue):
		return previousOwned




class ConstantStrategy:
	name = 'constant value'
	def apply(previousOwned, previousValue, newValue):
		return previousOwned * previousValue / newValue




Tester.MultiTest(Tester, [KeepStrategy, ConstantStrategy], range(10, 100))
