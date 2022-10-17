import numpy as np
from dateutil.relativedelta import relativedelta as rd
import datetime as dt
import calendar as cd 

class Calculations:

    def __init__(self):
        self.units = "metric"
            

    def ExponentialDecline_Time(self,t, q, ti, qi, thanging, MaxYears=30,qf=1, month_min = 0, month_hang = 1):
        # Feed in t in months?
        ai = np.log(qi/q)/t # Unit: 1/month (1/time)

        # rate at max time
        q_mt = qi * np.exp(-ai * MaxYears * 12)

        if q_mt > qf:
            # The years is the limiting variable  
            ts = np.concatenate((np.arange(t, ti, (ti - t)/50),np.arange(ti, MaxYears, (MaxYears - ti)/50)))
            qs = qi * np.exp(-ai * (ti - ts))
            
            qf = q_mt
            DurationYears = MaxYears
            t_last = ti + DurationYears

        else:
            # The qf is the limiting variable
            t_last = ti + np.log(qf/qi)/(-ai) # Months
            ts = np.concatenate((np.arange(t, ti, (ti - t)/50),np.arange(ti, t_last, (t_last - ti)/50)))
            qs = qi * np.exp(-ai * (ti - ts))

            qf = qf
            DurationYears = np.log(qf/qi)/(-ai) / 12
        
        LastProduction = thanging + rd(years=DurationYears)   
        EUR = qi/ (ai*12/365) * (1 - np.exp(-ai*t_last))

        return ai*12/365, EUR, DurationYears, LastProduction, qf, ts, qs

    def ExponentialDecline_Cum(self, q, Q, qi, Qi, thanging, MaxYears=30, qf=1, month_min = 0, month_hang = 1):
        ai=(qi-q)/((Q-Qi)*1000)
        DurationDays=np.log(qi/qf)/ai
        DurationYears,LastProduction = self.Duration(thanging,DurationDays)
        if DurationYears>MaxYears:
            DurationYears, DurationDays, LastProduction = self.DurationYearsGreaterThanMaxYears(MaxYears,thanging) 
            qf=qi*np.exp(-ai*DurationDays)
        else:
            LastProduction=thanging+rd(days=DurationDays)

        EUR=Qi+(qi-qf)/(ai*1000)

        Qs = np.concatenate((np.arange(Q, Qi, (Qi - Q)/50),np.arange(Qi, EUR, (EUR - Qi)/50)))
        qs = qi - 1000 * (Qs - Qi) * ai
        
        ai_months = ai * 365/12
        ts = -np.log(1 - 1000*(Qs-Qi)/qi * ai)/ai_months + month_hang

        return ai,EUR,DurationYears,LastProduction,qf, 1000 * Qs, qs, ts

    def HyperbolicDecline_Cum(self, q, Q, qi, Qi, N, thanging, MaxYears=30, paf=1, qf=1, month_min = 0, month_hang = 1):

        ai=qi**N/((Q-Qi)*1000*(1-N))*((qi**(1-N))-q**(1-N))
        DurationDays=-1*np.power(qf/qi,-N)*(np.power(qf/qi,N)-1)/(N*ai)
        af=ai/(1+N*ai*DurationDays)
        DurationYears,LastProduction = self.Duration(thanging,DurationDays)

        if af*36525<paf:
            af=paf/36525
            DurationDays=(ai-af)/(ai*N*af)
            qf=qi/((1+N*ai*DurationDays)**(1/N))
            DurationYears,LastProduction = self.Duration(thanging,DurationDays)
        
        if DurationYears>MaxYears:
            DurationYears, DurationDays, LastProduction = self.DurationYearsGreaterThanMaxYears(MaxYears,thanging) 
            af=ai/(1+N*ai*DurationDays)
            qf=qi/np.power((1+N*ai*DurationDays),(1/N))

        EUR=Qi+(qi**N)/(ai*(1-N))*((qi**(1-N))-(qf**(1-N)))/1000

        Qs = np.concatenate((np.arange(Q,Qi,(Qi - Q)/50), np.arange(Qi, EUR, (EUR - Qi)/50)))
        qs = (qi ** (1-N) - 1000 * (Qs-Qi) * (ai*(1-N)/qi**N)) ** (1/(1-N))

        ai_months = ai * 365/12
        ts = month_hang + (qi**N/(N*ai_months)) * (qs**-N-qi**-N)

        return ai,EUR,DurationYears,LastProduction,af,qf, 1000 * Qs, qs, ts

    def HarmonicDecline_Cum(self, q, Q, qi, Qi, thanging, MaxYears=30, paf=1, qf=1, month_min = 0, month_hang = 1):
        ai=qi/(1000*(Q-Qi))*np.log(qi/q)
        DurationDays=(qi-qf)/(ai*qf)
        af=ai/(1+ai*DurationDays)
        DurationYears,LastProduction = self.Duration(thanging,DurationDays)
        if af<paf/36525:
            af=paf/36525
            DurationDays=1/af-1/ai
            qf=qi/(1+ai*DurationDays)
            DurationYears,LastProduction = self.Duration(thanging,DurationDays)
        
        if DurationYears>MaxYears:
            DurationYears,DurationDays,LastProduction = self.DurationYearsGreaterThanMaxYears(MaxYears,thanging) 
            af=ai/(1+ai*DurationDays)
            qf=qi/(1+ai*DurationDays)

        EUR=Qi+qi/(ai*1000)*np.log(qi/qf)

        try:
            Qs = np.concatenate((np.arange(Q,Qi,(Qi - Q)/50), np.arange(Qi, EUR, (EUR - Qi)/50)))
        except:
            Qs = np.concatenate((np.arange(Q,Qi,(Qi - Q)/50), np.arange(Qi, Qi+0.001, (0.001)/50)))
        qs = qi * np.exp(-1000*(Qs-Qi) * ai/qi)
        
        ai_months = ai * 365/12
        ts = month_hang - qi/ai_months * ((-1/qs)-(-1/qi))

        return ai,EUR,DurationYears,LastProduction,af,qf, 1000*Qs, qs, ts

    def DisplayDi(self,ai):
            '''Get af stuff figured out. Maybe do return ai*36525 and af*36525 instead of a function itself.'''
            Di=ai*36525

    def Duration(self,thanging,DurationDays):
        MonthOfTHanging=thanging.month
        DayOfTHanging=thanging.day

        try:
            LastProduction = thanging+dt.timedelta(DurationDays)
        except OverflowError:
            LastProduction = thanging+dt.timedelta(36500)

        YearOfLastProduction=LastProduction.year
        StartOfYearOfLastProduction=dt.datetime(year=YearOfLastProduction,month=MonthOfTHanging,day=DayOfTHanging)
        StartOfYearAfterYearOfLastProduction=dt.datetime(year=YearOfLastProduction+1,month=MonthOfTHanging,day=DayOfTHanging)
        if LastProduction > StartOfYearOfLastProduction:
            YearElapsed=LastProduction-StartOfYearOfLastProduction
        else:
            YearElapsed=LastProduction-StartOfYearOfLastProduction+dt.timedelta(365+cd.isleap(YearOfLastProduction))
        #YearElapsed=LastProduction-StartOfYearOfLastProduction
        YearDuration=StartOfYearAfterYearOfLastProduction-StartOfYearOfLastProduction
        YearFraction=YearElapsed/YearDuration
        NumberOfYears=rd(LastProduction,thanging).years
        DurationYears=NumberOfYears+YearFraction
        return DurationYears,LastProduction

    def DurationYearsGreaterThanMaxYears(self, MaxYears, thanging):
        if isinstance(MaxYears,int): 
            DurationYears=MaxYears
            LastProduction=thanging+rd(years=DurationYears)
        else:
            DurationYears=int(MaxYears)
            YearFraction=MaxYears-DurationYears
            YearOfTHanging=thanging.year
            MonthOfTHanging=thanging.month
            DayOfTHanging=thanging.day
            StartOfYearOfLastProduction=dt.datetime(year=YearOfTHanging+DurationYears,month=MonthOfTHanging,day=DayOfTHanging)
            YearOfLastProduction=StartOfYearOfLastProduction.year
            DaysForYearOfLastProduction=dt.timedelta(YearFraction*(365+cd.isleap(YearOfLastProduction)))
            LastProduction=DaysForYearOfLastProduction+StartOfYearOfLastProduction
            DurationYears=MaxYears
        DurationDays=(LastProduction-thanging).days
        return DurationYears,DurationDays,LastProduction
