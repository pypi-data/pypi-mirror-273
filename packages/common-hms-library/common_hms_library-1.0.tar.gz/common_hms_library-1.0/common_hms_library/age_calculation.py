from datetime import datetime

class AgeCalculator:
    def __init__(self, dob):
        self.dob = dob

    def calculate_age(self):
        """
        Calculate age based on the given birth date.
        """

        born = datetime.strptime(self.dob.strftime("%Y-%m-%d"), "%Y-%m-%d")
        today = datetime.now()
        total_months = (today.year - born.year) * 12 + (today.month - born.month)
        age = total_months / 12
        age = round(age, 2)
        return age
