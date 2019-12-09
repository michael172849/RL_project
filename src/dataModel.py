import numpy as np

class DataPoint():
    """
    one data from the Mannheim dataset
    """

class Duration():
    """
    Time a user spends in one state. Determined by Log-normal Distribution
    """
    def __init__(self, mu, sigma=60*30):
        if mu != 0:
            normal_std = np.sqrt(np.log(1 + (sigma/mu)**2))
            normal_mean = np.log(mu) - normal_std**2 / 2
            self.sigma = normal_std    # mean (minute)
            self.mu = normal_mean
        else:
            self.mu = 0

        self.samples = []   # duration, time pair. Time is a second in a day (ranges 0 ~ 43199)
        
    def sample(self):
        if self.mu == 0:
            return self.mu
        return np.random.lognormal(self.mu, self.sigma, 1).item()

    def addSample(self, duration, time):
        self.samples.append(duration, time)



class State():
    """
    State that represents user doing one activity in one location
    self.activity: user's current activity. "start" to indicate the start of the day. Is unique in the datamodel
    self.duration: if mean for duration is 0, it is an "event" where the activity that takes no time, like waking up
    """
    def __init__(self, activity, location="", duration=3*60, duration_sigma=60*30):
        self.transitions = []
        self.transition_weights = np.array([])
        # self.next_activities = []    # dictionary of possible next activity and their occurrences
        # self.next_activities_occurrence = np.array([])
        # self.next_activities_transition = []
        self.activity = activity
        self.location = location
        self.duration = Duration(duration, duration_sigma)
        self.duration_seconds = self.duration.sample()

    def get_duration_seconds(self):
        return self.duration_seconds

    def get_location(self, seconds):
        return self.location

    def get_activity(self):
        return self.activity
    
    def sample_next(self):
        """
        samples which transition to take
        return: Transition object
        """
        return np.random.choice(self.transitions, p=self.transition_weights/sum(self.transition_weights))

    def add_next_state(self, state, duration_mean, weight, duration_sigma=10*60):
        self.transitions.append(Transition(self, state, Duration(duration_mean)))
        self.transition_weights = np.append(self.transition_weights, weight)

        return self
    
    def __eq__(self, other):
        """
        only have to check activity because it's assumed to be unique
        """

        if self.activity == other.activity:
            return True
        else:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
class Transition():   # @TODO make street separate class
    """
    Transition stage from one stage to other
    The duration is determined at the time of the creation of this class
    """
    def __init__(self, from_state: State, to_state: State, duration=Duration(10, 0.1), weight=1):
        self.duration = duration
        self.duration_seconds = duration.sample()
        self.from_state = from_state
        self.to_state = to_state
        self.weight = weight
        self.place_between = ""

        # if duration is more than 10 minutes, we assume that the user is walking on the streets
        if self.duration_seconds > 10 * 60:
            self.place_between = "Street"

    def get_location(self, seconds):    # seconds from the back (remaining time)
        if self.place_between == "Street":
            if seconds < 5 * 60:
                return self.to_state.location
            elif seconds > self.duration_seconds - 5 * 60:
                return self.from_state.location
            else:
                return State("Street", "Street").location
        else:
            if seconds < self.duration_seconds / 2:
                return self.to_state.location
            else:
                return self.from_state.location

    def get_activity(self):
        return "Transition"

    def get_duration_seconds(self):
        return self.duration_seconds

    def is_next(self, state):
        """
        checks if next state (to_state) is the given state
        """
        return self.to_state == state

class ObservationSpace():
    """
    lowest and highest possible values of a feature
    """
    def __init__(self, low, high):
        self.low = low
        self.high = high


