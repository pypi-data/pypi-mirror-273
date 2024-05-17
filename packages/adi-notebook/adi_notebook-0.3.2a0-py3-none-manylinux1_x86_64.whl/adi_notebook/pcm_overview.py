import argparse

from adi_notebook.runner import PCM

# import argcomplete


def main():
    parser = argparse.ArgumentParser(
        prog="pcm-overview",
        description="Overview Processing Configuration Manager (PCM). EXAMPLE:\n"
        "pcm-overview <process_name>",
    )
    parser.add_argument("process_name", help="<process_name>")
    args = parser.parse_args()

    pcm = PCM(process_name=args.process_name)
    df = pcm.get_pcm_overview(pivot_by_col="no_pivot", show_pivot_name=True).drop(
        columns="rules"
    )
    print(df.to_markdown(tablefmt="fancy_outline", index=False))


if __name__ == "__main__":
    main()
