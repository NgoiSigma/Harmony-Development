class GeoResonantPulse:
    def __init__(self, location, date):
        self.location = location
        self.date = date
        self.signals = []

    def check_volcanic_activity(self):
        if self.location in ['Oregon', 'Chile', 'Axial Seamount']:
            self.signals.append('Sub-crustal tension rising')

    def check_infowaves(self):
        if self.location in ['Ukraine', 'Israel', 'Switzerland']:
            self.signals.append('Information flux shift')

    def check_ethic_field(self):
        if self.location in ['Odessa', 'Tibet', 'Mecca']:
            self.signals.append('Moral inversion or purification in process')

    def forecast(self):
        self.check_volcanic_activity()
        self.check_infowaves()
        self.check_ethic_field()
        return {
            'Location': self.location,
            'Date': self.date,
            'Signals': self.signals
        }

