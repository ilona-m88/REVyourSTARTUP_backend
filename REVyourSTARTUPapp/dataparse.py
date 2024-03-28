# File to provide functions to parse through JSON data for various views

# REVFORM json parser to flatten into a format to be serialized
def flatten_revform_json(valuation_data, reality_check):
    # Valuation Paramters
    year3_goals = valuation_data['hit3YearGoals']
    exit_years = valuation_data['exitYears']

    rev_form_dict = {
        'last_year_total_revenue': valuation_data['lastYearTotalRevenue'],
        'amount_needed': valuation_data['amountNeeded'],
        'three_years_effective_interest': year3_goals['3years']['effectiveInterest'],
        'five_years_effective_interest': year3_goals['5years']['effectiveInterest'],
        'seven_years_effective_interest': year3_goals['7years']['effectiveInterest'],
        'revenue_multiplier': valuation_data['revenueMultiplier'],
        'exit_amount': valuation_data['exitAmount'],
        'year0_percentage': exit_years['year0']['percentage'],
        'year0_revenue': exit_years['year0']['revenue'],
        'year0_force_to': exit_years['year0']['ForceTo'],
        'year1_percentage': exit_years['year1']['percentage'],
        'year1_revenue': exit_years['year1']['revenue'],
        'year1_force_to': exit_years['year1']['ForceTo'],
        'year2_percentage': exit_years['year2']['percentage'],
        'year2_revenue': exit_years['year2']['revenue'],
        'year2_force_to': exit_years['year2']['ForceTo'],
        'year3_percentage': exit_years['year3']['percentage'],
        'year3_revenue': exit_years['year3']['revenue'],
        'year3_force_to': exit_years['year3']['ForceTo'],
        'year4_percentage': exit_years['year4']['percentage'],
        'year4_revenue': exit_years['year4']['revenue'],
        'year4_force_to': exit_years['year4']['ForceTo'],
        'year5_percentage': exit_years['year5']['percentage'],
        'year5_revenue': exit_years['year5']['revenue'],
        'year5_force_to': exit_years['year5']['ForceTo'],
        'equity_percentage': valuation_data['equityPercentage'],
        'year3_company_worth': valuation_data['year3CompanyWorth'],
        'exit_revenue_multiplier': valuation_data['exitRevenueMultiplier'],
        'revenue_needed_year3': valuation_data['revenueNeededYear3'],
        'growth_projection': valuation_data['growthProjection'],
        'total_market': reality_check['totalMarket'],
        'captured_at_year5': reality_check['capturedAtYear5']
    }

    return rev_form_dict


def flatten_revform_rows_json(customer_segment, index_name):
    row_count = customer_segment['rowCount']
    row_index_dict = {'revform_rows_name': index_name, 'row_count': row_count}

    row_dict = {}
    row_num = 1
    for row in range(len(customer_segment['rows'])):
        single_row = {}
        single_row['segment_name'] = customer_segment['rows'][row]['segmentName']
        single_row['avg_revenue_per_customer'] = customer_segment['rows'][row]['avgRevenuePerCustomer']
        single_row['quick_modeling_percentage'] = customer_segment['rows'][row]['quickModelingPercentage']
        single_row['revenue'] = customer_segment['rows'][row]['revenue']
        single_row['customers'] = customer_segment['rows'][row]['customers']
        single_row['your_percentage'] = customer_segment['rows'][row]['yourPercentage']
        single_row['total_revenue'] = customer_segment['rows'][row]['totalRevenue']
        row_dict[row_num] = single_row
        row_num += 1
    
    return {'RevFormRowsIndex': row_index_dict, 'RevFormRows': row_dict}


