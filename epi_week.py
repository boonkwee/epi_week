import datetime

class epi_week:
    def __init__(self, year: int=datetime.date.today().year, start_day:str='sun'):
        '''
        Epidemiological Week calculator class Constructor
        Parameters
        ----------
        year : int, optional
            DESCRIPTION. The default is datetime.date.today().year.
        start_day : str, optional
            DESCRIPTION. The default is 'sun'.

        Returns
        -------
        None.

        '''
        self.year = year
        self.non_current_year = {}
        self.first_sunday = self.calculate_first_sunday()
        self.last_sunday = self.calculate_last_sunday()

        week_counter = 1
        current_sunday = self.first_sunday

        self.epiweek = {week_counter: current_sunday}
        while current_sunday < self.last_sunday:
            week_counter += 1
            current_sunday += datetime.timedelta(days=7)
            if current_sunday.year == year:
                self.epiweek[week_counter] = current_sunday


    def get_epi_number(self, dt) -> int:
        """
        Parameters
        ----------
        dt : TYPE
            DESCRIPTION. Date in the datetime.date type

        Raises
        ------
        ValueError
            DESCRIPTION. if parameter given is not datetime.date type

        Returns
        -------
        epi_num : TYPE
            DESCRIPTION. The epidemiological week number

        """
        if not hasattr(dt, 'year'):
            raise ValueError('Not datetime type')
        if dt.year != self.year:
            if self.non_current_year.get(dt.year, None) is None:
                self.non_current_year[dt.year] = epi_week(year=dt.year)
            epi_num = self.non_current_year[dt.year].get_epi_number(dt)
            return epi_num
        max_epi_num = len(self.epiweek)
        for epi_num, wk in self.epiweek.items():
            calculated_epi_num = epi_num + 1
            if calculated_epi_num > max_epi_num:  # already beyond the current year
                calculated_epi_num = calculated_epi_num - max_epi_num
                return calculated_epi_num
            else:
                if dt >= wk and dt < self.epiweek[epi_num+1]:
                    return epi_num


    def get_epi_week_range(self, epi_num: int, date_format:str='%d-%b') -> str:
        """
        Parameters
        ----------
        epi_num : int
            DESCRIPTION. The epidemiological week number

        Returns
        -------
        str
            DESCRIPTION. The date range of the epidemiological week in the
            format dd-mmm to dd-mmm
            e.g. "01-Jan to 07-Jan"

        """
        if not 0 < epi_num <= len(self.epiweek):
            return ''
        first_day_of_week = self.epiweek[epi_num]
        last_day_of_week = first_day_of_week + datetime.timedelta(days=6)
        return '%s to %s' % (first_day_of_week.strftime(date_format),
                             last_day_of_week.strftime(date_format)
                             )

    def get_week_start(self, epi_num: int) -> datetime.date:
        if not 0 < epi_num <= len(self.epiweek):
            raise ValueError('epidemiological week number out of range')
        first_day_of_week = self.epiweek[epi_num]
        return first_day_of_week


    def get_week_end(self, epi_num: int) -> datetime.date:
        if not 0 < epi_num <= len(self.epiweek):
            raise ValueError('epidemiological week number out of range')
        first_day_of_week = self.epiweek[epi_num]
        last_day_of_week = first_day_of_week + datetime.timedelta(days=6)
        return last_day_of_week


    def calculate_first_sunday(self):
        year = self.year
        # Create a datetime object for January 1st of the given year
        january_first = datetime.date(year, 1, 1)

        # Calculate the day of the week for January 1st (0 is Monday, 6 is Sunday)
        day_of_week = january_first.weekday()
        if day_of_week < 6:    # 1 Jan is not Sunday, then first sunday is last sunday of prev year
            prev_year = year -1
            e = epi_week(year=prev_year)
            first_sunday = e.last_sunday
            self.non_current_year[prev_year] = e
        else:
            first_sunday = january_first

        # Calculate the number of days to add to reach the first Sunday
        # days_to_add = (6 - day_of_week) % 7

        # Calculate the date of the first Sunday
        # first_sunday = january_first + datetime.timedelta(days=days_to_add)

        return first_sunday


    def calculate_last_sunday(self):
        year = self.year
        sunday = 6
        # Create a datetime object for December 31st of the given year
        december_31st = datetime.date(year, 12, 31)

        # Calculate the day of the week for December 31st (0 is Monday, 6 is Sunday)
        day_of_week = december_31st.weekday()
        if day_of_week == sunday:
            last_sunday = december_31st
        else:
            # Calculate the number of days to subtract to reach the last Sunday
            days_to_subtract = day_of_week

            # Calculate the date of the last Sunday
            last_sunday = december_31st - datetime.timedelta(days=days_to_subtract + 1)

        return last_sunday

