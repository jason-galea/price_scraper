from src.Database import SSD

CATEGORY_CLASS_DICT = {
    # "hdd":      HDD,
    "ssd":      SSD,
    # "ddr4":     RAM,
    # "ddr5":     RAM,
}

PAGE_INFO = {
    "index":{
        "route":        "/",
        "template":     "children/index.html",
        "title":        "Home",
        "desc": [
            "Welcome to Price Scraper (TM)!",
            "This website will scrape & display the latest price/specs/etc. of computer hardware.",
            "It's designed to work with specific Australian computer parts retailers."
        ]
    },
    "scrape":{
        "route":        "/scrape",
        "template":     "children/scrape.html",
        "title":        "Scrape",
        "desc": [
            "This page lets you scrape the latest data from your chosen website & category.",
            "Make a selection and press 'Submit' to continue."
        ]
    },
    "table":{
        "route":        "/table",
        "template":     "children/table.html",
        "title":        "Table",
        "desc": [
            "This page allows you to view the most recent result for a given website & category.",
            "The data will be displayed in a table.",
            "Make a selection and press 'Submit' to continue."
        ]
    },
    "graph":{
        "route":        "/graph",
        "template":     "children/graph.html",
        "title":        "Graph",
        "desc": [
            "This page allows you to view the most recent result for a given website & category.",
            "The data will be displayed in a graph.",
            "Make a selection and press 'Submit' to continue."
        ]
    },
    "results":{
        "route":        "/results",
        "template":     "children/results.html",
        "title":        "Results",
        "desc": [
            "This page shows all previously collected result files.",
            "In case of any error, collecting some more data in the 'Scrape' page"
        ]
    },
    "test":{
        "route":        "/test",
        "template":     "children/test.html",
        "title":        "TEST",
        "desc": [
            "TEST PAGE"
        ]
    }
}

FORM_LABELS = {
    "website":{
        "pccg":         "PC Case Gear",
        "scorptec":     "Scorptec",
        "centrecom":    "Centre Com"
    },
    "category":{
        "hdd":      "3.5\" Hard Drive",
        "ssd":      "SSD",
        "ddr4":     "DDR4",
        "ddr5":     "DDR5",
        "cpu":      "CPU",
        "gpu":      "GPU"
    }
}

TABLE_COLS = {
    "hdd": {
        "display_cols": ["TitleLink", "Brand", "PriceAUD", "CapacityTB", "PricePerTB"],
        "sort_col":     "PricePerTB"
    },
    "ssd": {
        "display_cols": ["TitleLink", "Brand", "PriceAUD", "Protocol", "CapacityTB", "PricePerTB"],
        "sort_col":     "PricePerTB"
    },
    "ddr4": {
        "display_cols": ["TitleLink", "Brand", "Model", "KitConfiguration", "CapacityGB", "PriceAUD", "PricePerGB"],
        "sort_col":     "PricePerGB"
    },
    "ddr5": {
        "display_cols": ["TitleLink", "Brand", "Model", "KitConfiguration", "CapacityGB", "PriceAUD", "PricePerGB"],
        "sort_col":     "PricePerGB"
    },
    "cpu": {
        "display_cols": ["TitleLink", "Brand", "PriceAUD"],
        "sort_col":     "PricePerTB"
    },
    "gpu": {
        "display_cols": ["TitleLink", "Brand", "PriceAUD"],
        "sort_col":     "PricePerTB"
    }
}
