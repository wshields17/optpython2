import QuantLib as ql



def binomialmodels(stockprice,strikeprice,volatility,intrate,calcdate,expdate,divrate,opttype,modelname,steps):
    day_count = ql.Actual365Fixed()
    calendar = ql.UnitedStates()  
    
    calculation_date = ql.Date(calcdate.day, calcdate.month,calcdate.year)
    if opttype == "p":
        option_type = ql.Option.Put
    else:
        option_type = ql.Option.Call    
    exp_date = ql.Date(expdate.day,expdate.month,expdate.year)
    ql.Settings.instance().evaluationDate = calculation_date
    payoff = ql.PlainVanillaPayoff(option_type, strikeprice)
    exercise = ql.AmericanExercise(calculation_date,exp_date)
    american_option = ql.VanillaOption(payoff, exercise)
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(stockprice))

    flat_ts = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, intrate, day_count))
    dividend_yield = ql.YieldTermStructureHandle(ql.FlatForward(calculation_date, divrate, day_count))
    flat_vol_ts = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(calculation_date, calendar, volatility, day_count))
    bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_yield, flat_ts, flat_vol_ts)

    binomial_engine = ql.BinomialVanillaEngine(bsm_process, modelname, steps)
    american_option.setPricingEngine(binomial_engine)
    
    return american_option.NPV()

