
"""
Calculadora de Dano T20 — primeira versão.

Calcula o dano médio de expressões como:
    1d8+4+1d6

Aceita dados de dano e bônus fixos.
Acertos críticos serão adicionados depois.
"""

import re


def media_dado(faces: int) -> float:
    """Calcula a média de um dado."""
    if faces < 1:
        raise ValueError("O dado precisa ter pelo menos 1 face.")

    return (faces + 1) / 2


def calcular_dano_medio(expressao: str) -> float:
    """Calcula o dano médio de uma expressão, como 1d8+4+1d6."""

    texto = expressao.replace(" ", "").lower()

    if not texto:
        raise ValueError("Digite uma expressão de dano, como 1d8+4.")

    termos = re.findall(r"[+-]?[^+-]+", texto)

    if "".join(termos) != texto:
        raise ValueError("Expressão inválida. Exemplo: 1d8+4+1d6.")

    total = 0.0

    for termo in termos:
        sinal = -1 if termo.startswith("-") else 1
        parte = termo.lstrip("+-")

        dado = re.fullmatch(r"(\d*)d(\d+)", parte)

        if dado:
            quantidade = int(dado.group(1) or "1")
            faces = int(dado.group(2))

            if quantidade < 1 or faces < 1:
                raise ValueError("Quantidade de dados e faces devem ser positivas.")

            total += sinal * quantidade * media_dado(faces)

        else:
            try:
                total += sinal * float(parte)
            except ValueError as erro:
                raise ValueError(
                    f"Termo inválido: {termo}. Use dados como 1d8 ou bônus como +4."
                ) from erro

    return total


def formatar_numero(valor: float) -> str:
    """Evita mostrar casas decimais desnecessárias."""
    return f"{valor:.2f}".rstrip("0").rstrip(".")


def main() -> None:
    print("=== Calculadora de Dano T20 ===")
    print("Exemplo: 1d8+4+1d6")
    print("Digite 'sair' para encerrar.\n")

    while True:
        expressao = input("Expressão de dano: ").strip()

        if expressao.lower() in {"sair", "exit", "q"}:
            print("Até a próxima!")
            break

        try:
            resultado = calcular_dano_medio(expressao)
            print(f"Dano médio: {formatar_numero(resultado)} pontos\n")
        except ValueError as erro:
            print(f"Erro: {erro}\n")


if __name__ == "__main__":
    main()