def build_revform_json(revform, year1, year2, year3):
    valuation_parameters = {
        "lastYearTotalRevenue": revform.last_year_total_revenue,
        "amountNeeded": revform.amount_needed,
        "hit3YearGoals": {
            "3years": {
                "effectiveInterest": revform.three_years_effective_interest
            },
            "5years": {
                "effectiveInterest": revform.five_years_effective_interest
            },
            "7years": {
                "effectiveInterest": revform.seven_years_effective_interest
            }
        },
        "revenueMultiplier": revform.revenue_multiplier,
        "exitAmount": revform.exit_amount,
        "exitYears": {
            "year0": {
                "percentage": revform.year0_percentage,
                "revenue": revform.year0_revenue,
                "ForceTo": revform.year0_force_to
            },
            "year1": {
                "percentage": revform.year1_percentage,
                "revenue": revform.year1_revenue,
                "ForceTo": revform.year1_force_to
            },
            "year2": {
                "percentage": revform.year2_percentage,
                "revenue": revform.year2_revenue,
                "ForceTo": revform.year2_force_to
            },
            "year3": {
                "percentage": revform.year3_percentage,
                "revenue": revform.year3_revenue,
                "ForceTo": revform.year3_force_to
            },
            "year4": {
                "percentage": revform.year4_percentage,
                "revenue": revform.year4_revenue,
                "ForceTo": revform.year4_force_to
            },
            "year5": {
                "percentage": revform.year5_percentage,
                "revenue": revform.year5_revenue,
                "ForceTo": revform.year5_force_to
            }
        },
        "equityPercentage": revform.equity_percentage,
        "year3CompanyWorth": revform.year3_company_worth,
        "exitRevenueMultiplier": revform.exit_revenue_multiplier,
        "revenueNeededYear3": revform.revenue_needed_year3,
        "growthProjection": revform.growth_projection
    }

    reality_check = {
        "totalMarket": revform.total_market,
        "capturedAtYear5": revform.captured_at_year5
    }

    return {"valuationParameters": valuation_parameters, "realityCheck1": reality_check, "customerSegmentsYear3": year3, "customerSegmentsYear2": year2, "customerSegmentsYear1": year1}


def build_customer_segments_json(revform_index_data, revform_row_data):
    rows = []
    for i in range(len(revform_row_data)):
        rows.append(
            {
                "segmentName": revform_row_data[i]["segment_name"],
                "avgRevenuePerCustomer": float(revform_row_data[i]["avg_revenue_per_customer"]),
                "quickModelingPercentage": revform_row_data[i]["quick_modeling_percentage"],
                "revenue": float(revform_row_data[i]["revenue"]),
                "customers": revform_row_data[i]["customers"],
                "yourPercentage": revform_row_data[i]["your_percentage"],
                "totalRevenue": float(revform_row_data[i]["total_revenue"])
            }
        )
    
    row_count = revform_index_data["row_count"]

    return {"rowCount": row_count, "rows": rows}


