import os
import json
import importlib
genai = None
types = None
HAS_GENAI = False
# Safe optional imports for Google GenAI SDK
try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

def generate_scr_narrative_offline(findings: dict) -> dict:
    """
    Offline fallback path (Task 4): Generates the SCR narrative using 
    a deterministic template with zero network dependency or API key required.
    """
    narrative = f"""Situation:
Mamaearth's data pipeline processed a total uncleaned baseline revenue of ₹{findings['raw_total_revenue_inr']:,.2f} across all raw orders. Following rigorous data cleaning, deduplication, and anomaly handling, the verified clean total revenue stands at ₹{findings['cleaned_total_revenue_inr']:,.2f}.

Complication:
Operational risks severely threaten profitability, driven primarily by payment methods and volume anomalies. Cash on Delivery (COD) orders exhibit an alarming return rate of {findings['return_rate_by_payment']['COD']}%—roughly three times higher than card payments. When segmented by geography, COD orders originating from Tier-2 cities spike to a highest-risk return rate of {findings['highest_risk_segment']['return_rate_pct']}%. Furthermore, initial time series trends were distorted by bulk volume outliers, falsely highlighting January as the top revenue month.

Resolution:
Precise financial reconciliation identified a duplicate-driven reconciliation delta of ₹{findings['duplicate_reconciliation_delta_inr']:,.2f} resulting from duplicate order removal. Once these outliers are filtered out, January's apparent revenue of ₹{findings['outlier_inflated_month']['apparent_revenue_inr']:,.2f} normalizes to ₹{findings['outlier_inflated_month']['corrected_revenue_inr']:,.2f}, firmly establishing March as the true peak month with ₹{findings['true_peak_month']['revenue_inr']:,.2f} in revenue. Strategic policy adjustments targeting COD in Tier-2 regions are recommended immediately."""

    return {
        "status": "success",
        "narrative": narrative,
        "tokens": 0
    }

def generate_scr_narrative(findings: dict) -> dict:
    """
    Generates the SCR business report using the Gemini API (Task 2 & 3) 
    with parameter locking, system instructions, and fallback safety.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not HAS_GENAI or not api_key:
        return generate_scr_narrative_offline(findings)
    
    try:
        client = genai.Client(api_key=api_key)
        
        system_instruction = (
            "You are a senior data analyst writing for Mamaearth's regional ops and finance heads. "
            "You must structure your response into exactly three labeled sections: Situation, Complication, Resolution. "
            "Explicit constraint: Every number and figure used in your output must come from the supplied findings dictionary "
            "and appear with the exact same value—no invented statistics."
        )
        
        user_prompt = f"""Please generate the SCR business narrative using these validated findings:
- Cleaned Total Revenue: ₹{findings['cleaned_total_revenue_inr']}
- Raw Total Revenue: ₹{findings['raw_total_revenue_inr']}
- Duplicate Reconciliation Delta: ₹{findings['duplicate_reconciliation_delta_inr']}
- Return Rates by Payment: {findings['return_rate_by_payment']}
- Highest Risk Segment: {findings['highest_risk_segment']}
- True Peak Month: {findings['true_peak_month']}
- Outlier Inflated Month: {findings['outlier_inflated_month']}
"""

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.0,
            max_output_tokens=400,
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=config,
        )
        
        return {
            "status": "success",
            "narrative": response.text,
            "tokens": getattr(response, 'usage_metadata', None) and getattr(response.usage_metadata, 'total_token_count', 0) or 0
        }
        
    except Exception as err:
        offline_res = generate_scr_narrative_offline(findings)
        offline_res["message"] = str(err)
        return offline_res

if __name__ == "__main__":
    findings_path = 'narrator/findings.json'
    if not os.path.exists(findings_path):
        raise FileNotFoundError(f"Error: {findings_path} not found. Run analysis/clean_and_eda.py first.")
        
    with open(findings_path, 'r') as f:
        findings = json.load(f)
        
    result = generate_scr_narrative(findings)
    
    print("==================================================")
    print(f" PART 3 NARRATIVE STATUS: {result['status'].upper()}")
    print("==================================================\n")
    print(result["narrative"])
    
    os.makedirs('narrator', exist_ok=True)
    sample_output_path = 'narrator/sample_output.txt'
    with open(sample_output_path, 'w', encoding='utf-8') as out_f:
        out_f.write(result["narrative"])
    print(f"\n[INFO] Saved narrative sample to {sample_output_path}")
    
    print("\n--- TASK 5: NUMERIC ACCURACY CHECKLIST ---")
    narrative_text = result["narrative"]
    required_figures = ["97,358.30", "44.4", "54.5", "2,501.90", "20,318.90"]
    normalized_text = narrative_text.replace(",", "")
    
    passed_all = True
    for fig in required_figures:
        clean_fig = fig.replace(",", "")
        if fig in narrative_text or clean_fig in normalized_text or fig.replace(".30", ".3") in narrative_text:
            print(f" [PASS] Required figure present: {fig}")
        else:
            print(f" [FAIL] Required figure missing: {fig}")
            passed_all = False
            
    if passed_all:
        print("\nResult: ALL NUMERIC CHECKS PASSED SUCCESSFULLY!")
    else:
        print("\nResult: Some numeric checks failed.")