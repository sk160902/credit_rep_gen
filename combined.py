import json
import re
from jinja2 import Environment, FileSystemLoader

# Function to escape LaTeX special characters and replace underscores with spaces
def escape_latex(text):
    """
    Escapes LaTeX special characters in the given text and replaces '&' with '\&'.
    """
    if not isinstance(text, str):
        return text
    # Adding specific replacement for '&' to ensure it appears as '\&' in LaTeX
    replacements = {
        '%': r'\%', '$': r'\$', '#': r'\#',
        '&': r'\&',  # Handle ampersand specifically for LaTeX
        '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}', '\n': ' '
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text



# escaped_text = escape_latex("Mr. Jayanti Patel: 47 yrs of experience in Overseas corporate affairs & finance.")
# print(escaped_text)
# File paths
json_file_path = '/Users/Shreyas2/Desktop/Onfinance/credit/credit_reports-main/orig.json'
latex_template_path = 'combined.tex'
output_file_path = 'credit_report2.tex'

# Open and read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Extracting data from the JSON
company_profile = data["company_profile"]
promoter_data = data["promoters"]["promoters"]
key_issues = data["key_issues"]
key_strengths = data["key_strengths"]
Justification_of_Proposal = data["justification_of_proposal"]
industry_risks = data["industry_risks"]
brief_financials = data["brief_financials"]
peer_ratings = data["peer_ratings"]
concalls = data["Concalls"]
recent_news = data["Recent_News"]
# Cleaning and formatting company profile data
def clean_text(text):
    # Remove remaining \n and ** characters
    text = text.replace('\n', ' ')
    text = re.sub(r'\*\*', '', text)
    return text

def convert_to_list_format(profile):
    formatted_profile = {}
    for key, value in profile.items():
        items = value.split('\n- ')
        formatted_list = [clean_text(item.replace('- **', '').replace('**:', '')) for item in items]
        formatted_profile[key] = formatted_list
    return formatted_profile

formatted_profile = convert_to_list_format(company_profile)

names = [escape_latex(promoter["name"]) for promoter in promoter_data]
experiences = [escape_latex(promoter["experience"]) for promoter in promoter_data]
promoters_dict = {"names": names, "experiences": experiences}


# promoters_dict = {
#     "names": names,
#     "experiences": experiences
# }

# Preparing key issues data
key_issues_list = [
    (escape_latex(issue["point_header"]), escape_latex(issue["point_content"]))
    for issue in key_issues["issues"]
]

# Preparing key strengths data
key_strengths_list = [
    (escape_latex(strength["point_header"]), escape_latex(strength["point_content"]))
    for strength in key_strengths["strengths"]
]

# Preparing industry risks data
industry_risks_list = [
    (risk["sources"][0] if isinstance(risk["sources"], list) else risk["sources"], escape_latex(risk["risk"]))
    for risk in industry_risks["risks"]
]
# for risk in industry_risks["risks"]:
#     print("Source URL Type:", type(risk["sources"]))  # This should output <class 'str'>
#     print("Source URL:", risk["sources"])
# Preparing Justification of Proposal data
justification_of_proposal_list = [
    escape_latex(justification)
    for justification in data["justification_of_proposal"]
]

Recommendation_list= [
    escape_latex(Recommendation)
    for Recommendation in data["recommendation"]
]


def parse_financial_data(financial_section):
    result = []
    for entry in financial_section:
        if entry['value'] != 'NA':
            result.append({
                "year": escape_latex(entry['year']),
                "value": escape_latex(entry['value'])
            })
        else:
            result.append({
                "year": escape_latex(entry['year']),
                "value": 'NA'
            })
    return result

# Use the function to parse 'sales'
sales_data = parse_financial_data(data['brief_financials']['sales'])

# Process detailed financial data
financial_data = {}
for category, entries in data['financial_data']['table'].items():
    financial_data[category] = []
    for entry in entries:
        financial_data[category].append({
            "Quarter": escape_latex(entry['Quarter']),
            "Value": escape_latex(str(entry['Value']))
        })

# Preparing peer ratings data
peer_ratings_list = [
    {
        "company_name": escape_latex(rating["company_name"]),
        "long_term_rating": escape_latex(rating["long_term_rating"]),
        "short_term_rating": escape_latex(rating["short_term_rating"])
    }
    for rating in peer_ratings["ratings"]
]

peer_ratings_commentary = [escape_latex(comment) for comment in peer_ratings["commentary"]]

# Setup Jinja2 environment and load template file
financial_data = data["financial_data"]["table"]


years = [item["Quarter"] for item in financial_data["Sales"]]
value_sales = [item["Value"] for item in financial_data["Sales"]]
value_expenses = [item["Value"] for item in financial_data["Expenses"]]
OperatingProfit = [item["Value"] for item in financial_data["OperatingProfit"]]
OPM = [escape_latex(item["Value"]) for item in financial_data["OPM %"]]
OtherIncome = [item["Value"] for item in financial_data["OtherIncome"]]
Interest = [item["Value"] for item in financial_data["Interest"]]
Depreciation = [item["Value"] for item in financial_data["Depreciation"]]
ProfitBeforeTax = [item["Value"] for item in financial_data["ProfitBeforeTax"]]
TaxPercentage = [escape_latex(item["Value"]) for item in financial_data["TaxPercentage"]]
NetProfit = [item["Value"] for item in financial_data["NetProfit"]]
EPS = [item["Value"] for item in financial_data["EPS"]]

financial_dict = {
    "years": years,
    "value_sales": value_sales,
    "value_expenses": value_expenses,
    "OperatingProfit": OperatingProfit,
    "OPM": OPM,
    "OtherIncome": OtherIncome,
    "Interest": Interest,
    "Depreciation": Depreciation,
    "ProfitBeforeTax": ProfitBeforeTax,
    "TaxPercentage": TaxPercentage,
    "NetProfit": NetProfit,
    "EPS": EPS
}

financial_commentary = [escape_latex(comment) for comment in data["financial_data"]["commentary"]]

company_financials = {}
for category, entries in data['company_financials']['table'].items():
    company_financials[category] = []
    for entry in entries:
        company_financials[category].append({
            "Year": escape_latex(entry['Year']),
            "Value": escape_latex(str(entry['Value']))
        })

years = [entry["Year"] for entry in company_financials["Sales"]]
sales_values = [entry["Value"] for entry in company_financials["Sales"]]
expenses_values = [entry["Value"] for entry in company_financials["Expenses"]]
operating_profits = [entry["Value"] for entry in company_financials["OperatingProfit"]]
other_incomes = [entry["Value"] for entry in company_financials["OtherIncome"]]
interest_expenses = [entry["Value"] for entry in company_financials["Interest"]]
depreciation_costs = [entry["Value"] for entry in company_financials["Depreciation"]]
profits_before_tax = [entry["Value"] for entry in company_financials["ProfitBeforeTax"]]
tax_rate_percentages = [entry["Value"] for entry in company_financials["TaxPercentage"]]
net_profits = [entry["Value"] for entry in company_financials["NetProfit"]]
earnings_per_share = [entry["Value"] for entry in company_financials["EPS"]]
dividend_payout_rates = [entry["Value"] for entry in company_financials["DividendPayoutPercentage"]]


# Creating a dictionary to organize all the financial data
company_financials_dict = {
    "years": years,
    "sales": sales_values,
    "expenses": expenses_values,
    "operating_profits": operating_profits,
    "otherIncomes": other_incomes,
    "interestExpenses": interest_expenses,
    "depreciationCosts": depreciation_costs,
    "profitsbeforetax": profits_before_tax,
    "tax_rate_percentages": tax_rate_percentages,
    "netprofits": net_profits,
    "earningspershare": earnings_per_share,
    "dividendpayoutrates": dividend_payout_rates
}

debt_schedule_data = {}

# Loop over each main category in the debt_schedule table (e.g., 'borrowings', 'other_liabilities')
for main_category, subcategories in data['debt_schedule']['table'].items():
    debt_schedule_data[main_category] = {}
    
    # Loop over each subcategory like 'Total', 'LongTerm', etc., within 'borrowings' or 'other_liabilities'
    for subcategory, entries in subcategories.items():
        debt_schedule_data[main_category][subcategory] = []
        
        # Process each entry in the subcategory
        for entry in entries:
            # Prepare the Year and Value, ensuring Value is converted to string and checking for null values
            formatted_entry = {
                "Year": escape_latex(entry['Year']),
                "Value": escape_latex(str(entry['Value'])) if entry['Value'] is not None else "N/A"
            }
            debt_schedule_data[main_category][subcategory].append(formatted_entry)
debt_schedule_data = data["debt_schedule"]["table"]

# Extracting borrowing details
years = [item["Year"] for item in debt_schedule_data["borrowings"]["Total"]]
total_borrowings = [item["Value"] for item in debt_schedule_data["borrowings"]["Total"]]
long_term_borrowings = [item["Value"] for item in debt_schedule_data["borrowings"]["LongTerm"]]
short_term_borrowings = [item["Value"] for item in debt_schedule_data["borrowings"]["ShortTerm"]]
lease_liabilities = [item["Value"] for item in debt_schedule_data["borrowings"]["LeaseLiabilities"]]
other_borrowings = [item["Value"] for item in debt_schedule_data["borrowings"]["OtherBorrowings"]]

# Extracting other liability details
total_liabilities = [item["Value"] for item in debt_schedule_data["other_liabilities"]["Total"]]
non_controlling_interest = [item["Value"] for item in debt_schedule_data["other_liabilities"]["NonControllingInterest"]]
trade_payables = [item["Value"] for item in debt_schedule_data["other_liabilities"]["TradePayables"]]
advances_from_customers = [item["Value"] for item in debt_schedule_data["other_liabilities"]["AdvanceFromCustomers"]]
other_liability_items = [item["Value"] for item in debt_schedule_data["other_liabilities"]["OtherLiabilityItems"]]

# Combining all data into a single dictionary
debt_data_dict = {
    "years": years,
    "totalborrowings": total_borrowings,
    "longterm_borrowings": long_term_borrowings,
    "shorttermborrowings": short_term_borrowings,
    "leaseliabilities": lease_liabilities,
    "otherborrowings": other_borrowings,
    "totalliabilities": total_liabilities,
    "noncontrollinginterest": non_controlling_interest,
    "tradepayables": trade_payables,
    "advances_fromcustomers": advances_from_customers,
    "otherliabilityitems": other_liability_items
}

debt_schedule_commentary = [escape_latex(comment) for comment in data["debt_schedule"]["commentary"]]

# Setup Jinja2 environment and load template file
balance_sheet_analysis = data["balance_sheet_analysis"]["table"]

years = [item["Year"] for item in balance_sheet_analysis["EquityCapital"]]
EquityCapital = [item["Value"] for item in balance_sheet_analysis["EquityCapital"]]
Reserves = [item["Value"] for item in balance_sheet_analysis["Reserves"]]
Borrowings = [item["Value"] for item in balance_sheet_analysis["Borrowings"]]
OtherLiabilities = [item["Value"] for item in balance_sheet_analysis["OtherLiabilities"]]
TotalLiabilities = [item["Value"] for item in balance_sheet_analysis["TotalLiabilities"]]
FixedAssets = [item["Value"] for item in balance_sheet_analysis["FixedAssets"]]
CWIP = [item["Value"] for item in balance_sheet_analysis["CWIP"]]
Investments = [item["Value"] for item in balance_sheet_analysis["Investments"]]
OtherAssets = [item["Value"] for item in balance_sheet_analysis["OtherAssets"]]
Inventories = [item["Value"] for item in balance_sheet_analysis["Inventories"]]
TradeReceivables = [item["Value"] for item in balance_sheet_analysis["TradeReceivables"]]
CashEquivalents = [item["Value"] for item in balance_sheet_analysis["CashEquivalents"]]
ShortTermLoans = [item["Value"] for item in balance_sheet_analysis["ShortTermLoans"]]
OtherAssetItems = [item["Value"] for item in balance_sheet_analysis["OtherAssetItems"]]
TotalAssets = [item["Value"] for item in balance_sheet_analysis["TotalAssets"]]

balance_sheet_dict = {
    "years": years,
    "EquityCapital": EquityCapital,
    "Reserves": Reserves,
    "Borrowings": Borrowings,
    "OtherLiabilities": OtherLiabilities,
    "TotalLiabilities": TotalLiabilities,
    "FixedAssets": FixedAssets,
    "CWIP": CWIP,
    "Investments": Investments,
    "OtherAssets": OtherAssets,
    "Inventories": Inventories,
    "TradeReceivables": TradeReceivables,
    "CashEquivalents": CashEquivalents,
    "ShortTermLoans": ShortTermLoans,
    "OtherAssetItems": OtherAssetItems,
    "TotalAssets": TotalAssets
}

balance_sheet_commentary = [escape_latex(comment) for comment in data["balance_sheet_analysis"]["commentary"]]
company_financials_commentary = [escape_latex(comment) for comment in data["company_financials"]["commentary"]]
cash_flow_analysis_commentary = [escape_latex(comment) for comment in data["cash_flow_analysis"]["commentary"]]
# Accessing the fixed assets table from the provided data structure
fixed_assets_data = {}
for category, entries in data['fixed_assets']['table'].items():
    fixed_assets_data[category] = []
    for entry in entries:
        fixed_assets_data[category].append({
            "Year": entry['Year'],
            "Value": entry['Value']
        })
fixed_assets_data = data["fixed_assets"]["table"]

# Extracting data for each asset category
years = [item["Year"] for item in fixed_assets_data["Land"]]
land_values = [item["Value"] for item in fixed_assets_data["Land"]]
building_values = [item["Value"] for item in fixed_assets_data["Building"]]
plant_machinery_values = [item["Value"] for item in fixed_assets_data["PlantMachinery"]]
equipment_values = [item["Value"] for item in fixed_assets_data["Equipments"]]
furniture_fittings_values = [item["Value"] for item in fixed_assets_data["FurnitureNFittings"]]
vehicle_values = [item["Value"] for item in fixed_assets_data["Vehicles"]]
wind_turbine_values = [item["Value"] for item in fixed_assets_data["WindTurbines"]]
intangible_assets_values = [item["Value"] for item in fixed_assets_data["IntangibleAssets"]]
other_fixed_assets_values = [item["Value"] for item in fixed_assets_data["OtherFixedAssets"]]
gross_block_values = [item["Value"] for item in fixed_assets_data["GrossBlock"]]
accumulated_depreciation_values = [item["Value"] for item in fixed_assets_data["AccumulatedDepreciation"]]
cwip_values = [item["Value"] for item in fixed_assets_data["CWIP"]]
investments_values = [item["Value"] for item in fixed_assets_data["Investments"]]
inventories_values = [item["Value"] for item in fixed_assets_data["Inventories"]]
trade_receivables_values = [item["Value"] for item in fixed_assets_data["TradeReceivables"]]
cash_equivalents_values = [item["Value"] for item in fixed_assets_data["CashEquivalents"]]
short_term_loans_values = [item["Value"] for item in fixed_assets_data["ShortTermLoans"]]
other_asset_items_values = [item["Value"] for item in fixed_assets_data["OtherAssetItems"]]
total_assets_values = [item["Value"] for item in fixed_assets_data["TotalAssets"]]

# Combining all data into a single dictionary
fixed_assets_dict = {
    "years": years,
    "land": land_values,
    "building": building_values,
    "plant_machinery": plant_machinery_values,
    "equipment": equipment_values,
    "furniture_fittings": furniture_fittings_values,
    "vehicles": vehicle_values,
    "wind_turbines": wind_turbine_values,
    "intangible_assets": intangible_assets_values,
    "other_fixed_assets": other_fixed_assets_values,
    "gross_block": gross_block_values,
    "accumulated_depreciation": accumulated_depreciation_values,
    "cwip": cwip_values,
    "investments": investments_values,
    "inventories": inventories_values,
    "trade_receivables": trade_receivables_values,
    "cash_equivalents": cash_equivalents_values,
    "short_term_loans": short_term_loans_values,
    "other_asset_items": other_asset_items_values,
    "total_assets": total_assets_values
}

fixed_assets_commentary = [escape_latex(comment) for comment in data["fixed_assets"]["commentary"]]
# Accessing the cash flow analysis table from the provided data structure
cash_flow_data = {}

# Loop over each cash flow category in the table data
for category, entries in data['cash_flow_analysis']['table'].items():
    cash_flow_data[category] = []
    
    # Process each entry in the category
    for entry in entries:
        # Prepare the Year and Value, ensuring Value is converted to string and checking for null values
        formatted_entry = {
            "Year": escape_latex(entry['year']),
            "Value": escape_latex(str(entry['value'])) if entry['value'] is not None else "N/A"
        }
        cash_flow_data[category].append(formatted_entry)

cash_flow_data = data["cash_flow_analysis"]["table"]

# Extracting data for each cash flow component
years = [item["year"] for item in cash_flow_data["profit_from_operations"]]
profit_from_operations = [item["value"] for item in cash_flow_data["profit_from_operations"]]
receivables = [item["value"] for item in cash_flow_data["receivables"]]
inventory = [item["value"] for item in cash_flow_data["inventory"]]
loans_advances = [item["value"] for item in cash_flow_data["Loans_Advances"]]
other_wc_items = [item["value"] for item in cash_flow_data["Other_WC_items"]]
direct_taxes = [item["value"] for item in cash_flow_data["Direct_taxes"]]
fixed_assets_purchased = [item["value"] for item in cash_flow_data["Fixed_assets_purchased"]]
fixed_assets_sold = [item["value"] for item in cash_flow_data["Fixed_assets_sold"]]
investments_purchased = [item["value"] for item in cash_flow_data["Investments_purchased"]]
investments_sold = [item["value"] for item in cash_flow_data["Investments_sold"]]
interest_received = [item["value"] for item in cash_flow_data["Interest_received"]]
invest_in_subsidies = [item["value"] for item in cash_flow_data["Invest_in_subsidiaries"]]
investment_in_group_cos = [item["value"] for item in cash_flow_data["Investment_in_group_cos"]]
other_investing_items = [item["value"] for item in cash_flow_data["Other_investing_items"]]
proceeds_from_shares = [item["value"] for item in cash_flow_data["Proceeds_from_shares"]]
proceeds_from_borrowings = [item["value"] for item in cash_flow_data["Proceeds_from_borrowings"]]
repayment_of_borrowings = [item["value"] for item in cash_flow_data["Repayment_of_borrowings"]]
interest_paid_fin = [item["value"] for item in cash_flow_data["Interest_paid_fin"]]
dividends_paid = [item["value"] for item in cash_flow_data["Dividends_paid"]]
financial_liabilities = [item["value"] for item in cash_flow_data["Financial_liabilities"]]
other_financing_items = [item["value"] for item in cash_flow_data["Other_financing_items"]]

# Combining all data into a single dictionary
cash_flow_analysis_dict = {
    "years": years,
    "profit_from_operations": profit_from_operations,
    "changes_in_receivables": receivables,
    "changes_in_inventory": inventory,
    "changes_in_loans_advances": loans_advances,
    "other_wc_items": other_wc_items,
    "direct_taxes": direct_taxes,
    "fixed_assets_purchased": fixed_assets_purchased,
    "fixed_assets_sold": fixed_assets_sold,
    "investments_purchased": investments_purchased,
    "investments_sold": investments_sold,
    "interest_received": interest_received,
    "invest_in_subsidies": invest_in_subsidies,
    "investment_in_group_cos": investment_in_group_cos,
    "other_investing_items": other_investing_items,
    "proceeds_from_shares": proceeds_from_shares,
    "proceeds_from_borrowings": proceeds_from_borrowings,
    "repayment_of_borrowings": repayment_of_borrowings,
    "interest_paid_fin": interest_paid_fin,
    "dividends_paid": dividends_paid,
    "financial_liabilities": financial_liabilities,
    "other_financing_items": other_financing_items
}
cash_flow_analysis_commentary = [escape_latex(comment) for comment in data["cash_flow_analysis"]["commentary"]]
# Setup Jinja2 environment and load template file
leverage_ratio_data = data["leverage_ratio"]
#leverage_ratio_graphs = [{"name": key, "url": value["url"]} for key, value in leverage_ratio_data["graphs"].items()]
leverage_ratio_commentary = [escape_latex(comment) for comment in leverage_ratio_data["commentary"]]
leverage_ratio_graphs = [{"name": key, "url": value} for key, value in leverage_ratio_data["graphs"].items()]
#leverage_ratio_commentary = leverage_ratio_data.commentary

# Extracting performance ratios data
performance_ratios_data = data["performance_ratios"]
#performance_ratio_graphs = [{"name": key, "url": value["url"]} for key, value in performance_ratios_data["graphs"].items()]
performance_ratio_commentary = [escape_latex(comment) for comment in performance_ratios_data["commentary"]]
performance_ratio_graphs = [{"name": key, "url": value} for key, value in performance_ratios_data["graphs"].items()]
#performance_ratio_commentary = leverage_ratio_data.commentary
# Extracting activity ratios data
activity_ratios_data = data["activity_ratio"]
#activity_ratio_graphs = [{"name": key, "url": value["url"]} for key, value in activity_ratios_data["graphs"].items()]
activity_ratio_commentary = [escape_latex(comment) for comment in activity_ratios_data["commentary"]]
activity_ratio_graphs = [{"name": key, "url": value} for key, value in activity_ratios_data["graphs"].items()]
#activity_ratio_commentary = activity_ratios_data.commentary
# Extracting valuation ratios data
# valuation_ratios_data = data["valuation_ratios"]
# valuation_ratio_graphs = [{"name": key, "url": value["url"]} for key, value in valuation_ratios_data["graphs"].items()]
# valuation_ratio_commentary = [escape_latex(comment) for comment in valuation_ratios_data["commentary"]]
working_capital_movement_data = data["working_capital_movement"]
working_capital_movement_commentary = [escape_latex(comment) for comment in working_capital_movement_data["commentary"]]
working_capital_movement_graphs = [{"name": key, "url": value["url"]} for key, value in working_capital_movement_data["graphs"].items()]
# Setup Jinja2 environment and load template file
ownership_structure_data = data["ownership_structure"]
ownership_structure_graphs = [{"name": key, "url": value["url"]} for key, value in ownership_structure_data["graphs"].items()]
ownership_structure_commentary = [escape_latex(comment) for comment in ownership_structure_data["commentary"]]

# Setup Jinja2 environment and load template file
subsidiary_jv_info_data = {
    "subsidiary": [],
    "JV_information": [escape_latex(jv) for jv in data["subsidiary_jv_info"]["JV_information"]]
}

subsidiaries = data["subsidiary_jv_info"]["subsidiary"]
for subsidiary in subsidiaries:
    date_of_creation_key = "Date_of_Creation" if "Date_of_Creation" in subsidiary else "Date of Creation"
    
    subsidiary_info = {
        "subsidiary_name": escape_latex(subsidiary["subsidiary_name"]),
        date_of_creation_key: escape_latex(subsidiary[date_of_creation_key]),
        "Interest": escape_latex(subsidiary["Interest"]),
        "Location": escape_latex(subsidiary["Location"])
    }
    subsidiary_jv_info_data["subsidiary"].append(subsidiary_info)


# Setup Jinja2 environment and load template file
cash_flow_data = {
    "commentary": [escape_latex(comment) for comment in data["cash_flow_analysis"]["commentary"]],
    "graph": {
        "url": escape_latex(data["cash_flow_analysis"]["graph"]["url"])
    },
    "graph_commentary": [escape_latex(comment) for comment in data["cash_flow_analysis"]["graph_commentary"]]
}

table = data["cash_flow_analysis"]["table"]
cash_flow_data["table"] = {}

for category, details in table.items():
    years = [item["year"] for item in details]
    values = [item["value"] for item in details]
    cash_flow_data["table"][category] = {
        "Years": years,
        "Values": values
    }
financial_analysis_data = {
    "Profitability": {},
    "commentary": [escape_latex(comment) for comment in data["financial_analysis"]["commentary"]]
}

# profitability = data["financial_analysis"]["Profitability"]
# for metric, details in profitability.items():
#     years = [item["year"] for item in details]
#     values = [item["value"] for item in details]
#     financial_analysis_data["Profitability"][metric] = {
#         "Years": years,
#         "Values": values
#     }

print(financial_analysis_data)

# Setup Jinja2 environment and load template file
env = Environment(loader=FileSystemLoader('.'))
env.filters['escape_latex'] = escape_latex
template = env.get_template(latex_template_path)

# Render the template with the combined data
rendered_str = template.render(
    concalls = concalls,
    recent_news=recent_news,
    company_profile=formatted_profile,
    promoters_dict=promoters_dict,
    key_issues=key_issues_list,
    key_strengths=key_strengths_list,
    industry_risks=industry_risks_list,
    brief_financials=financial_data,
    financial_dict=financial_dict,
    financial_commentary=financial_commentary,
    balance_sheet_dict=balance_sheet_dict,
    balance_sheet_commentary=balance_sheet_commentary,
    leverage_ratio_graphs=leverage_ratio_graphs,

    fixed_assets_data = fixed_assets_data,
    fixed_assets_commentary = fixed_assets_commentary,
    fixed_assets_dict = fixed_assets_dict,
    company_financials = company_financials,
    company_financials_dict = company_financials_dict,
    company_financials_commentary = company_financials_commentary,
    debt_data=debt_schedule_data ,
    debt_data_dict = debt_data_dict,
    debt_schedule_commentary = debt_schedule_commentary,
    cash_flow_data = cash_flow_data,
    cash_flow_analysis_dict = cash_flow_analysis_dict,
    cash_flow_analysis_commentary  = cash_flow_analysis_commentary ,
    justification_of_proposal = justification_of_proposal_list,
    Recommendation =  Recommendation_list,

    leverage_ratio_commentary=leverage_ratio_commentary,
    performance_ratio_graphs=performance_ratio_graphs,
    performance_ratio_commentary=performance_ratio_commentary,
    activity_ratio_graphs=activity_ratio_graphs,
    activity_ratio_commentary=activity_ratio_commentary,
    ownership_structure_graphs=ownership_structure_graphs,
    ownership_structure_commentary=ownership_structure_commentary,
    peer_ratings=peer_ratings_list,
    peer_commentary=peer_ratings_commentary,
   
    working_capital_graphs=working_capital_movement_graphs,
    working_capital_movement_commentary = working_capital_movement_commentary ,
    subsidiary_jv_info_data=subsidiary_jv_info_data,
    financial_analysis_data=financial_analysis_data
)

# Write the rendered template to the output file
with open(output_file_path, "w") as f:
    f.write(rendered_str)

print("Credit Appraisal LaTeX file has been generated and saved as credit_appraisal_output.tex")
print(rendered_str)