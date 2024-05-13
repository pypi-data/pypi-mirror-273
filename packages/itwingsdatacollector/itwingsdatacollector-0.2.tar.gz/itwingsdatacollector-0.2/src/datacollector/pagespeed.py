from datacollector.raw_data_to_csv import raw_data_to_csv
import requests
from datacollector.config import *

def pagespeed(pagespeed_parameters):
    # Initial data dictionary setup
    data = {
        "url": pagespeed_parameters['url']
    }
    # Setup the initial data structure with default "" values
    def setup_no_data():
        data.update(
            {f"{strategy}_evaluation_result": "-" for strategy in pagespeed_parameters["strategies"]})

    try:
        for strategy in pagespeed_parameters["strategies"]:
            # API request
            response = requests.get(
                f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={pagespeed_parameters["url"]}&strategy={strategy}')
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Processing response
            report = response.json()

            if ("LARGEST_CONTENTFUL_PAINT_MS" in report.get("loadingExperience", {}).get("metrics", {}) and
                "INTERACTION_TO_NEXT_PAINT" in report.get("loadingExperience", {}).get("metrics", {}) and
                    "CUMULATIVE_LAYOUT_SHIFT_SCORE" in report.get("loadingExperience", {}).get("metrics", {})):

                if (report["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"] > ps_config["thresholds"]["LCP"] or
                    report["loadingExperience"]["metrics"]["INTERACTION_TO_NEXT_PAINT"]["percentile"] > ps_config["thresholds"]["INP"] or
                        report["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100 > ps_config["thresholds"]["CLS"]):
                    result = "failed"
                else:
                    result = "passed"

                data[f"{strategy}_evaluation_result"] = result
            else:
                setup_no_data()

        raw_data_to_csv("pagespeed", data, append=True)

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving pagespeed report: {e}")
        # If there is an error, setup data dictionary with ""
        setup_no_data()
        # Then save or log the error data as needed
        raw_data_to_csv("pagespeed", data, append=True)