def flatten_pro_forma_json(pro_forma_startup_factors):
    calendar = pro_forma_startup_factors["calendar"]
    profit_first = pro_forma_startup_factors["profitFirst"]
    income_and_expenses = pro_forma_startup_factors["incomeAndExpenses"]
    cash_flow = pro_forma_startup_factors["cashFlow"]
    max_headcount_per_year = pro_forma_startup_factors["maxHeadCountPerYear"]

    pro_forma_dict = {
        'start_year': calendar["startYear"],
        'start_month': calendar["startMonth"],
        'start_capital': pro_forma_startup_factors["startCapital"],
        'number_of_founders': pro_forma_startup_factors["foundersDraw"]["numberOfFounders"],
        'year1_pid': profit_first["percentageOfIncomeDistributed"]["year1"],
        'year2_pid': profit_first["percentageOfIncomeDistributed"]["year2"],
        'year3_pid': profit_first["percentageOfIncomeDistributed"]["year3"],
        'year4_pid': profit_first["percentageOfIncomeDistributed"]["year4"],
        'year5_pid': profit_first["percentageOfIncomeDistributed"]["year5"],
        'include_investments': profit_first["includeInvestments"],
        'year1_income': income_and_expenses["years"]["year1"]["income"],
        'year1_distribution': income_and_expenses["years"]["year1"]["distribution"],
        'year1_expenses': income_and_expenses["years"]["year1"]["expenses"],
        'year1_margin': income_and_expenses["years"]["year1"]["margin"],
        'year2_income': income_and_expenses["years"]["year2"]["income"],
        'year2_distribution': income_and_expenses["years"]["year2"]["distribution"],
        'year2_expenses': income_and_expenses["years"]["year2"]["expenses"],
        'year2_margin': income_and_expenses["years"]["year2"]["margin"],
        'year3_income': income_and_expenses["years"]["year3"]["income"],
        'year3_distribution': income_and_expenses["years"]["year3"]["distribution"],
        'year3_expenses': income_and_expenses["years"]["year3"]["expenses"],
        'year3_margin': income_and_expenses["years"]["year3"]["margin"],
        'year4_income': income_and_expenses["years"]["year4"]["income"],
        'year4_distribution': income_and_expenses["years"]["year4"]["distribution"],
        'year4_expenses': income_and_expenses["years"]["year4"]["expenses"],
        'year4_margin': income_and_expenses["years"]["year4"]["margin"],
        'year5_income': income_and_expenses["years"]["year5"]["income"],
        'year5_distribution': income_and_expenses["years"]["year5"]["distribution"],
        'year5_expenses': income_and_expenses["years"]["year5"]["expenses"],
        'year5_margin': income_and_expenses["years"]["year5"]["margin"],
        'exclude_depreciation': cash_flow["excludeDepreciation"],
        'year1_first_negative_month': cash_flow["minimumCashOnHandPerYear"]["year1"]["firstNegativeMonth"],
        'year1_first_negative_month_amount': cash_flow["minimumCashOnHandPerYear"]["year1"]["firstNegativeMonthAmount"],
        'year1_minimum_this_year': cash_flow["minimumCashOnHandPerYear"]["year1"]["minimumThisYear"],
        'year2_first_negative_month': cash_flow["minimumCashOnHandPerYear"]["year2"]["firstNegativeMonth"],
        'year2_first_negative_month_amount': cash_flow["minimumCashOnHandPerYear"]["year2"]["firstNegativeMonthAmount"],
        'year2_minimum_this_year': cash_flow["minimumCashOnHandPerYear"]["year2"]["minimumThisYear"],
        'year3_first_negative_month': cash_flow["minimumCashOnHandPerYear"]["year3"]["firstNegativeMonth"],
        'year3_first_negative_month_amount': cash_flow["minimumCashOnHandPerYear"]["year3"]["firstNegativeMonthAmount"],
        'year3_minimum_this_year': cash_flow["minimumCashOnHandPerYear"]["year3"]["minimumThisYear"],
        'year1_founders': max_headcount_per_year["year1"]["founders"],
        'year1_salaries': max_headcount_per_year["year1"]["salaries"],
        'year1_fulltime': max_headcount_per_year["year1"]["fulltime"],
        'year1_parttime': max_headcount_per_year["year1"]["parttime"],
        'year2_founders': max_headcount_per_year["year2"]["founders"],
        'year2_salaries': max_headcount_per_year["year2"]["salaries"],
        'year2_fulltime': max_headcount_per_year["year2"]["fulltime"],
        'year2_parttime': max_headcount_per_year["year2"]["parttime"],
        'year3_founders': max_headcount_per_year["year3"]["founders"],
        'year3_salaries': max_headcount_per_year["year3"]["salaries"],
        'year3_fulltime': max_headcount_per_year["year3"]["fulltime"],
        'year3_parttime': max_headcount_per_year["year3"]["parttime"],
        'year4_founders': max_headcount_per_year["year4"]["founders"],
        'year4_salaries': max_headcount_per_year["year4"]["salaries"],
        'year4_fulltime': max_headcount_per_year["year4"]["fulltime"],
        'year4_parttime': max_headcount_per_year["year4"]["parttime"],
        'year5_founders': max_headcount_per_year["year5"]["founders"],
        'year5_salaries': max_headcount_per_year["year5"]["salaries"],
        'year5_fulltime': max_headcount_per_year["year5"]["fulltime"],
        'year5_parttime': max_headcount_per_year["year5"]["parttime"]
    }

    return pro_forma_dict


def flatten_pro_forma_founders_json(pro_forma_founders_data):
    founders_dict = {
        'name': pro_forma_founders_data["name"],
        'compensation_at_year3': pro_forma_founders_data["compensationAtYear3"],
        'year1_percent': pro_forma_founders_data["year1"]["year1percent"],
        'year1_total': pro_forma_founders_data["year1"]["total"],
        'year2_percent': pro_forma_founders_data["year2"]["year2percent"],
        'year2_total': pro_forma_founders_data["year2"]["total"],
        'year3_percent': pro_forma_founders_data["year3"]["year3percent"],
        'year3_total': pro_forma_founders_data["year3"]["total"],
        'year4_percent': pro_forma_founders_data["year4"]["year4percent"],
        'year4_total': pro_forma_founders_data["year4"]["total"],
        'year5_percent': pro_forma_founders_data["year5"]["year5percent"],
        'year5_total': pro_forma_founders_data["year5"]["total"]
    }

    return founders_dict

