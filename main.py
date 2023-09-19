import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px


# Title and introduction
st.title("Company Fundamentals Showcase with Streamlit")
st.write("Enter a stock ticker symbol to view company fundamentals.")

# Input for entering the stock ticker symbol
ticker = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL):")

# Create a placeholder for displaying company information
company_info_placeholder = st.empty()

# Button to trigger data fetching
if st.button("Get Data"):
    if ticker:
        # Display loading animation while fetching data
        with st.spinner("Fetching data..."):
            try:
                # Get company information using yfinance
                company = yf.Ticker(ticker)
                company_data = company.info
                                
                # Create a Streamlit app
                #         st.subheader(f"Company Information for {company.info['shortName']}")
                st.title(f"Company Report for {company_data['shortName']}")

                # Section 1: Company Business Summary
                st.header("1. Company Business Summary")
                st.write(company_data['longBusinessSummary'])

                # Section 2: Company Officers
                st.header("2. Company Officers")
                officers_data = company_data['companyOfficers']
                officers_df = pd.DataFrame(officers_data)
                officers_df = officers_df.drop('maxAge', axis=1)
                st.dataframe(officers_df)

                # Section 3: Financial Summary
                st.header("3. Financial Summary")

                # Create a table for financial data (e.g., market cap, revenue, etc.)

                # Format market cap, revenue, and profit margins in billions
                market_cap_billion = company_data['marketCap'] / 1e9
                revenue_billion = company_data['totalRevenue'] / 1e9
                profit_margins = company_data['profitMargins'] * 100  # Convert to percentage

                st.write(f"Market Cap: ${market_cap_billion:.2f}B")
                st.write(f"Revenue: ${revenue_billion:.2f}B")
                st.write(f"Profit Margins: {profit_margins:.2f}%")

                # Section 4: Interactive Charts and Graphs
                st.header("4. Price and PE Ratio Comparison")

                # Create an interactive bar chart for Price vs. PE ratio using Plotly
                price_pe_data = {
                    'Metric': ['Price', 'PE Ratio'],
                    'Value': [company_data['currentPrice'], company_data['trailingPE']],
                }
                price_pe_df = pd.DataFrame(price_pe_data)

                fig = px.bar(price_pe_df, x='Metric', y='Value', text='Value')
                fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                fig.update_layout(xaxis_title='Metric', yaxis_title='Value', title='Price vs. PE Ratio')
                st.plotly_chart(fig)


                st.header("5. Shareholder Distribution")
                # Create an interactive pie chart for Shareholder Distribution using Plotly
                shareholder_data = {
                    'Category': ['Institutions', 'Insiders', 'Public'],
                    'Percentage': [company_data['heldPercentInstitutions'], company_data['heldPercentInsiders'], 1 - company_data['heldPercentInstitutions'] - company_data['heldPercentInsiders']],
                }
                shareholder_df = pd.DataFrame(shareholder_data)

                fig_pie = px.pie(shareholder_df, values='Percentage', names='Category', title='Shareholder Distribution')
                st.plotly_chart(fig_pie)

                # You can add more interactive charts and visualizations here as needed.

                # Section 5: Recommendations and Analyst Opinions
                st.header("5. Recommendations and Analyst Opinions")

                # Display analyst recommendations and opinions
                st.write(f"Recommendation Key: {company_data['recommendationKey']}")
                st.write(f"Number of Analyst Opinions: {company_data['numberOfAnalystOpinions']}")

                # Section 6: Risk Assessment
                st.header("6. Risk Assessment")

                # Create a table for risk assessment data
                risk_data = {
                    'Audit Risk': [company_data['auditRisk']],
                    'Board Risk': [company_data['boardRisk']],
                    'Compensation Risk': [company_data['compensationRisk']],
                    'Shareholder Rights Risk': [company_data['shareHolderRightsRisk']],
                    'Overall Risk': [company_data['overallRisk']],
                }
                risk_df = pd.DataFrame(risk_data)
                st.table(risk_df)

                # You can add more sections and data as needed.

                # Section 7: Conclusion
                st.header("7. Conclusion")
                st.write("This report provides an overview of the company's business, financials, and risk assessment.")

                # Section 8: Data Source
                st.header("8. Data Source")
                st.write(f"Data source: {company_data['website']}")

                # Footer
                st.text("Powered by Streamlit")


                # Display the company name and logo
                # company_info_placeholder.subheader(f"Company Information for {company.info['shortName']}")

                # company_df = pd.DataFrame.from_dict(company.info, orient='index', columns=['Value'])

                # # Display the company report
                # st.subheader("Company Report")
                # st.write("Here is the company report:")
                # st.table(company_df)
                # st.json(company.info)

            except Exception as e:
                company_info_placeholder.error(f"An error occurred: {str(e)}")
