def main():
    """
    Parse the command line arguments and execute the appropriate command.
    """

    parser = argparse.ArgumentParser(description="Process BotifyMe commands.")
    parser.add_argument_group("commands")
    parser.add_argument(
        "command",
        help="The command to execute. Possible values: generate-config, exec-tool, list-tools.",
    )
    parser.add_argument(
        "--tool-name", type=str, default=None, help="The function to execute."
    )
    parser.add_argument(
        "--tool-args",
        type=str,
        default=None,
        help="The arguments to pass to the function.",
    )

    parser.add_argument(
        "--temp-dir",
        type=str,
        default=None,
        help="The temporary directory to use for the execution.",
    )

    args = parser.parse_args()

    if args.command == "generate-config":
        generate_config()
    elif args.command == "exec-tool":
        execute_tool(args.tool_name, args.tool_args, args.temp_dir)
    elif args.command == "list-tools":
        list_tools()
    else:
        raise ValueError(f"Unknown command: {args.command}")
