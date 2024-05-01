from app.adaptation.Strategy import Strategy
from app.adaptation.Util import *
from app.adaptation import Knowledge
from app.network.Network import Network
from app.Config import adaptation_period
import csv
from numpy import mean


class AvoidOverLoadedStreets(Strategy):

    def monitor(self):
        return Util.get_street_utilizations(Knowledge.time_of_last_adaptation, adaptation_period)[0]

    def analyze(self, utilizations):
        overloaded_streets = []
        for street, utilizations in utilizations.iteritems():
            mean_utilization = mean(utilizations)
            if mean_utilization > 0.4:
                print "overloaded street: " + str(street)
                overloaded_streets.append(street)
        return overloaded_streets

    def plan(self, overloaded_streets):
        avoid_streets_signal = []
        for i in range(Knowledge.planning_steps):
            avoid_streets_signal += [0 if edge.id in overloaded_streets else 1 for edge in Network.routingEdges]
        return avoid_streets_signal

    def execute(self, avoid_streets_signal):
        if len(avoid_streets_signal) > 0:
            print "Sending signal to avoid overloaded streets!"
        with open('datasets/plans/signal.target', 'w') as signal_fil:
            signal_writer = csv.writer(signal_fil, dialect='excel')
            signal_writer.writerow(avoid_streets_signal)

        Knowledge.globalCostFunction = "XCORR"