class DataModel():
    """
    DataModel for producing mockup datasets based on given dataset of a user
    Extracts user activity pattern and makes a graph model out of it
    The dataset created has three features (at least for now) 
        Time: 24 hr time
        Location: home_bathroom home_kitchen home_study 
        Posture:
        State (Activity - Ground Truth)
        
    Assumptions: User can just do one activity in one context

    """
    def __init__(self, pre_defined, seed=42):
        """
        pre_defined: load pre-defined models rather than automatically processing the dataset
        """
        # np.random.seed(seed)

        self.s = []   # states
        self.cur_time = 0    # current time in seconds (ranges 0 ~ 43199)
        self.start_state = None
        self.end_state = None 
        self.observation_space = ObservationSpace(0, 86399)
        self.role = pre_defined
        self.loc_set = []
        if pre_defined == "test_homeless":
            # Define all the states
            sleep_state = State("Sleeping", "home_bed", 4*60*60)
            wake_up_state = State("Wake up", "home_bed", 10)
            going_to_bed_state = State("Going to bed", "home_bed", 0)
            sleep_state = State("Sleeping", "home_bed", 30 * 60)

            # Define transition
            sleep_state.add_next_state(wake_up_state, 10, 9)
            wake_up_state.add_next_state(going_to_bed_state, 120 * 60, 9) # homeless person moves around the street
            going_to_bed_state.add_next_state(sleep_state, 10, 9)

            # add to state list
            self.s = [sleep_state, wake_up_state, going_to_bed_state]

            # Initialize start and end states
            self.start_state = sleep_state
            self.end_state = sleep_state 
            self.cur = self.start_state     # cur can be transition or state


        if pre_defined == "coffee_guy":
            # Define all the states
            sleep_state = State("Sleeping", "home_bed", 2*60*60)
            wake_up_state = State("Wake up", "home_bedroom", 5*60, 10)
            home_bathroom_state = State("PersonalGrooming", "home_bathroom", 7*60, 30)
            breakfast_state = State("Breakfast", "home_kitchen", 30*60, 60)

            morning_work_state = State("MorningWork", "Office", 3*60*60)
            evening_work_state = State("AfternoonWork", "Office", 5*60*60)

            lunch_outside_state = State("LunchOutside", "Restaurant", 1*60*60)
            lunch_home_state = State("LunchAtHome", "home_kitchen", 1*60*60)

            housework_livingroom_state = State("Housework", "home_livingroom", 2*60*60)

            socializing_home_state = State("SocializingAtHome", "home_study", 30*60, 10*60)
            socializing_outside_state = State("SocializingOutside", "Building", 4*60*60)
            
            dinner_state = State("Dinner", "Restaurant", 2*60*60)
            deskwork_state = State("Deskwork", "home_study", 1*60*60)
            bath_state = State("Bath", "home_bathroom", 1*60*60)
            going_to_bed_state = State("Going to bed", "home_bed", 20*60*60, 10)

            # Define transitions
            sleep_state.add_next_state(wake_up_state, 0, 7, 5)

            wake_up_state.add_next_state(home_bathroom_state, 10, 9, 4)
            home_bathroom_state.add_next_state(breakfast_state, 60, 9, 10)
            breakfast_state.add_next_state(morning_work_state, 30*60, 5)   # weekdays. takes 30min to commute to work
            breakfast_state.add_next_state(housework_livingroom_state, 60, 2)    # weekends.

            housework_livingroom_state.add_next_state(lunch_home_state, 60, 2)
            lunch_home_state.add_next_state(evening_work_state, 30*60,3)
            lunch_home_state.add_next_state(socializing_outside_state, 20*60, 0)

            morning_work_state.add_next_state(lunch_outside_state, 15*60, 13) # takes 15min to go to lunch
            morning_work_state.add_next_state(lunch_home_state, 30*60, 3) # takes 30min to go to home to have lunch
            lunch_outside_state.add_next_state(evening_work_state, 20*60, 7)

            evening_work_state.add_next_state(dinner_state, 30*60, 5)

            socializing_outside_state.add_next_state(dinner_state, 11*60, 7)
            dinner_state.add_next_state(socializing_home_state, 40*60, 3)
            dinner_state.add_next_state(deskwork_state, 40*60, 4)

            deskwork_state.add_next_state(bath_state, 100, 3)
            socializing_home_state.add_next_state(bath_state, 100, 4)

            bath_state.add_next_state(going_to_bed_state, 100, 4)

            # add to state list
            self.s = [sleep_state, wake_up_state, home_bathroom_state,
                    breakfast_state, morning_work_state, evening_work_state,
                    lunch_outside_state, lunch_home_state, socializing_home_state,
                    socializing_outside_state,dinner_state, deskwork_state, 
                    bath_state, going_to_bed_state, housework_livingroom_state]
            self.loc_set = list(set([state.location for state in self.s]))
            self.loc_set.append('Street')

             # Initialize start and end states
            self.start_state = sleep_state
            self.end_state = sleep_state 
            self.cur = self.start_state     # cur can be transition or state
            self.cur_time = 6 * 60 * 60

        # initialze time
        self.remaining_duration = self.start_state.get_duration_seconds()

    def reset(self, p=None, seed=2):
        if p is None:
            p = self.role
        self.__init__(p, seed=2)

    def findStateByActivity(self, activity):
        return [x for x in self.s if x == State(activity)]

    def step(self, seconds=10):
        """
        seconds: how many seconds is it going forward
        returns: {(time of the day(in seconds), location(label), activity(ground truth))}, done
        """
        self.cur_time += seconds
        if self.cur_time > 86399:
            return {"time":np.ceil(self.cur_time), 
                    "loc_cate":self.cur.get_location(self.remaining_duration),
                    "act_truth":self.cur.get_activity(),}, True

        while self.remaining_duration < seconds:    # if there are remaining time for current state / transition
            seconds -= self.remaining_duration
            if isinstance(self.cur, State):    # if the user was previously in state
                self.cur = self.cur.sample_next()
                self.remaining_duration = self.cur.get_duration_seconds()
            elif isinstance(self.cur, Transition):   # if the user was previously in transition
                self.cur = self.cur.to_state
                self.remaining_duration = self.cur.get_duration_seconds()

        if self.remaining_duration >= seconds:    # now the user is stopping halfway of a state or transition
            self.remaining_duration -= seconds
 
        return {"time":np.ceil(self.cur_time), 
                "loc_cate":self.cur.get_location(self.remaining_duration),
                "act_truth":self.cur.get_activity(),}, False

    def get_num_locations(self):
        print(self.loc_set)
        return len(self.loc_set)  # @TODO change this later
    
    def get_cont_low_high(self):
        return [self.observation_space.low], [self.observation_space.high]
        # return [],[]

    def get_cont_cate(self, state):
        """
            Compute the continuous and categorical part of a state snapshot
        """
        cont = np.array([state['time']])
        cate = np.array([self.loc_set.index(state['loc_cate'])]).astype(int)
        return cont, cate

    def get_loc_index(self, loc_cate):
        return self.loc_set.index(loc_cate)
    def add_data(self, data):
        s = State(data.activity, data.location, data.duration)
        