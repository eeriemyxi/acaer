import dataclasses
import enum
import logging
import string

from rich.logging import RichHandler

logging.basicConfig(
    level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
log = logging.getLogger(__name__)


class TokenType(enum.Enum):
    ZERO = enum.auto()
    ONE = enum.auto()
    TWO = enum.auto()
    THREE = enum.auto()
    FOUR = enum.auto()
    FIVE = enum.auto()
    SIX = enum.auto()
    SEVEN = enum.auto()
    EIGHT = enum.auto()
    NINE = enum.auto()

    MUL = enum.auto()
    DIV = enum.auto()
    ADD = enum.auto()
    SUB = enum.auto()


@dataclasses.dataclass
class Token:
    token_type: TokenType
    literal: str
    precedence: int
    line: int
    column: int


LITERAL_TOKENS = {
    "0": TokenType.ZERO,
    "1": TokenType.ONE,
    "2": TokenType.TWO,
    "3": TokenType.THREE,
    "4": TokenType.FOUR,
    "5": TokenType.FIVE,
    "6": TokenType.SIX,
    "7": TokenType.SEVEN,
    "8": TokenType.EIGHT,
    "9": TokenType.NINE,
    "*": TokenType.MUL,
    "/": TokenType.DIV,
    "+": TokenType.ADD,
    "-": TokenType.SUB,
}


def get_precedence(char: str):
    match char:
        case "*" | "/":
            return 2
        case "+" | "-":
            return 1
        case _:
            return 0


def get_expr() -> str:
    return "1 + 2 * 6 / 2 * oarsetaortsn6 / 2"


def goto_address(line, col) -> str:
    return f"({line}:{col})"


def tokenize_expr(expr: str) -> list[Token]:
    stack = list()
    line = 1
    for col, c in enumerate(expr, 1):
        if c in string.whitespace:
            line += c == "\n"
            continue

        current_token = LITERAL_TOKENS.get(c)
        if not current_token:
            log.warning("Unexpected char %s: %s", goto_address(line, col), repr(c))
            log.info("Ignoring char %s: %s", goto_address(line, col), repr(c))
            continue

        stack.append(
            Token(
                token_type=current_token,
                literal=c,
                precedence=get_precedence(c),
                line=line,
                column=col,
            )
        )
    return stack


def main() -> int:
    expr = get_expr()
    log.info(f"{expr=}")

    expr_tokenized = tokenize_expr(expr)
    log.info(f"{expr_tokenized=}")

    rpn: list[Token] = []
    stack: list[Token] = []

    # TODO: handle parentheses
    for token in expr_tokenized:
        log.info(
            f"{goto_address(token.line, token.column)}  {token.literal=}  {token.precedence=}"
        )
        if token.literal.isdigit():
            rpn.append(token)
        elif token.literal in "*/-+":
            while stack and stack[-1].precedence >= token.precedence:
                rpn.append(stack.pop())
            stack.append(token)
    while stack:
        rpn.append(stack.pop())

    log.info("RPN: %s", [c.literal for c in rpn])

    return 0


if __name__ == "__main__":
    exit(main())
