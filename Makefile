
LOG_LEVEL := INFO

WORKING_DIR := working
IMPACT_DIR := $(WORKING_DIR)/impact
PARAMS_DIR := $(WORKING_DIR)/params
DATASPEC_DIR := dataspecs

FEATURES := \
	frac_B03002_003E:"Fraction of Population Who Identify as Non-Hipanic or Latino White Alone" \
	frac_B03002_004E:"Fraction of Population Who Identify as Non-Hipanic or Latino Black of African American Alone" \
	frac_B03002_005E:"Fraction of Population Who Identify as Non-Hipanic or Latino American Indian and Alaska Native Alone" \
	frac_B03002_006E:"Fraction of Population Who Identify as Non-Hipanic or Latino Asian Alone" \
	frac_B03002_007E:"Fraction of Population Who Identify as Non-Hipanic or Latino Native Hawaiian and Other Pacific Islander Alone" \
	frac_B03002_008E:"Fraction of Population Who Identify as Non-Hipanic or Latino Some Other Race Alone" \
	frac_B03002_010E:"Fraction of Population Who Identify as Non-Hipanic or Latino Two Races Including Some Other Race" \
	frac_B03002_011E:"Fraction of Population Who Identify as Non-Hipanic or Latino Two Races Excluding Some Other Race, and Three or More Races" \
	frac_B03002_012E:"Fraction of Population Who Identify as Hispanic or Latino of Any Race" \
	B19013_001E:"Median Household Income"
	# B25119_002E:"Median Household Income of Homeowners"

TARGET := B25077_001E:"Median Home Value"

WEIGHT := B25003_002E:"Total Owner-Occupied Households"

# Income is capped at $250k; higher values clipped to $250.001.
# Home values is capped at $2MM; higher values clipped to $2,000,000.
FILTERS := \
	"B19013_001E <= 250000" \
	"B25077_001E <= 2000000"

.PHONY: all data clean

all: plots

data: $(WORKING_DIR)/la-cbsa.csv

params: $(PARAMS_DIR)/la-cbsa.yaml

plots: $(IMPACT_DIR)/la-cbsa

clean:
	rm -rf $(WORKING_DIR)

$(WORKING_DIR)/la-cbsa.csv: $(DATASPEC_DIR)/la-cbsa.yaml
	mkdir -p $(@D)
	censusdis --log $(LOG_LEVEL) download -o $@ $<

$(PARAMS_DIR)/la-cbsa.yaml: $(WORKING_DIR)/la-cbsa.csv
	mkdir -p $(@D)
	impactchart --log $(LOG_LEVEL) optimize -f $(FILTERS) -X $(FEATURES) -y $(TARGET) -w $(WEIGHT) -o $@ $<

$(IMPACT_DIR)/la-cbsa: $(PARAMS_DIR)/la-cbsa.yaml $(WORKING_DIR)/la-cbsa.csv
	mkdir -p $@
	impactchart --log $(LOG_LEVEL) plot -f $(FILTERS) -p $(PARAMS_DIR)/la-cbsa.yaml --yformat=DOLLAR -o $@ $(WORKING_DIR)/la-cbsa.csv
