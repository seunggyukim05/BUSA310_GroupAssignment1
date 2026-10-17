import csv
import json
from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
SETTINGS_PATH = BASE_DIR / "app_assets" / "settings.json"

with open(SETTINGS_PATH, encoding="utf-8") as file:
    settings = json.load(file)

st.set_page_config(
    page_title="Chicago Home Estimator",
    page_icon="🏠",
    layout="wide",
)

st.markdown("""
<style>
    .block-container {
        max-width: 1120px;
        padding-top: 3.5rem;
        padding-bottom: 3rem;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Remember which screen the visitor is viewing.
if "page" not in st.session_state:
    st.session_state.page = "home"


# Home screen
if st.session_state.page == "home":
    st.markdown(
        '<div style="background:linear-gradient(120deg,#0F172A,#164E63);'
        'padding:40px 32px;border-radius:22px;margin-bottom:24px;">'
        '<div style="color:#5EEAD4;font-size:12px;font-weight:700;'
        'letter-spacing:2px;">CHICAGO HOME ESTIMATOR</div>'
        '<h1 style="color:white;font-size:clamp(32px,5vw,52px);'
        'line-height:1.15;margin:16px 0;padding:0;">'
        'A clearer view of your next home.</h1>'
        '<p style="color:#CBD5E1;font-size:18px;margin:0;">'
        'Explore property details, comparable sales, '
        'and the Chicago housing market.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "For homebuyers and real estate professionals "
        "exploring Chicago single-family homes."
    )

    first, second, third = st.columns(3)

    with first:
        if st.button("Enter Property Details →", type="primary"):
            st.session_state.page = "details"
            st.rerun()

    with second:
        if st.button("Explore the Market"):
            st.session_state.page = "market"
            st.rerun()

    with third:
        if st.button("Data & Accuracy"):
            st.session_state.page = "data"
            st.rerun()

    st.caption(
        "Preview version · Price prediction is awaiting "
        "the team's final model."
    )

    st.divider()
    st.subheader("From property details to market context")
    st.write("Start with the home. Then explore the evidence.")

    first, second, third = st.columns(3)

    with first:
        with st.container(border=True):
            st.caption("01 · DESCRIBE")
            st.subheader("Your property")
            st.write(
                "Choose the location and enter building area, "
                "rooms, bathrooms, and construction year."
            )

    with second:
        with st.container(border=True):
            st.caption("02 · REVIEW")
            st.subheader("Your summary")
            st.write(
                "Review your property details and download "
                "a copy for your records."
            )

    with third:
        with st.container(border=True):
            st.caption("03 · EXPLORE")
            st.subheader("The market")
            st.write(
                "Compare past recorded sales and explore "
                "price trends and transaction activity."
            )

    st.divider()
    st.caption(
        "Chicago single-family homes · "
        "Recorded sales: September 2019–August 2026 · "
        "Building area uses exterior measurements."
    )

# Property details screen
elif st.session_state.page == "details":
    saved = st.session_state.get("property_details", {})

    st.markdown("""
    <style>
        .block-container {
            max-width: 1120px;
        }
        .property-hero {
            background: linear-gradient(120deg, #0F172A, #164E63);
            padding: 32px;
            border-radius: 22px;
            margin: 12px 0 24px;
        }
        .property-hero .eyebrow {
            color: #5EEAD4;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
        }
        .property-hero h1 {
            color: white;
            font-size: clamp(28px, 4vw, 42px);
            margin: 8px 0;
            padding: 0;
        }
        .property-hero p {
            color: #CBD5E1;
            margin: 0;
        }
    </style>

    <div class="property-hero">
        <div class="eyebrow">CHICAGO HOME ESTIMATOR</div>
        <h1>Tell us about your home.</h1>
        <p>A few property details. A clearer starting point.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.caption("STEP 1 OF 2  ·  PROPERTY DETAILS → REVIEW")
    st.write("")

    with st.container(border=True):
        st.subheader("01 · Location")
        st.caption(
            "Choose a ZIP, then select the property's actual "
            "Assessor neighborhood code."
        )

        zip_options = settings["zip_options"]
        saved_zip = saved.get("ZIP Code")
        zip_index = (
            zip_options.index(saved_zip)
            if saved_zip in zip_options
            else 0
        )

        left, right = st.columns(2)

        with left:
            zip_code = st.selectbox(
                "ZIP Code",
                options=zip_options,
                index=zip_index,
            )

        neighborhood_options = settings["zip_neighborhoods"][zip_code]
        saved_neighborhood = saved.get("Neighborhood Code")
        neighborhood_index = (
            neighborhood_options.index(saved_neighborhood)
            if saved_neighborhood in neighborhood_options
            else 0
        )

        with right:
            neighborhood = st.selectbox(
                "Assessor Neighborhood Code",
                options=neighborhood_options,
                index=neighborhood_index,
                help=(
                    "These codes are separate from ZIP codes. "
                    "The choices show combinations present in our data."
                ),
            )

    with st.form("property_details_form"):
        st.subheader("02 · Building Details")
        st.caption("Property type: Single-family home")

        area_col, land_col, year_col = st.columns(3)

        with area_col:
            building_area = st.number_input(
                "Building Area (sq ft)",
                min_value=100,
                max_value=30000,
                value=saved.get("Building Area (sq ft)", 1400),
                step=50,
                help="Exterior building measurements, not interior living area.",
            )

        with land_col:
            land_area = st.number_input(
                "Land Area (sq ft)",
                min_value=100,
                max_value=1000000,
                value=saved.get("Land Area (sq ft)", 3750),
                step=50,
            )

        with year_col:
            year_built = st.number_input(
                "Year Built",
                min_value=1600,
                max_value=2026,
                value=saved.get("Year Built", 1950),
                step=1,
            )

        st.divider()
        st.subheader("03 · Rooms & Bathrooms")
        st.caption("Enter full and half bathrooms separately.")

        bed_col, full_col, half_col = st.columns(3)

        with bed_col:
            bedrooms = st.number_input(
                "Bedrooms",
                min_value=0,
                max_value=20,
                value=saved.get("Bedrooms", 3),
                step=1,
            )

        with full_col:
            full_bathrooms = st.number_input(
                "Full Bathrooms",
                min_value=0,
                max_value=15,
                value=saved.get("Full Bathrooms", 1),
                step=1,
                help="Includes a toilet, sink, and bathtub or shower.",
            )

        with half_col:
            half_bathrooms = st.number_input(
                "Half Bathrooms",
                min_value=0,
                max_value=15,
                value=saved.get("Half Bathrooms", 1),
                step=1,
                help="Includes a toilet and sink, without a bathtub or shower.",
            )

        st.divider()

        submitted = st.form_submit_button(
            "Review Property →",
            type="primary",
        )

        st.caption(
            "Review your details next. "
            "Price prediction is awaiting the team's final model."
        )

    if submitted:
        valid_zip = (
            len(zip_code) == 5
            and zip_code.isascii()
            and zip_code.isdigit()
        )
        valid_neighborhood = (
            len(neighborhood) == 5
            and neighborhood.isascii()
            and neighborhood.isdigit()
        )

        if not valid_zip:
            st.error("Select a valid five-digit ZIP code.")

        elif not valid_neighborhood:
            st.error("Select a valid five-digit neighborhood code.")

        else:
            st.session_state.property_details = {
                "ZIP Code": zip_code,
                "Neighborhood Code": neighborhood,
                "Property Type": "Single-family home",
                "Building Area (sq ft)": building_area,
                "Land Area (sq ft)": land_area,
                "Bedrooms": bedrooms,
                "Full Bathrooms": full_bathrooms,
                "Half Bathrooms": half_bathrooms,
                "Year Built": year_built,
            }

            st.session_state.page = "review"
            st.rerun()

# Review screen
elif st.session_state.page == "review":
    details = st.session_state.property_details

    st.caption("STEP 2 OF 2 · REVIEW")
    st.title("Your home, at a glance.")
    st.write(
        "Check your property details and explore similar recorded sales."
    )

    with st.container(border=True):
        st.caption("LOCATION")
        st.subheader(f"Chicago · ZIP {details['ZIP Code']}")
        st.caption(
            f"Assessor Neighborhood: {details['Neighborhood Code']} "
            f"  ·  {details['Property Type']}"
        )

        st.divider()

        first, second, third = st.columns(3)

        with first:
            st.metric(
                "Building Area",
                f"{details['Building Area (sq ft)']:,} sq ft",
            )

        with second:
            st.metric(
                "Land Area",
                f"{details['Land Area (sq ft)']:,} sq ft",
            )

        with third:
            st.metric("Year Built", str(details["Year Built"]))

        st.divider()

        first, second, third = st.columns(3)

        with first:
            st.metric("Bedrooms", details["Bedrooms"])

        with second:
            st.metric("Full Bathrooms", details["Full Bathrooms"])

        with third:
            st.metric("Half Bathrooms", details["Half Bathrooms"])

        st.caption(
            "Building area uses exterior measurements "
            "and differs from interior living area."
        )
    st.info(
        "Price prediction will be available after "
        "the team's final model is connected."
    )

    summary = json.dumps(
        details,
        indent=2,
        ensure_ascii=False,
    )

    st.download_button(
        label="Download Property Details",
        data=summary,
        file_name="chicago_property_details.json",
        mime="application/json",
    )
    st.divider()
    st.subheader("Comparable Sales")
    st.caption(
        "Historical examples from a sample of Chicago single-family sales. "
        "Matched by ZIP and neighborhood, then ranked by building area."
    )

    comparables_path = BASE_DIR / "app_assets" / "comparables.csv"

    with open(
        comparables_path,
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        matches = [
            sale
            for sale in reader
            if sale["zip_code"] == details["ZIP Code"]
            and sale["nbhd"] == details["Neighborhood Code"]
        ]

    matches.sort(
        key=lambda sale: abs(
            float(sale["char_bldg_sf"])
            - details["Building Area (sq ft)"]
        )
    )

    if matches:
        displayed_sales = matches[:3]
        columns = st.columns(len(displayed_sales))

        for column, sale in zip(columns, displayed_sales):
            with column:
                with st.container(border=True):
                    sold_price = float(sale["sale_price"])
                    area = float(sale["char_bldg_sf"])
                    sale_date = sale["sale_date"][:10]

                    st.caption("RECORDED SALE")
                    st.metric("Sold Price", f"${sold_price:,.0f}")

                    st.divider()

                    st.write(f"**{area:,.0f} sq ft**")
                    st.caption("Exterior building area")

                    st.write(f"**Sale Date:** {sale_date}")
                    st.write(f"**ZIP:** {sale['zip_code']}")
                    st.write(
                        f"**Neighborhood:** {sale['nbhd']}"
                    )

                    area_difference = (
                        area - details["Building Area (sq ft)"]
                    )

                    if area_difference == 0:
                        comparison = "Same building area as your input"
                    elif area_difference > 0:
                        comparison = (
                            f"{area_difference:,.0f} sq ft larger "
                            "than your input"
                        )
                    else:
                        comparison = (
                            f"{abs(area_difference):,.0f} sq ft smaller "
                            "than your input"
                        )

                    st.divider()
                    st.caption(comparison)

        st.caption(
            "These are past recorded sales, not current listings. "
            "Matching uses ZIP, Assessor neighborhood, and building area; "
            "condition and other differences may affect comparability."
        )

    else:
        st.info(
            "No matching sales were found in this sample. "
            "Other comparable transactions may exist."
        )
    if st.button("Back to Property Details"):
        st.session_state.page = "details"
        st.rerun()

# Data and accuracy screen
elif st.session_state.page == "data":
    st.markdown(
        '<div style="background:linear-gradient(120deg,#0F172A,#164E63);'
        'padding:32px;border-radius:22px;margin-bottom:24px;">'
        '<div style="color:#5EEAD4;font-size:12px;font-weight:700;'
        'letter-spacing:2px;">DATA & ACCURACY</div>'
        '<h1 style="color:white;font-size:clamp(28px,4vw,42px);'
        'margin:8px 0;padding:0;">Know what powers the tool.</h1>'
        '<p style="color:#CBD5E1;margin:0;">'
        'Understand the data, model status, and limits '
        'behind each result.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    with st.container(border=True):
        st.caption("MODEL STATUS")
        st.subheader("Final model integration pending")
        st.write(
            "Property review and market exploration are available. "
            "Price predictions and evaluation results will be added "
            "after the team confirms its final model."
        )

    st.write("")
    st.subheader("Core Data Sources")

    first, second, third = st.columns(3)

    with first:
        with st.container(border=True):
            st.caption("01 · TRANSACTIONS")
            st.subheader("Recorded Sales")
            st.write(
                "Historical sale prices, recording dates, "
                "and property identifiers."
            )
            st.markdown(
                "[View Cook County Sales ↗]"
                "(https://datacatalog.cookcountyil.gov/d/wvhk-k5uv)"
            )

    with second:
        with st.container(border=True):
            st.caption("02 · PROPERTIES")
            st.subheader("Building Details")
            st.write(
                "Building area, construction year, rooms, "
                "and other recorded characteristics."
            )
            st.markdown(
                "[View Building Data ↗]"
                "(https://datacatalog.cookcountyil.gov/d/x54s-btds)"
            )

    with third:
        with st.container(border=True):
            st.caption("03 · MARKET CONTEXT")
            st.subheader("Mortgage Rates")
            st.write(
                "Historical mortgage rates provide context "
                "for market conditions over time."
            )
            st.markdown(
                "[View FRED Mortgage Rates ↗]"
                "(https://fred.stlouisfed.org/series/MORTGAGE30US)"
            )

    st.caption(
        "The team also supplied ZIP mappings, crime, migration, "
        "tax, and unemployment data. Final model features "
        "remain subject to team review."
    )

    st.divider()
    st.subheader("Coverage & Interpretation")

    with st.container(border=True):
        st.write(
            "**Recorded sale period:** "
            "September 1, 2019–August 11, 2026."
        )
        st.markdown(
            "- **Building area:** Exterior measurements; "
            "different from interior living area.\n"
            "- **Sale dates:** Recording dates may differ "
            "from closing dates.\n"
            "- **Partial coverage:** 2019 and 2026 are incomplete years; "
            "the latest month is also incomplete.\n"
            "- **Location:** ZIP and Assessor neighborhood codes "
            "are separate identifiers.\n"
            "- **Historical sales:** Transactions shown are "
            "past sales, not current listings.\n"
            "- **Market trends:** Changes reflect the homes sold "
            "in the sample, not an individual home's appreciation.\n"
            "- **Area statistics:** Describe geographic areas, "
            "not individual households."
        )

    st.caption(
        "Prototype data cleaning is still being aligned with "
        "the team's final dataset."
    )
    
# Market overview screen
elif st.session_state.page == "market":
    st.markdown(
        '<div style="background:linear-gradient(120deg,#0F172A,#164E63);'
        'padding:32px;border-radius:22px;margin-bottom:24px;">'
        '<div style="color:#5EEAD4;font-size:12px;font-weight:700;'
        'letter-spacing:2px;">CHICAGO MARKET EXPLORER</div>'
        '<h1 style="color:white;font-size:clamp(28px,4vw,42px);'
        'margin:8px 0;padding:0;">See the market behind the home.</h1>'
        '<p style="color:#CBD5E1;margin:0;">'
        'Explore recorded sales, price trends, and '
        'year-over-year changes by ZIP.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Prototype Chicago single-family sales sample. "
        "Final dataset alignment is pending team review."
    )

    market = pd.read_csv(
        BASE_DIR / "app_assets" / "market_sales.csv",
        dtype={"zip_code": str},
        parse_dates=["sale_date"],
    )

    zip_choices = ["All available ZIPs"] + sorted(
        market["zip_code"].dropna().unique().tolist()
    )

    selected_zip = st.selectbox(
        "Explore a ZIP Code",
        options=zip_choices,
    )

    if selected_zip == "All available ZIPs":
        selected = market
    else:
        selected = market[
            market["zip_code"] == selected_zip
        ]

    st.write("")

    first, second, third = st.columns(3)

    with first:
        with st.container(border=True):
            st.caption("SALES ACTIVITY")
            st.metric(
                "Recorded Transactions",
                f"{len(selected):,}",
            )
            st.caption("Transactions in the selected sample")

    with second:
        with st.container(border=True):
            median_price = selected["sale_price"].median()

            st.caption("SALE PRICES")
            st.metric(
                "Median Sold Price",
                f"${median_price:,.0f}",
            )
            st.caption("Middle sale price across all covered years")

    with third:
        with st.container(border=True):
            median_area = selected["char_bldg_sf"].median()

            st.caption("BUILDING SIZE")
            st.metric(
                "Median Building Area",
                f"{median_area:,.0f} sq ft",
            )
            st.caption("Based on exterior measurements")

    st.caption(
        "Statistics describe transactions in this sample, "
        "not every home in Chicago. "
        "The 2019 and 2026 data cover partial years."
    )
    st.divider()
    st.subheader("Monthly Market Trends")

    monthly = (
        selected
        .assign(
            Month=selected["sale_date"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )
        .groupby("Month")
        .agg(
            Transactions=("sale_price", "size"),
            Median_Sold_Price=("sale_price", "median"),
        )
    )

    all_months = pd.date_range(
        start=market["sale_date"].min().to_period("M").to_timestamp(),
        end=market["sale_date"].max().to_period("M").to_timestamp(),
        freq="MS",
    )

    monthly = monthly.reindex(all_months)
    monthly.index.name = "Month"

    monthly["Transactions"] = (
        monthly["Transactions"].fillna(0).astype(int)
    )

    volume_tab, price_tab = st.tabs(
        ["Sales Activity", "Price Trends"]
    )

    with volume_tab:
        with st.container(border=True):
            st.subheader("Monthly Sales Activity")
            st.caption(
                "Number of recorded transactions in the selected sample."
            )
            st.bar_chart(monthly[["Transactions"]])

    with price_tab:
        with st.container(border=True):
            st.subheader("Monthly Median Sold Price")
            st.caption(
                "Median transaction price for each month, in dollars."
            )
            st.line_chart(monthly[["Median_Sold_Price"]])

    st.caption(
        "Charts reflect the selected ZIP and this transaction sample. "
        "Months without recorded transactions have no median price. "
        "The first and last months cover partial months."
    )

    st.divider()
    st.subheader("Year-over-Year Comparison")

    coverage_start = market["sale_date"].min()
    coverage_end = market["sale_date"].max()

    comparison_years = [
        int(year)
        for year in sorted(market["sale_date"].dt.year.unique())
        if coverage_start <= pd.Timestamp(
            year=int(year) - 1,
            month=1,
            day=1,
        )
    ]

    comparison_year = st.selectbox(
        "Comparison Year",
        options=comparison_years,
        index=len(comparison_years) - 1,
    )

    current_start = pd.Timestamp(
        year=comparison_year, month=1, day=1
    )

    current_end = min(
        pd.Timestamp(year=comparison_year, month=12, day=31),
        coverage_end,
    )

    previous_start = current_start - pd.DateOffset(years=1)
    previous_end = current_end - pd.DateOffset(years=1)

    current = selected[
        selected["sale_date"].between(current_start, current_end)
    ]

    previous = selected[
        selected["sale_date"].between(previous_start, previous_end)
    ]

    st.caption(
        f"Comparing {current_start:%Y-%m-%d} to {current_end:%Y-%m-%d} "
        f"with {previous_start:%Y-%m-%d} to {previous_end:%Y-%m-%d}."
    )

    if current.empty or previous.empty:
        st.info("Not enough transactions to compare these periods.")

    else:
        current_median = current["sale_price"].median()
        previous_median = previous["sale_price"].median()

        price_change = (
            current_median / previous_median - 1
        ) * 100

        volume_change = (
            len(current) / len(previous) - 1
        ) * 100

        left, right = st.columns(2)

        with left:
            st.metric(
                "Transactions in Comparison Period",
                f"{len(current):,}",
                delta=f"{volume_change:+.1f}% vs prior period",
                delta_color="off",
            )

        with right:
            st.metric(
                "Median Sold Price in Comparison Period",
                f"${current_median:,.0f}",
                delta=f"{price_change:+.1f}% vs prior period",
                delta_color="off",
            )

        st.caption(
            f"Current period: {len(current):,} transactions. "
            f"Prior period: {len(previous):,} transactions. "
            "Changes reflect this sample and the mix of homes sold, "
            "not the appreciation of an individual property."
        )

    if st.button("Return to Home"):
        st.session_state.page = "home"
        st.rerun()