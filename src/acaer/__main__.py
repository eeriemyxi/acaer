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
    DIGIT = enum.auto()
    OPERATOR = enum.auto()


@dataclasses.dataclass
class Token:
    token_type: TokenType
    literal: str
    precedence: int
    line: int
    column: int

    @classmethod
    def from_char(cls, char: str, line: int, column: int) -> "Token | None":
        if char.isdigit():
            token_type = TokenType.DIGIT
        elif char in "*/+-":
            token_type = TokenType.OPERATOR
        else:
            return None

        return cls(
            token_type=token_type,
            literal=char,
            precedence=get_precedence(char),
            line=line,
            column=column,
        )


def get_precedence(char: str):
    match char:
        case "*" | "/":
            return 2
        case "+" | "-":
            return 1
        case _:
            return 0


def get_expr() -> str:
    return "1 + 2\n * 6 / 2 * oarsetaortsn6 / 2"


def goto_address(line, col) -> str:
    return f"({line}:{col})"


def tokenize_expr(expr: str) -> list[Token]:
    stack = list()
    line = 1
    col = 0

    for c in expr:
        col += 1

        if c in string.whitespace:
            if c == "\n":
                line += 1
                col = 0
            continue

        current_token = Token.from_char(c, line, col)
        if not current_token:
            log.warning("Unexpected char %s: %s", goto_address(line, col), repr(c))
            log.info("Ignoring char %s: %s", goto_address(line, col), repr(c))
            continue

        stack.append(current_token)

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
