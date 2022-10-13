import numpy as np
from dateutil.relativedelta import relativedelta as rd
import datetime as dt
import calendar as cd 

class Calculations:

    def __init__(self):
        self.units = "metric"
            

    def ExponentialDecline(self,q,Q,qi,Qi,thanging,MaxYears=30,qf=1):
        ai=(qi-q)/((Q-Qi)*1000)
        DurationDays=np.log(qi/qf)/ai
        DurationYears,LastProduction = self.Duration(thanging,DurationDays)
        if DurationYears>MaxYears:
            DurationYears, DurationDays, LastProduction = self.DurationYearsGreaterThanMaxYears(MaxYears,thanging) 
            qf=qi*np.exp(-ai*DurationDays)
        else:
            LastProduction=thanging+rd(days=DurationDays)

        EUR=Qi+(qi-qf)/(ai*1000)

        return ai,EUR,DurationYears,LastProduction,qf

    def HyperbolicDecline(self,q,Q,qi,Qi,N,thanging,MaxYears=30,paf=1,qf=1):

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

        return ai,EUR,DurationYears,LastProduction,af,qf

    def HarmonicDecline(self,q,Q,qi,Qi,thanging,MaxYears=30,paf=1,qf=1):
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
        return ai,EUR,DurationYears,LastProduction,af,qf

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

#m = Calculations()


#ai,EUR,DurationYears,LastProduction,af,qf = m.HyperbolicDecline(290,2496.5,200,2548.3,1.25,dt.datetime(2018,2,1),1.5,1,50)
#print(ai*36525,EUR,DurationYears,LastProduction,af*36525,qf)
