from market_data import download_all_stocks


if __name__ == "__main__":

    results = download_all_stocks()

    print("\n========== DOWNLOAD SUMMARY ==========")

    for result in results:
        print(result)