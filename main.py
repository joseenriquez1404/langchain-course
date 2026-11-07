import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def main():
    print("Hello from section-3!")
    information = """
    Elon Reeve Musk (/ˈiːlɒn mʌsk/ Pretoria, 28 de junio de 1971) es un empresario, inversor, activista político conservador[3][4] y magnate sudafricano naturalizado estadounidense.[nota 1] Es el fundador, consejero delegado e «ingeniero» en jefe de la empresa SpaceX; inversor ángel, director general y arquitecto de productos de Tesla, Inc.; fundador de The Boring Company; y cofundador de Neuralink y OpenAI.[nota 2] Además, es el director de tecnología de X Corp.[5] Entre enero y mayo de 2025, ejerció como administrador de facto del Departamento de Eficiencia Gubernamental de la Casa Blanca bajo la segunda presidencia de Donald Trump.[6][7]A junio de 2026, Musk es la persona más rica del mundo según Forbes. Tras la salida a bolsa de SpaceX, su patrimonio neto superó los 1,1 billones de dólares estadounidenses, convirtiéndolo en el único y primer billlonario en términos de dólares estadounidenses de la historia.[8] El 16 de junio de 2026, su patrimonio alcanzaría un récord máximo de 1,4 billones de dólares.[9]

    Musk nació y se crió en una rica familia de Pretoria (Sudáfrica). Su madre es canadiense y su padre un sudafricano blanco. Estudió brevemente en la Universidad de Pretoria antes de trasladarse a Canadá a los 17 años. Se matriculó en la Universidad de Queen y se trasladó a la Universidad de Pensilvania dos años después, donde se graduó en Economía y Física. En 1995 se trasladó a California para asistir a la Universidad Stanford, pero en su lugar decidió seguir una carrera empresarial, cofundando la empresa de software web Zip2 con su hermano Kimbal. Zip2 fue adquirida por Compaq por 307 millones de dólares en 1999. Ese mismo año, Musk cofundó el banco en línea X.com, que se fusionó con Confinity en 2000 para formar PayPal. La empresa fue comprada por eBay en 2002 por mil quinientos millones de dólares.
    """

    summary_template = """
    given the information {information} about a person I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
    )

    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)

    chain = summary_prompt_template | llm
    response = chain.invoke(input={"information": information})

    print(response.content)


if __name__ == "__main__":
    main()
