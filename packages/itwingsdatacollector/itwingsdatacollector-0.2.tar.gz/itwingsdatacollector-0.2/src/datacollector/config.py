############################################################################################################
# Pagespeed
############################################################################################################

ps_config = {
    "thresholds": {	
        "LCP": 2500,  # milliseconds
        "INP": 200,  # milliseconds
        "CLS": 0.1  # CLS score
    },
    "metrics": {
        "LCP": "LARGEST_CONTENTFUL_PAINT_MS",
        "INP": "INTERACTION_TO_NEXT_PAINT",
        "CLS": "CUMULATIVE_LAYOUT_SHIFT_SCORE",
        "FCP": "FIRST_CONTENTFUL_PAINT_MS",
        "FID": "FIRST_INPUT_DELAY_MS",
        "TTFB": "EXPERIMENTAL_TIME_TO_FIRST_BYTE"
    }
}