# recommender.py
import pandas as pd
import sys
import os

def recommend_funds(risk_appetite):
    """
    Inputs: 'Low', 'Moderate', 'High' risk appetite classes
    Outputs: Top 3 matching system fund codes ranked by Sharpe Ratio
    """
    # 1. Look for the file in the data/processed directory relative to project root
    path_options = [
        'data/processed/fund_scorecard.csv',
        '../data/processed/fund_scorecard.csv',
        'processed/fund_scorecard.csv'
    ]
    
    scorecard_path = None
    for path in path_options:
        if os.path.exists(path):
            scorecard_path = path
            break
            
    if not scorecard_path:
        return "❌ Error: Could not locate 'fund_scorecard.csv'. Please check file execution path."
        
    # 2. Read the card ledger matrix
    scorecard = pd.read_csv(scorecard_path)
    
    # --- DYNAMIC RISK CLASSIFICATION VIA QUANTILE SPLITS ---
    # Low Risk = High Sharpe Stability, High Risk = High Volatility Seekers
    # We slice the dataset into 3 parts based on existing metrics
    try:
        q33 = scorecard['sharpe_ratio'].quantile(0.33)
        q66 = scorecard['sharpe_ratio'].quantile(0.66)
        
        # Clean string manipulation for input arguments
        clean_input = str(risk_appetite).strip().capitalize()
        
        if clean_input == 'Low':
            # Low Risk Appetite: Prefers stable, optimized performers
            matches = scorecard[scorecard['sharpe_ratio'] >= q66]
            display_grade = "Low Risk Profile (Top Tier Sharpe Stability)"
        elif clean_input == 'High':
            # High Risk Appetite: Aggressive return seekers, potentially higher volatility tolerance
            matches = scorecard[scorecard['sharpe_ratio'] <= q33]
            display_grade = "High Risk Profile (Aggressive Performance Profiles)"
        else:
            # Default to Moderate Risk
            matches = scorecard[(scorecard['sharpe_ratio'] > q33) & (scorecard['sharpe_ratio'] < q66)]
            display_grade = "Moderate Risk Profile (Balanced Risk/Return Grid)"
            
    except KeyError:
        return "❌ Error: 'sharpe_ratio' column missing from data source matrix layout."

    if matches.empty:
        return f"⚠️ No direct matches found for risk layout profile."
        
    # 3. Sort by total fund performance score to extract the top 3 items
    top_3 = matches.sort_values(by='fund_score', ascending=False).head(3)
    
    # Add our virtual dynamic column for presentation output formatting clarity
    output_df = top_3[['amfi_code', 'scheme_name', 'sharpe_ratio', 'fund_score']].copy()
    output_df['assigned_profile'] = display_grade
    
    return output_df

if __name__ == "__main__":
    # Pull incoming args or default gracefully to Moderate focus
    user_input = sys.argv[1] if len(sys.argv) > 1 else 'Moderate'
    
    print(f"\n--- BLUESTOCK INTELLIGENT RECOMMENDATION SYSTEM OUTCOMES FOR: {user_input.upper()} RISK ---")
    
    results = recommend_funds(user_input)
    
    # SAFE CHECK: Handle text validation dynamically without raising internal object attributes errors
    if isinstance(results, str):
        print(results)
    else:
        print(results.to_string(index=False))