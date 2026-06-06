def validate_args(args):
    if args.temperature < 0 or args.temperature > 2:
        raise ValueError("temperatureは0〜2で指定してください")

    if args.max_tokens <= 0:
        raise ValueError("max_tokensは1以上にしてください")

    if not args.session.strip():
        raise ValueError("session can't be empty (e.g. --session work)")


def show_config(
    session: str, role: str, model: str, temperature: float, max_tokens: int
):
    print("=== AI CLI Config ===")
    print(f"session     : {session}")
    print(f"role        : {role}")
    print(f"model       : {model}")
    print(f"temperature : {temperature}")
    print(f"max_tokens  : {max_tokens}")
    print("======================")


def show_help():
    print("=== Runtime Commands ===")
    print("/config         show current config")
    print("/session xxx    change session")
    print("/role xxx       change role")
    print("/role           list current roles")
    print("/history        view history")
    print("/reset          clear conversation")
    print("/exit           Exit CLI")
