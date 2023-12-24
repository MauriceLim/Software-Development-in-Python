import numpy as np

def GMWB_pricing(assumption, scenario, parameter,policy, mortality):
    np.random.seed(parameter['seed'])
    result = []
    for k in range(len(policy)):
        initial_premium = policy[k]['initial_premium']
        issue_age = policy[k]['issue_age']
        fee_pct_av = policy[k]['fee_pct_av']
        benefit_type = policy[k]['benefit_type']
        guarantee_rate = policy[k]['guarantee_wd_rate']

        r = scenario['risk_free_rate']
        q = scenario['dividend_yield']
        vol = scenario['volatility']

        dur = parameter['proj_periods']
        num_paths = parameter['num_paths']

        mortality_multiplier = assumption['mortality_multiplier']
        min_wd_delay = assumption['min_wd_delay']
        wd_age = assumption['wd_age']

        qx = mortality['qx']

        dur_v = np.arange(0,dur+1,1)
        age_v = issue_age + dur_v
        prob_surv = np.zeros(len(dur_v))
        prob_surv[0] = 1
        for t in range(1, len(dur_v)):
            if age_v[t] >= 115:
                prob_surv[t] = 0
            else:
                prob_surv[t] = prob_surv[t-1] * (1 - qx[age_v[t]] * mortality_multiplier)
        discount_v = np.exp(-r*dur_v)

        prices = []
        for i in range(1,num_paths):
            benefit_base = np.zeros(dur+1)
            av_end_of_period = np.zeros(dur+1)
            remaining_principal = np.zeros(dur+1)
            av_beg_of_period = np.zeros(dur+1)
            fee = np.zeros(dur+1)
            av_after_fee = np.zeros(dur+1)
            av_after_return = np.zeros(dur+1)
            av_after_wd = np.zeros(dur+1)
            wd_claim = np.zeros(dur+1)
            av_end_of_period[0] = initial_premium
            benefit_base[:] = initial_premium
            remaining_principal[0] = initial_premium
            epsilon = np.random.normal(size=dur+1)
            found_negative = False
            
            for j in range(1, dur+1):
                av_beg_of_period[j] = av_end_of_period[j-1]
                fee[j] = av_beg_of_period[j] * fee_pct_av
                av_after_fee[j] = av_beg_of_period[j] - fee[j]
                av_after_return[j] = av_after_fee[j] * np.exp((r-q-0.5*(vol**2))*1+vol*epsilon[j]*np.sqrt(1))
                wd_amt = 0
                
                if (age_v[j]>wd_age) and (dur_v[j] > min_wd_delay):
                    if benefit_type == 'FOR_LIFE':
                        wd_amt = benefit_base[j] * guarantee_rate
                    elif benefit_type == 'PRINCIPAL_BACK':
                        wd_amt = min(benefit_base[j] * guarantee_rate, max(remaining_principal[j-1],av_after_return[j]))
                remaining_principal[j] = remaining_principal[j-1] - wd_amt
                av_after_wd[j] = av_after_return[j] - wd_amt
                
                if av_after_wd[j] < 0:
                    av_after_wd[j] = 0

                if av_after_wd[j] <= 0 and not found_negative: # account for first time account depleted 
                    av_after_wd[j] = abs(av_after_return[j] - wd_amt)
                    found_negative = True
                    wd_claim[j] = max(wd_amt - av_after_wd[j],0)
                    av_after_wd[j] = 0
                    continue 
                
                wd_claim[j] = max(wd_amt - av_after_wd[j],0)
                av_end_of_period[j] = av_after_wd[j]
            
            CF = discount_v * prob_surv * wd_claim
            prices.append(np.sum(CF))
        result.append((policy[k]['id'], np.average(prices)))
    return(result)


