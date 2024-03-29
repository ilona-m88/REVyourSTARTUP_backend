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
