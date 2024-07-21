import sqlite3
import requests
import csv
import os

# Create database connection and cursor
conn = sqlite3.connect('stocks_data.db')
cursor = conn.cursor()

# Create tables based on the fields in APICatalogue.txt

cursor.execute('''
CREATE TABLE IF NOT EXISTS financial_statement_symbol_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT
)
''')


# Indicators Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    TDV_Volume REAL,
    relative_volume REAL,
    pvi_nvi REAL,
    nvi_pvi REAL,
    volume_divergence REAL,
    volume_momentum REAL,
    last_volume_momentum REAL,
    fv_per_share REAL,
    lv_per_share REAL,
    nv_per_share REAL,
    nv_eps_share REAL,
    nv_eps_growth_share REAL,
    ev_per_share REAL,
    graham_number REAL,
    revenue_growth_dif REAL,
    ohlson_o REAL,
    liab_assets REAL
)
''')

# Create other tables manually based on the APICatalogue.txt fields
cursor.execute('''
CREATE TABLE IF NOT EXISTS sectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS industries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    industry TEXT
)
''')

# Historical Metrics Tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS ipo_calendar_confirmed (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    cik TEXT,
    form TEXT,
    filingDate TEXT,
    acceptedDate TEXT,
    effectivenessDate TEXT,
    url TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS symbol_change (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    name TEXT,
    oldSymbol TEXT,
    newSymbol TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS delisted_companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    companyName TEXT,
    exchange TEXT,
    ipoDate TEXT,
    delistedDate TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS social_sentiments_change (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    name TEXT,
    rank INTEGER,
    sentiment REAL,
    sentimentChange REAL,
    type TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS social_sentiments_trending (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    name TEXT,
    rank INTEGER,
    sentiment REAL,
    lastSentiment REAL,
    type TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS historical_shares_float (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date TEXT,
    freeFloat REAL,
    floatShares INTEGER,
    outstandingShares INTEGER,
    source TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS historical_employee_count (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    cik TEXT,
    acceptanceTime TEXT,
    periodOfReport TEXT,
    companyName TEXT,
    formType TEXT,
    filingDate TEXT,
    employeeCount INTEGER,
    source TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS analyst_stock_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date TEXT,
    analystRatingsBuy INTEGER,
    analystRatingsHold INTEGER,
    analystRatingsSell INTEGER,
    analystRatingsStrongSell INTEGER,
    analystRatingsStrongBuy INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS analyst_estimates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date TEXT,
    estimatedRevenueLow REAL,
    estimatedRevenueHigh REAL,
    estimatedRevenueAvg REAL,
    estimatedEbitdaLow REAL,
    estimatedEbitdaHigh REAL,
    estimatedEbitdaAvg REAL,
    estimatedEbitLow REAL,
    estimatedEbitHigh REAL,
    estimatedEbitAvg REAL,
    estimatedNetIncomeLow REAL,
    estimatedNetIncomeHigh REAL,
    estimatedNetIncomeAvg REAL,
    estimatedSgaExpenseLow REAL,
    estimatedSgaExpenseHigh REAL,
    estimatedSgaExpenseAvg REAL,
    estimatedEpsAvg REAL,
    estimatedEpsHigh REAL,
    estimatedEpsLow REAL,
    numberAnalystEstimatedRevenue INTEGER,
    numberAnalystsEstimatedEps INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS upgrades_downgrades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    publishedDate TEXT,
    newsURL TEXT,
    newsTitle TEXT,
    newsBaseURL TEXT,
    newsPublisher TEXT,
    newGrade TEXT,
    previousGrade TEXT,
    gradingCompany TEXT,
    action TEXT,
    priceWhenPosted REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS grade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date TEXT,
    gradingCompany TEXT,
    previousGrade TEXT,
    newGrade TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS price_target (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    publishedDate TEXT,
    newsURL TEXT,
    newsTitle TEXT,
    analystName TEXT,
    priceTarget REAL,
    adjPriceTarget REAL,
    priceWhenPosted REAL,
    newsPublisher TEXT,
    newsBaseURL TEXT,
    analystCompany TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    publishedDate TEXT,
    title TEXT,
    image TEXT,
    site TEXT,
    text TEXT,
    url TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS historical_rating (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date TEXT,
    rating TEXT,
    ratingScore INTEGER,
    ratingRecommendation TEXT,
    ratingDetailsDCFScore INTEGER,
    ratingDetailsDCFRecommendation TEXT,
    ratingDetailsROEScore INTEGER,
    ratingDetailsROERecommendation TEXT,
    ratingDetailsROAScore INTEGER,
    ratingDetailsROARecommendation TEXT,
    ratingDetailsDEScore INTEGER,
    ratingDetailsDERecommendation TEXT,
    ratingDetailsPEScore INTEGER,
    ratingDetailsPERecommendation TEXT,
    ratingDetailsPBScore INTEGER,
    ratingDetailsPBRecommendation TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS historical_social_sentiment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    symbol TEXT,
    stocktwitsPosts INTEGER,
    twitterPosts INTEGER,
    stocktwitsComments INTEGER,
    twitterComments INTEGER,
    stocktwitsLikes INTEGER,
    twitterLikes INTEGER,
    stocktwitsImpressions INTEGER,
    twitterImpressions INTEGER,
    stocktwitsSentiment REAL,
    twitterSentiment REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS senate_trading (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT,
    lastName TEXT,
    office TEXT,
    link TEXT,
    dateRecieved TEXT,
    transactionDate TEXT,
    owner TEXT,
    assetDescription TEXT,
    assetType TEXT,
    type TEXT,
    amount TEXT,
    comment TEXT,
    symbol TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS senate_disclosure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disclosureYear TEXT,
    disclosureDate TEXT,
    transactionDate TEXT,
    owner TEXT,
    ticker TEXT,
    assetDescription TEXT,
    type TEXT,
    amount TEXT,
    representative TEXT,
    district TEXT,
    link TEXT,
    capitalGainsOver200USD TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS commitment_of_traders_report_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date TEXT,
    sector TEXT,
    currentLongMarketSituation REAL,
    currentShortMarketSituation REAL,
    marketSituation TEXT,
    previousLongMarketSituation REAL,
    previousShortMarketSituation REAL,
    previousMarketSituation TEXT,
    netPostion INTEGER,
    previousNetPosition INTEGER,
    changeInNetPosition INTEGER,
    marketSentiment TEXT,
    reversalTrend TEXT,
    name TEXT,
    exchange TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS balance_sheet_statement_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    symbol TEXT,
    reportedCurrency TEXT,
    cik TEXT,
    fillingDate TEXT,
    acceptedDate TEXT,
    calendarYear TEXT,
    period TEXT,
    cashAndCashEquivalents REAL,
    shortTermInvestments REAL,
    cashAndShortTermInvestments REAL,
    netReceivables REAL,
    inventory REAL,
    otherCurrentAssets REAL,
    totalCurrentAssets REAL,
    propertyPlantEquipmentNet REAL,
    goodwill REAL,
    intangibleAssets REAL,
    goodwillAndIntangibleAssets REAL,
    longTermInvestments REAL,
    taxAssets REAL,
    otherNonCurrentAssets REAL,
    totalNonCurrentAssets REAL,
    otherAssets REAL,
    totalAssets REAL,
    accountPayables REAL,
    shortTermDebt REAL,
    taxPayables REAL,
    deferredRevenue REAL,
    otherCurrentLiabilities REAL,
    totalCurrentLiabilities REAL,
    longTermDebt REAL,
    deferredRevenueNonCurrent REAL,
    deferredTaxLiabilitiesNonCurrent REAL,
    otherNonCurrentLiabilities REAL,
    totalNonCurrentLiabilities REAL,
    otherLiabilities REAL,
    capitalLeaseObligations REAL,
    totalLiabilities REAL,
    preferredStock REAL,
    commonStock REAL,
    retainedEarnings REAL,
    accumulatedOtherComprehensiveIncomeLoss REAL,
    othertotalStockholdersEquity REAL,
    totalStockholdersEquity REAL,
    totalLiabilitiesAndStockholdersEquity REAL,
    minorityInterest REAL,
    totalEquity REAL,
    totalLiabilitiesAndTotalEquity REAL,
    totalInvestments TEXT,
    totalDebt TEXT,
    netDebt TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS cash_flow_statement_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    symbol TEXT,
    reportedCurrency TEXT,
    cik TEXT,
    fillingDate TEXT,
    acceptedDate TEXT,
    calendarYear TEXT,
    period TEXT,
    netIncome REAL,
    depreciationAndAmortization REAL,
    deferredIncomeTax REAL,
    stockBasedCompensation REAL,
    changeInWorkingCapital REAL,
    accountsReceivables REAL,
    inventory REAL,
    accountsPayables REAL,
    otherWorkingCapital REAL,
    otherNonCashItems REAL,
    netCashProvidedByOperatingActivities REAL,
    investmentsInPropertyPlantAndEquipment REAL,
    acquisitionsNet REAL,
    purchasesOfInvestments REAL,
    salesMaturitiesOfInvestments REAL,
    otherInvestingActivites REAL,
    netCashUsedForInvestingActivites REAL,
    debtRepayment REAL,
    commonStockIssued REAL,
    commonStockRepurchased REAL,
    dividendsPaid REAL,
    otherFinancingActivites REAL,
    netCashUsedProvidedByFinancingActivities REAL,
    effectOfForexChangesOnCash REAL,
    netChangeInCash REAL,
    cashAtEndOfPeriod REAL,
    cashAtBeginningOfPeriod REAL,
    operatingCashFlow REAL,
    capitalExpenditure REAL,
    freeCashFlow REAL,
    link TEXT,
    finalLink TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dcf_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    symbol TEXT,
    fillingDate TEXT,
    acceptedDate TEXT,
    calendarYear TEXT,
    period TEXT,
    dcf REAL,
    stockPrice REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS earnings_surprises_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    symbol TEXT,
    estimatedEPS REAL,
    actualEPS REAL,
    surprisePercentage REAL,
    surpriseAmount REAL,
    estimateTrend REAL,
    numberOfEstimates INTEGER,
    EPSYearAgo REAL,
    EPSNextYear REAL,
    EPSThisYear REAL
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS etf_holder_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    sharesNumber INTEGER,
    asset TEXT,
    weightPercentage REAL,
    cusip TEXT,
    isin TEXT,
    name TEXT,
    marketValue REAL,
    updated TEXT 
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS financial_growth_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date TEXT,
    period TEXT,
    revenueGrowth REAL,
    grossProfitGrowth REAL,
    EBITGrowth REAL,
    operatingIncomeGrowth REAL,
    netIncomeGrowth REAL,
    EPSGrowth REAL,
    EPSDilutedGrowth REAL,
    weightedAverageSharesGrowth REAL,
    weightedAverageSharesDilutedGrowth REAL,
    dividendsperShareGrowth REAL,
    operatingCashFlowGrowth REAL,
    freeCashFlowGrowth REAL,
    tenYRevenueGrowthPerShare REAL,
    fiveYRevenueGrowthPerShare REAL,
    threeYRevenueGrowthPerShare REAL,
    tenYOperatingCFGrowthPerShare REAL,
    fiveYOperatingCFGrowthPerShare REAL,
    threeYOperatingCFGrowthPerShare REAL,
    tenYNetIncomeGrowthPerShare REAL,
    fiveYNetIncomeGrowthPerShare REAL,
    threeYNetIncomeGrowthPerShare REAL,
    tenYShareholdersEquityGrowthPerShare REAL,
    fiveYShareholdersEquityGrowthPerShare REAL,
    threeYShareholdersEquityGrowthPerShare REAL,
    tenYDividendperShareGrowthPerShare REAL,
    fiveYDividendperShareGrowthPerShare REAL,
    threeYDividendperShareGrowthPerShare REAL,
    receivablesGrowth REAL,
    inventoryGrowth REAL,
    assetGrowth REAL,
    bookValueperShareGrowth REAL,
    debtGrowth REAL,
    RDExpenseGrowth REAL,
    SGAExpensesGrowth REAL,
    calendarYear INTEGER
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS income_statement_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    symbol TEXT,
    reportedCurrency TEXT,
    cik TEXT,
    fillingDate TEXT,
    acceptedDate TEXT,
    calendarYear INTEGER,
    period TEXT,
    revenue REAL,
    costOfRevenue REAL,
    grossProfit REAL,
    grossProfitRatio REAL,
    ResearchAndDevelopmentExpenses REAL,
    GeneralAndAdministrativeExpenses REAL,
    SellingAndMarketingExpenses REAL,
    SellingGeneralAndAdministrativeExpenses REAL,
    otherExpenses REAL,
    operatingExpenses REAL,
    costAndExpenses REAL,
    interestExpense REAL,
    depreciationAndAmortization REAL,
    EBITDA REAL,
    EBITDARatio REAL,
    operatingIncome REAL,
    operatingIncomeRatio REAL,
    totalOtherIncomeExpensesNet REAL,
    incomeBeforeTax REAL,
    incomeBeforeTaxRatio REAL,
    incomeTaxExpense REAL,
    netIncome REAL,
    netIncomeRatio REAL,
    EPS REAL,
    EPSDiluted REAL,
    weightedAverageShsOut REAL,
    weightedAverageShsOutDil REAL,
    link TEXT,
    finalLink TEXT,
    interestIncome REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS key_metrics_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date TEXT,
    period TEXT,
    revenuePerShare REAL,
    netIncomePerShare REAL,
    operatingCashFlowPerShare REAL,
    freeCashFlowPerShare REAL,
    cashPerShare REAL,
    bookValuePerShare REAL,
    tangibleBookValuePerShare REAL,
    shareholdersEquityPerShare REAL,
    interestDebtPerShare REAL,
    marketCap REAL,
    enterpriseValue REAL,
    peRatio REAL,
    priceToSalesRatio REAL,
    pocfratio REAL,
    pfcfRatio REAL,
    pbRatio REAL,
    ptbRatio REAL,
    evToSales REAL,
    enterpriseValueOverEBITDA REAL,
    evToOperatingCashFlow REAL,
    earningsYield REAL,
    freeCashFlowYield REAL,
    debtToEquity REAL,
    debtToAssets REAL,
    netDebtToEBITDA REAL,
    currentRatio REAL,
    interestCoverage REAL,
    incomeQuality REAL,
    dividendYield REAL,
    payoutRatio REAL,
    salesGeneralAndAdministrativeToRevenue REAL,
    researchAndDdevelopementToRevenue REAL,
    intangiblesToTotalAssets REAL,
    capexToOperatingCashFlow REAL,
    capexToRevenue REAL,
    capexToDepreciation REAL,
    stockBasedCompensationToRevenue REAL,
    grahamNumber REAL,
    roic REAL,
    returnOnTangibleAssets REAL,
    grahamNetNet REAL,
    workingCapital REAL,
    tangibleAssetValue REAL,
    netCurrentAssetValue REAL,
    investedCapital REAL,
    averageReceivables REAL,
    averagePayables REAL,
    averageInventory REAL,
    daysSalesOutstanding REAL,
    daysPayablesOutstanding REAL,
    daysOfInventoryOnHand REAL,
    receivablesTurnover REAL,
    payablesTurnover REAL,
    inventoryTurnover REAL,
    roe REAL,
    capexPerShare REAL,
    calendarYear INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS price_target_summary_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    lastMonth TEXT,
    lastMonthAvgPT REAL,
    lastMonthAvgPTPercentDif REAL,
    lastQuarter TEXT,
    lastQuarterAvgPT REAL,
    lastQuarterAvgPTPercentDif REAL,
    lastYear TEXT,
    lastYearAvgPT REAL,
    lastYearAvgPTPercentDif REAL,
    allTime TEXT,
    allTimeAvgPT REAL,
    allTimeAvgPTPercentDif REAL,
    publishers TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS profile_all (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Symbol TEXT,
    Price REAL,
    Beta REAL,
    VolAvg REAL,
    MktCap REAL,
    LastDiv REAL,
    Range TEXT,
    Changes REAL,
    companyName TEXT,
    currency TEXT,
    cik TEXT,
    isin TEXT,
    cusip TEXT,
    exchange TEXT,
    exchangeShortName TEXT,
    industry TEXT,
    website TEXT,
    description TEXT,
    CEO TEXT,
    sector TEXT,
    country TEXT,
    fullTimeEmployees INTEGER,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    DCF_diff REAL,
    DCF REAL,
    image TEXT,
    ipoDate TEXT,
    defaultImage BOOLEAN,
    isEtf BOOLEAN,
    isActivelyTrading BOOLEAN,
    isFund BOOLEAN,
    isAdr BOOLEAN
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS rating_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date TEXT,
    rating TEXT,
    ratingScore INTEGER,
    ratingRecommendation TEXT,
    ratingDetailsDCFScore INTEGER,
    ratingDetailsDCFRecommendation TEXT,
    ratingDetailsROEScore INTEGER,
    ratingDetailsROERecommendation TEXT,
    ratingDetailsROAScore INTEGER,
    ratingDetailsROARecommendation TEXT,
    ratingDetailsDEScore INTEGER,
    ratingDetailsDERecommendation TEXT,
    ratingDetailsPEScore INTEGER,
    ratingDetailsPERecommendation TEXT,
    ratingDetailsPBScore INTEGER,
    ratingDetailsPBRecommendation TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ratios_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    date TEXT,
    period TEXT,
    currentRatio REAL,
    quickRatio REAL,
    cashRatio REAL,
    daysOfSalesOutstanding REAL,
    daysOfInventoryOutstanding REAL,
    operatingCycle REAL,
    daysOfPayablesOutstanding REAL,
    cashConversionCycle REAL,
    grossProfitMargin REAL,
    operatingProfitMargin REAL,
    pretaxProfitMargin REAL,
    netProfitMargin REAL,
    effectiveTaxRate REAL,
    returnOnAssets REAL,
    returnOnEquity REAL,
    returnOnCapitalEmployed REAL,
    netIncomePerEBT REAL,
    ebtPerEbit REAL,
    ebitPerRevenue REAL,
    debtRatio REAL,
    debtEquityRatio REAL,
    longTermDebtToCapitalization REAL,
    totalDebtToCapitalization REAL,
    interestCoverage REAL,
    cashFlowToDebtRatio REAL,
    companyEquityMultiplier REAL,
    receivablesTurnover REAL,
    payablesTurnover REAL,
    inventoryTurnover REAL,
    fixedAssetTurnover REAL,
    assetTurnover REAL,
    operatingCashFlowPerShare REAL,
    freeCashFlowPerShare REAL,
    cashPerShare REAL,
    payoutRatio REAL,
    operatingCashFlowSalesRatio REAL,
    freeCashFlowOperatingCashFlowRatio REAL,
    cashFlowCoverageRatios REAL,
    shortTermCoverageRatios REAL,
    capitalExpenditureCoverageRatio REAL,
    dividendPaidAndCapexCoverageRatio REAL,
    dividendPayoutRatio REAL,
    priceBookValueRatio REAL,
    priceToBookRatio REAL,
    priceToSalesRatio REAL,
    priceEarningsRatio REAL,
    priceToFreeCashFlowsRatio REAL,
    priceToOperatingCashFlowsRatio REAL,
    priceCashFlowRatio REAL,
    priceEarningsToGrowthRatio REAL,
    priceSalesRatio REAL,
    dividendYield REAL,
    enterpriseValueMultiple REAL,
    priceFairValue REAL,
    calendarYear INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ratios_ttm_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    dividendYielTTM REAL,
    dividendYielPercentageTTM REAL,
    peRatioTTM REAL,
    pegRatioTTM REAL,
    payoutRatioTTM REAL,
    currentRatioTTM REAL,
    quickRatioTTM REAL,
    cashRatioTTM REAL,
    daysOfSalesOutstandingTTM REAL,
    daysOfInventoryOutstandingTTM REAL,
    operatingCycleTTM REAL,
    daysOfPayablesOutstandingTTM REAL,
    cashConversionCycleTTM REAL,
    grossProfitMarginTTM REAL,
    operatingProfitMarginTTM REAL,
    pretaxProfitMarginTTM REAL,
    netProfitMarginTTM REAL,
    effectiveTaxRateTTM REAL,
    returnOnAssetsTTM REAL,
    returnOnEquityTTM REAL,
    returnOnCapitalEmployedTTM REAL,
    netIncomePerEBTTTM REAL,
    ebtPerEbitTTM REAL,
    ebitPerRevenueTTM REAL,
    debtRatioTTM REAL,
    debtEquityRatioTTM REAL,
    longTermDebtToCapitalizationTTM REAL,
    totalDebtToCapitalizationTTM REAL,
    interestCoverageTTM REAL,
    cashFlowToDebtRatioTTM REAL,
    companyEquityMultiplierTTM REAL,
    receivablesTurnoverTTM REAL,
    payablesTurnoverTTM REAL,
    inventoryTurnoverTTM REAL,
    fixedAssetTurnoverTTM REAL,
    assetTurnoverTTM REAL,
    operatingCashFlowPerShareTTM REAL,
    freeCashFlowPerShareTTM REAL,
    cashPerShareTTM REAL,
    operatingCashFlowSalesRatioTTM REAL,
    freeCashFlowOperatingCashFlowRatioTTM REAL,
    cashFlowCoverageRatiosTTM REAL,
    shortTermCoverageRatiosTTM REAL,
    capitalExpenditureCoverageRatioTTM REAL,
    dividendPaidAndCapexCoverageRatioTTM REAL,
    priceBookValueRatioTTM REAL,
    priceToBookRatioTTM REAL,
    priceToSalesRatioTTM REAL,
    priceEarningsRatioTTM REAL,
    priceToFreeCashFlowsRatioTTM REAL,
    priceToOperatingCashFlowsRatioTTM REAL,
    priceCashFlowRatioTTM REAL,
    priceEarningsToGrowthRatioTTM REAL,
    priceSalesRatioTTM REAL,
    dividendYieldTTM REAL,
    enterpriseValueMultipleTTM REAL,
    priceFairValueTTM REAL,
    dividendPerShareTTM REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS scores_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    altmanZScore REAL,
    piotroskiScore INTEGER,
    workingCapital REAL,
    totalAssets REAL,
    retainedEarnings REAL,
    ebit REAL,
    marketCap REAL,
    totalLiabilities REAL,
    revenue REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_peers_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    peers TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS upgrades_downgrades_consensus_bulk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT,
    strongBuy INTEGER,
    buy INTEGER,
    hold INTEGER,
    sell INTEGER,
    strongSell INTEGER,
    consensus TEXT
)
''')


# Close the database connection
conn.close()
