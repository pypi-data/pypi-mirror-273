from __future__ import annotations

import argparse

import kubeinfra
from kubeinfra import Embeddings
from kubeinfra.utils import get_logger


logger = get_logger(str(__name__))


def add_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    COMMAND_NAME = "embeddings"
    subparser = subparsers.add_parser(COMMAND_NAME)

    subparser.add_argument(
        "input",
        metavar="INPUT",
        default=None,
        type=str,
        help="A string providing context for the model to embed",
    )

    subparser.add_argument(
        "--model",
        "-m",
        default=kubeinfra.default_embedding_model,
        type=str,
        help=f"The name of the model to query. Default={kubeinfra.default_text_model}",
    )
    subparser.set_defaults(func=_run_complete)


def _run_complete(args: argparse.Namespace) -> None:
    embeddings = Embeddings()

    try:
        response = embeddings.create(
            input=args.input,
            model=args.model,
        )

        print([e.embedding for e in response.data])
    except kubeinfra.AuthenticationError:
        logger.critical(kubeinfra.MISSING_API_KEY_MESSAGE)
        exit(0)
