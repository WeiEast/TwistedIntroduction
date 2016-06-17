import time
from twisted.internet.task import LoopingCall

# Keeps track of Countdown activity and when to stop the reactor
class CountdownMonitor(object):

    def __init__(self):
        # The list of countdowns
        self.countdown_list = []

    # Add a countdown instance to the list of countdowns
    def addToList(self, *args):
        self.countdown_list.extend(args)

    # Starts a stopwatch
    def startTimer(self):
        self.starting_time = time.time()

    # Remove one countdown instance from the list after it has reached 0 ticks
    # Stop the reactor if no more instances exist
    def removeFromList(self, countdown_instance):
        self.countdown_list.remove(countdown_instance)

        # If there are no more countdowns in the list, stop the reactor
        if not self.countdown_list:
            reactor.callLater(0, reactor.stop)

    # Stop and return the stopwatch time
    def getTimeElapsed(self):
        return time.time() - self.starting_time


# Instances of this print terminal output at different rates
class Countdown(object):

    def __init__(self, name, ticks, rate, monitor):
        self.name, self.ticks, self.rate, self.monitor = name, ticks, rate, monitor

        # Create a looping call for the countdown method
        self.looper = LoopingCall(self.count)

        # Add this Countdown object to the Monitor list
        monitor.addToList(self)

    # Start the looper at the given rate
    def start(self):
        self.looper.start(self.rate)

    def count(self):
        # If the Countdown instance has ticks left
        # the looping call continues and we decrememnt this object's count
        if self.ticks > 0:

            print 'Timer {}: {} ticks left at {} ticks/second'.format(
                    self.name, self.ticks, self.rate
                    )

            self.ticks -= 1

        # If the ticks have reached 0
        # Remove this countdown object from the Monitor list
        # Stop the looping call
        else:
            self.looper.stop()

            print ' --> Timer {} finished in ({:.3f} seconds!'.format(
                    self.name, monitor.getTimeElapsed()
                    )

            self.monitor.removeFromList(self)

# Add countdowns to a list for running
def AddToCountdownQueue(countdown_list, name, ticks, rate):
    new_countdown_params = [name, ticks, rate]
    countdown_list.append(new_countdown_params)
    print countdown_list

from twisted.internet import reactor

# One monitor to rule them all
monitor = CountdownMonitor()

# Start timer when the reactor starts
reactor.callWhenRunning(monitor.startTimer)

# Create a list to hold our different countdowns
countdown_queue = []

# Create different countdowns
AddToCountdownQueue(countdown_queue, "1", 5, 1)
AddToCountdownQueue(countdown_queue, "2", 10, 1)
AddToCountdownQueue(countdown_queue, "3", 5, 0.5)
AddToCountdownQueue(countdown_queue, "4", 5, 0.6)

# Call different reactors
for name, ticks, rate in countdown_queue:
    reactor.callWhenRunning(
            Countdown(name, ticks, rate, monitor).start
            )

print 'Start!'
reactor.run()
print 'Stop!'
