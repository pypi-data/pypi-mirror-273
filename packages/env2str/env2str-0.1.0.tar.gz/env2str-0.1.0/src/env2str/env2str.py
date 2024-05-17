from typing import Annotated

import typer
from dotenv import dotenv_values

app = typer.Typer()


def load_env(env_file: str) -> dict[str, str | None]:
    return dotenv_values(env_file)


def env_to_str(env_values: dict[str, str | None]) -> str:
    return ";".join([f"{key}={value}" for key, value in env_values.items()])


@app.command(
    name="env2str",
    help="Converts a .env file to a string with the format 'key=value;key=value'",
)
def env2str(env_file: Annotated[str, typer.Option("-e", "--env", help="Path to .env file")] = ".env") -> None:
    env_values = load_env(env_file)
    print(env_to_str(env_values))


if __name__ == "__main__":
    app()
