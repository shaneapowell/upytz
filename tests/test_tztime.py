from utztime import TZTime, EPOCH
import unittest
import time
from utztime.tz.us import America_New_York
from utztime.tz.us import America_Los_Angeles
from utztime.tz.us import America_Chicago
from utztime.tz.us import America_Anchorage


class test_tz_time(unittest.TestCase):


    def test_create_default_tztime(self):

        # Given
        now = int(time.time())

        # When
        t = TZTime()

        # Then
        assert now <= t.time()


    def test_create_specific_utc_time(self):


        # When
        t = TZTime.create(2001, 2, 3, 4, 5, 6)

        # Then
        assert t.year() == 2001
        assert t.month() == 2
        assert t.day() == 3
        assert t.hour() == 4
        assert t.minute() == 5
        assert t.second() == 6
        assert t.dayOfWeek() == 5
        assert t.tz() is None


    def test_create_specific_TZ_time(self):

        # When
        t = TZTime.create(2022, 1, 7, 5, 0, 0, America_Anchorage)

        # Then
        assert t.year() == 2022
        assert t.month() == 1
        assert t.day() == 7
        assert t.hour() == 5
        assert t.minute() == 0
        assert t.second() == 0
        assert t.dayOfWeek() == 4
        assert t.tz() == America_Anchorage


    def test_toiso_with_specific_TZ(self):

        # When
        t = TZTime.create(2022, 1, 7, 5, 0, 0, America_Anchorage)

        # Then
        assert t.toISO8601() == "2022-01-07T05:00:00-09:00", t.toISO8601()


    def test_UTC_is_before_EST(self):

        # Given
        utc = TZTime.create(2001, 2, 3, 4, 5, 6)
        est = TZTime.create(2001, 2, 3, 4, 5, 6, America_New_York)

        # Then
        assert utc < est


    def test_PST_is_after_EST(self):

        # Given
        pst = TZTime.create(2001, 2, 3, 4, 5, 6, America_Los_Angeles)
        est = TZTime.create(2001, 2, 3, 4, 5, 6, America_New_York)

        # Then
        assert pst > est


    def test_time_eq(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 6, America_Los_Angeles)
        t2 = TZTime.create(2001, 2, 3, 4, 5, 6, America_Los_Angeles)
        t3 = TZTime.create(2001, 2, 3, 7, 5, 6, America_New_York)

        # Then
        assert t1 == t2
        assert t1 == t3
        assert t2 == t3


    def test_time_ne(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 6, America_Los_Angeles)
        t2 = TZTime.create(2001, 2, 3, 4, 5, 7, America_Los_Angeles)
        t3 = TZTime.create(2001, 2, 3, 7, 5, 8, America_New_York)

        # Then
        assert t1 != t2
        assert t1 != t3
        assert t2 != t3


    def test_time_gt(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 7, America_Los_Angeles)
        t2 = TZTime.create(2001, 2, 3, 4, 5, 6, America_Los_Angeles)
        t3 = TZTime.create(2001, 2, 3, 7, 5, 6, America_New_York)

        # Then
        assert t1 > t2
        assert t1 != t2
        assert t1 > t3
        assert t1 != t3


    def test_time_lt(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)
        t2 = TZTime.create(2001, 2, 3, 4, 5, 6, America_Los_Angeles)
        t3 = TZTime.create(2001, 2, 3, 7, 5, 6, America_New_York)

        # Then
        assert t1 < t2
        assert t1 != t2
        assert t1 < t3
        assert t1 != t3


    def test_time_ge(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 7, America_Los_Angeles)
        t2 = TZTime.create(2001, 2, 3, 4, 5, 6, America_Los_Angeles)
        t3 = TZTime.create(2001, 2, 3, 7, 5, 6, America_New_York)

        # Then
        assert t1 >= t2
        assert t1 != t2
        assert t1 >= t3
        assert t1 != t3
        assert t2 >= t3
        assert t3 == t3


    def test_time_le(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)
        t2 = TZTime.create(2001, 2, 3, 4, 5, 6, America_Los_Angeles)
        t3 = TZTime.create(2001, 2, 3, 7, 5, 6, America_New_York)

        # Then
        assert t1 <= t2
        assert t1 != t2
        assert t1 <= t3
        assert t1 != t3
        assert t2 <= t3
        assert t3 == t3


    def test_pre_epoch_time(self):

        # Then
        with self.assertRaises(Exception):
            # When
            TZTime.create(1931, 2, 3, 4, 5, 6)


    def test_toLocal_near_epoch_doesnt_fail(self):

        # Given
        t1 = EPOCH.plusHours(1).toTimezone(America_Los_Angeles)

        # When
        tISO = t1.toISO8601()

        # Then
        assert f"{EPOCH.year() - 1}-12-31" in tISO


    def test_plus_seconds(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusSeconds(70)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 6
        assert t2.second() == 15
        assert t2.tz() == America_Los_Angeles


    def test_minus_seconds(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusSeconds(-70)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 3
        assert t2.second() == 55
        assert t2.tz() == America_Los_Angeles


    def test_plus_minutes(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusMinutes(70)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 5
        assert t2.minute() == 15
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles


    def test_minus_minutes(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusMinutes(-70)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 2
        assert t2.minute() == 55
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles

    def test_plus_hours(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusHours(70)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 2
        assert t2.day() == 6
        assert t2.hour() == 2
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles


    def test_minus_hours(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusHours(-70)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 1
        assert t2.day() == 31
        assert t2.hour() == 6
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles


    def test_plus_days(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusDays(70)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 4
        assert t2.day() == 14
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles


    def test_minus_days(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusDays(-70)

        # Then
        assert t2.year() == 2000
        assert t2.month() == 11
        assert t2.day() == 25
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles


    def test_plus_months(self):

        # Given
        t1 = TZTime.create(2011, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusMonths(70)

        # Then
        assert t2.year() == 2016
        assert t2.month() == 12
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles


    def test_minus_months(self):

        # Given
        t1 = TZTime.create(2011, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusMonths(-70)

        # Then
        assert t2.year() == 2005
        assert t2.month() == 4
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles


    def test_plus_years(self):

        # Given
        t1 = TZTime.create(2010, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusYears(50)

        # Then
        assert t2.year() == 2060
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles


    def test_minus_years(self):

        # Given
        t1 = TZTime.create(2055, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusYears(-20)

        # Then
        assert t2.year() == 2035
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles


    def test_with_second(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.withSecond(32)
        t3 = t1.withSecond(122)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 32
        assert t2.tz() == America_Los_Angeles

        assert t3.year() == 2001
        assert t3.month() == 2
        assert t3.day() == 3
        assert t3.hour() == 4
        assert t3.minute() == 7
        assert t3.second() == 2
        assert t3.tz() == America_Los_Angeles


    def test_with_minute(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.withMinute(32)
        t3 = t1.withMinute(122)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 32
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles

        assert t3.year() == 2001
        assert t3.month() == 2
        assert t3.day() == 3
        assert t3.hour() == 6
        assert t3.minute() == 2
        assert t3.second() == 5
        assert t3.tz() == America_Los_Angeles


    def test_with_hour(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.withHour(22)
        t3 = t1.withHour(26)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 22
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles

        assert t3.year() == 2001
        assert t3.month() == 2
        assert t3.day() == 4
        assert t3.hour() == 2
        assert t3.minute() == 5
        assert t3.second() == 5
        assert t3.tz() == America_Los_Angeles


    def test_with_day(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.withDay(10)
        t3 = t1.withDay(42)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 2
        assert t2.day() == 10
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles

        assert t3.year() == 2001
        assert t3.month() == 3
        assert t3.day() == 14
        assert t3.hour() == 4
        assert t3.minute() == 5
        assert t3.second() == 5
        assert t3.tz() == America_Los_Angeles


    def test_with_month(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.withMonth(10)
        t3 = t1.withMonth(16)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 10
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles

        assert t3.year() == 2002
        assert t3.month() == 4
        assert t3.day() == 3
        assert t3.hour() == 4
        assert t3.minute() == 5
        assert t3.second() == 5
        assert t3.tz() == America_Los_Angeles


    def test_with_year(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.withYear(2011)

        # Then
        assert t2.year() == 2011
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles


    def test_with_tz(self):

        # Given
        t1 = TZTime.create(2001, 2, 3, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.withTimezone(America_New_York)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_New_York

        # Also When
        t2 = t1.withTimezone(America_Chicago)

        # Then
        assert t2.year() == 2001
        assert t2.month() == 2
        assert t2.day() == 3
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Chicago



    def test_leap_year(self):

        # When
        t = TZTime.create(2020, 2, 29, 4, 5, 5, America_Los_Angeles)

        # Then
        assert t.year() == 2020
        assert t.month() == 2
        assert t.day() == 29
        assert t.hour() == 4
        assert t.minute() == 5
        assert t.second() == 5
        assert t.tz() == America_Los_Angeles


    def test_leap_year_plus(self):

        # Given
        t1 = TZTime.create(2020, 2, 28, 4, 5, 5, America_Los_Angeles)

        # When
        t2 = t1.plusDays(2)

        # Then
        assert t2.year() == 2020
        assert t2.month() == 3
        assert t2.day() == 1
        assert t2.hour() == 4
        assert t2.minute() == 5
        assert t2.second() == 5
        assert t2.tz() == America_Los_Angeles
