from dataclasses import dataclass
import pandas as pd


def get_change_log(file: str) -> pd.DataFrame:
    """Read Change log from Pauper Cube XLSX File"""
    return pd.read_excel(file, sheet_name="Change Log")


def get_before(df: pd.DataFrame, block: str) -> pd.DataFrame:
    """Return dataframe excluding specified block and all past blocks"""
    q = df.query(f"Update == '{block}'")
    idx = q.index.min()
    return df.iloc[: idx - 1]


def get_buy_list(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return buy list from pruned Pauper Change List"""
    cards_in = df["In"]
    cards_out = df["Out"]
    set_in, set_out = set(cards_in.values), set(cards_out.values)
    keys = set_in - set_out
    double_cards = set_in.intersection(set_out)

    in_df = pd.Series(list(keys))
    double_df = pd.Series(list((double_cards)))

    return in_df, double_df


def save_buylists(dfs: tuple[pd.DataFrame, pd.DataFrame]) -> None:
    in_df, double_df = dfs

    in_df.name = ""
    in_df.to_csv("buylist.txt", index=None)

    double_df.name = ""
    double_df.to_csv("doubles.txt", index=None)


def clear_title(file: str, outfile: str = None) -> None:
    """Clear the title line of a csv file"""

    def remove_first_line(lines: list[str]) -> list[str]:
        """Remove the first line of a list of lines from a file"""
        new_file = []
        for idx, line in enumerate(lines):
            if idx == 0:
                continue
            new_file.append(line)
        return new_file

    with open(file, "r") as fh:
        new_file = remove_first_line(fh.readlines())

    if outfile is None:
        outfile = file

    with open(outfile, "w") as fh:
        fh.writelines(new_file)


def main(file: str, block: str):
    """
    Run application, given Pauper Cube XLSX file location and last updated
    block
    """
    change_log = get_change_log(file)
    new_cards = get_before(change_log, block)
    in_df, double_df = get_buy_list(new_cards)
    save_buylists((in_df, double_df))
    for file in ("buylist.txt", "doubles.txt"):
        clear_title(file)
    print(in_df)


if __name__ == "__main__":
    # import argparse
    # p = argparse.ArgumentParser(
    #     description="Read Pauper Cube and return newcards"
    # )
    # p.add_argument('file', help="Pauper Cube XLSX file", default=FILE)
    # p.add_argument(
    #     'block', help="Last Block Updated", default='Throne of Eldraine'
    # )
    # p.parse_args()
    # main(p.file, p.block)
    URL = "https://docs.google.com/spreadsheets/d/12iQhC4bHqFW7hEWxPBjyC8yBDehFZ0_4DkqzyA8EL3o/edit?usp=sharing"
    FILE = "./The Pauper Cube.xlsx"
    block = "CMR/KHM"
    main(FILE, block)
