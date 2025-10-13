from financegy.modules.securities import get_securities

securities = get_securities()

# Print all securities
for security in securities:
    print(security)

# Only print a certain security
for security in securities:
    if security["acronym"] == "DIH":
        print(security)