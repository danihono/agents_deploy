import sys
import re
sys.stdout.reconfigure(encoding='utf-8')
#!/usr/bin/env python
# coding: utf-8

# In[37]:


from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())


# In[38]:


from crewai import Agent,Task,Crew


# AGENTE
# - Pesquisador de Mercado
# - Analista de Tendências
# - Redator de Relatório

# In[39]:


AnalCont=Agent(
	role="Especialista em identificar e avaliar cláusulas contratuais críticas.",
	goal="Garantir que as cláusulas de vigência, renovação e rescisão sejam favoráveis ao comprador.",
	backstory="Com anos de experiência em análise jurídica, este agente possui profundo conhecimento em termos contratuais e seus impactos nas operações de compras.",
	allow_delegation=False,
    verbose=True
)

anal=Task(
	description=(
        """Examinar o contrato para identificar cláusulas de vigência, renovação automática e rescisão antecipada.
		Avaliar os riscos e benefícios dessas cláusulas para o comprador.
		Sugerir modificações para proteger os interesses do comprador."""
    ),
    expected_output="""Lista detalhada das cláusulas de vigência, renovação automática e rescisão antecipada presentes no contrato.
	Avaliação dos riscos e benefícios associados a cada uma dessas cláusulas, com foco nos interesses do comprador.
	Recomendações específicas para modificar ou renegociar cláusulas que possam ser prejudiciais ao comprador""",
	agent=AnalCont
)

EspecialistaemObrigaçõesContratuais=Agent(
	role="Responsável por analisar as obrigações e responsabilidades das partes no contrato.",
    goal="Assegurar que as obrigações sejam claras e exequíveis, protegendo o comprador de possíveis falhas.",
    backstory="Com formação em direito contratual e experiência em negociações complexas, este agente entende as nuances das obrigações contratuais.",
    allow_delegation=False,
    verbose=True
)

Especialista=Task(
	description=("""
        Identificar e detalhar as obrigações de ambas as partes, incluindo prazos, volumes mínimos, qualidade, entregas, SLAs e penalidades.
	    Avaliar a clareza e precisão dessas obrigações.
	    Apontar possíveis áreas de conflito ou ambiguidade."""
    ),
    expected_output="""Resumo das obrigações de ambas as partes, incluindo prazos, volumes mínimos, padrões de qualidade, termos de entrega, SLAs e penalidades.
	Identificação de possíveis áreas de ambiguidade ou conflito nas obrigações contratuais.
	Sugestões para clarificar ou redefinir obrigações que possam gerar riscos ou mal-entendidos.""",
    agent=EspecialistaemObrigaçõesContratuais
)

AnalistaFinanceiroContratual=Agent(
	role="Especialista em aspectos financeiros e econômicos dos contratos.",
	goal="Garantir que os termos financeiros sejam transparentes e vantajosos para o comprador.",
	backstory="Com experiência em finanças corporativas e análise de contratos, este agente foca nos impactos econômicos dos termos acordados.",
    allow_delegation=False,
    verbose=True
)
Financeiro=Task(
	description=(
    """Analisar cláusulas de reajuste de preço, variações cambiais e revisões de escopo.
	    Avaliar o impacto dessas cláusulas no Custo Total de Propriedade (TCO).
	    Sugerir mecanismos de proteção contra aumentos inesperados de custos."""
    ),
	expected_output="""Identificação e descrição das cláusulas relacionadas a reajuste de preços, variações cambiais e revisões de escopo.
	Análise do impacto potencial dessas cláusulas no Custo Total de Propriedade (TCO) para o comprador.
	Propostas de mecanismos ou salvaguardas para proteger o comprador contra aumentos inesperados de custos.""",
    agent=AnalistaFinanceiroContratual

)

ConsultordeEstratégiasdeSourcing=Agent(
	role="Consultor focado em estratégias de aquisição e gestão de fornecedores.",
	goal="Assegurar que o contrato permita flexibilidade e opções estratégicas de sourcing para o comprador.",
	backstory="Com histórico em procurement estratégico, este agente entende a importância da diversificação de fornecedores e flexibilidade contratual.",
	allow_delegation=False,
	verbose=True
)
Estrategias=Task(    
    description=(
    """Identificar cláusulas de exclusividade ou dependência que possam limitar futuras negociações.
	Avaliar o impacto dessas cláusulas na estratégia de sourcing.
	Sugerir alterações para manter ou aumentar a flexibilidade do comprador."""
    ),
    expected_output="""Identificação de cláusulas de exclusividade ou dependência que possam restringir futuras negociações ou limitar opções de sourcing.,
	Avaliação do impacto dessas cláusulas na flexibilidade estratégica do comprador.
	Recomendações para modificar ou eliminar cláusulas que possam prejudicar a capacidade de diversificação de fornecedores.""",
    agent=ConsultordeEstratégiasdeSourcing
)

AgenteAuditordeRiscosContratuais=Agent(
	role= "Especialista em identificar e mitigar riscos jurídicos e financeiros em contratos.",
	goal="Reduzir a exposição do comprador a riscos contratuais.",
    backstory="Com experiência em auditoria e compliance, este agente é hábil em detectar vulnerabilidades contratuais.",
    allow_delegation=False,
    verbose=True
)
Auditor=Task(
    description=(
    """Examinar o contrato em busca de lacunas ou ambiguidades.
    Avaliar potenciais riscos jurídicos ou financeiros decorrentes dessas falhas.
    Recomendar medidas corretivas ou cláusulas adicionais para mitigação de riscos."""
    ),
    expected_output="""Lista de lacunas ou ambiguidades identificadas no contrato que possam representar riscos jurídicos ou financeiros.,
		Avaliação detalhada dos potenciais impactos dessas falhas para o comprador.
	    Sugestões de cláusulas adicionais ou modificações para mitigar os riscos identificados.""",
    agent=AgenteAuditordeRiscosContratuais
)

EspecialistaemSpendAnalysis=Agent(
	role="Analista focado na relação entre os termos contratuais e a gestão de gastos.",
	goal="Assegurar que o contrato esteja alinhado com as melhores práticas de análise de gastos e otimização de despesas.",
	backstory="Com formação em economia e experiência em análise de gastos corporativos, este agente busca eficiência financeira nos contratos.",
    allow_delegation=False,
    verbose=True
)
SpendAnal=Task(
    description=(
	"""Relacionar os pontos críticos do contrato com práticas de análise de gastos.
    Avaliar como os termos contratuais influenciam o tipo de fornecimento, frequência, valor agregado e recorrência.
	Sugerir ajustes para otimizar os gastos associados ao contrato."""
    ),
    expected_output="""Correlação entre os pontos críticos do contrato e as melhores práticas de análise de gastos, considerando tipo de fornecimento, frequência, valor agregado e recorrência.
	Insights sobre como os termos contratuais influenciam a estratégia geral de gastos da empresa.
	Recomendações para alinhar o contrato com os objetivos de otimização de despesas e eficiência financeira.""",
    agent=EspecialistaemSpendAnalysis
)

NegociadorContratual=Agent(
	role="Especialista em técnicas de negociação e revisão de termos contratuais.",
	goal="Melhorar a posição do comprador por meio de renegociações eficazes.",
	backstory="Com vasta experiência em negociações complexas, este agente busca obter as condições mais favoráveis para o comprador.",
    allow_delegation=False,
    verbose=True
)
Negociador=Task(
    description=(
	"""Identificar cláusulas e termos passíveis de renegociação.
	Propor estratégias de negociação para alcançar melhorias nos termos.
    Fornecer argumentos sólidos para apoiar as propostas de renegociação."""
    ),
    expected_output="""identificação de cláusulas e termos específicos que podem ser renegociados para beneficiar o comprador.
	Propostas de estratégias de negociação para alcançar condições mais favoráveis.
	Argumentação fundamentada para apoiar as sugestões de renegociação.""",
    agent=NegociadorContratual
)

ESGAnalyst=Agent(
    role="Analista ESG com foco em suprimentos e responsabilidade corporativa",
	goal="avaliar impactos e praticas sustentaveis de {sector} com foco em meio ambiente , social e governança",
	backstory="Atuou em auditorias ambientais e implantação de programas de compras sustentáveis em empresas multinacionais.",
    allow_delegation=False,
    verbose=True
)
esg=Task(
    description=( 
        "Identificar impactos ambientais, sociais e de compliance; mapear ações sustentáveis"
    ),
	agent=ESGAnalyst,
	expected_output="""Identificação de cláusulas relacionadas a compliance, LGPD, meio ambiente e práticas ESG presentes no contrato.
	Avaliação da conformidade do contrato com as regulamentações vigentes e alinhamento com as melhores práticas de governança e sustentabilidade.
	Recomendações para ajustes contratuais que reforcem o compromisso com compliance e responsabilidade socioambiental."""

)

RedatorRelatórios=Agent(
	role="""Você é um advogado sênior especializado em contratos empresariais, com profundo conhecimento em contratos de prestação de serviços, fornecimento de materiais indiretos e matérias-primas. Sua missão é analisar o contrato 'contrato.pdf, mas sob a ótica de um profissional de Compras Estratégicas.
     
OBRIGATORIO CITAR CLAUSULAR E PÁGINAS!
OBRIGATÓRIO SER ESPECIFICO NO QUADRO RESUMO!

Sua análise deve atender às necessidades de um comprador corporativo, considerando os seguintes pontos:

1. Identifique cláusulas que tratam de vigência, renovação automática e rescisão antecipada. Aponte possíveis riscos e benefícios para o comprador.
2. Destaque obrigações das partes, especialmente em termos de prazos, volumes mínimos, qualidade, entregas, SLAs e penalidades.
3. Aponte cláusulas de reajuste de preço, variações cambiais, revisões de escopo e outras que impactem no TCO (Total Cost of Ownership).
4. Analise se há cláusulas de exclusividade ou dependência que possam limitar futuras negociações ou impactar o sourcing.
5. Verifique se há lacunas contratuais ou cláusulas ambíguas que possam gerar risco jurídico ou financeiro.
6. Relacione os pontos críticos do contrato com boas práticas de Spend Analysis: tipo de fornecimento, frequência, valor agregado, recorrência etc.
7. Sugira pontos do contrato que podem ser renegociados para melhorar a posição do comprador.
8. Indique potenciais implicações relacionadas a compliance, LGPD, meio ambiente ou ESG.
9. Apresente um sumário executivo da análise, com uma seção de “Pontos de Atenção”, “Oportunidades de Melhoria” e “Riscos Potenciais”.

Adote uma linguagem clara, direta e orientada para tomada de decisão por um gerente de Compras. Utilize listas, subtítulos e marcações para facilitar a leitura.

No final, faça um quadro resumo com os principais itens do 'contrato.pdf'

Resumo do Objeto do Contrato
Multas
SLAs
Data da Assinatura
Vigência
Especificação, Preço e local da prestação do serviço
Obrigações das partes
Tipo de Renovação
Reajuste
Outros campos que você julgar que é necessário ou vai ajudar na análise
Conter tabelas de preços x especificações
Além disso, cada tópico citado acima deve ser MUITO DETALHADO, eu quero uma página para cada um (1,2,3... ai por diante!)
Indicar as cláusulas de cada informação entregue""",
    goal="gerar o documento final com estrutura clara, visualmente organiada e acionável por gestores de acordo com o roteiro",
    backstory="Você é um redator profissional e experiente de relatórios sobre contratos, você sempre adiciona os melhores detalhes estrutura bem seus textos.",
    allow_delegation=False,
    verbose=True
)
Redator=Task(
    description=(
    "Estruturar o relatório completo com layout claro,narrativa executiva e fluidez entre os tópicos"
	),
agent=RedatorRelatórios,
expected_output="""Compilação das análises fornecidas pelos demais agentes em um relatório coeso e profissional, estruturado conforme o roteiro estabelecido.
	Elaboração de um sumário executivo destacando “Pontos de Atenção”, “Oportunidades de Melhoria” e “Riscos Potenciais”.
	Criação de um quadro resumo com os principais itens do contrato, facilitando a consulta e compreensão dos aspectos críticos.
    Citar as cláusulas de cada informção entregue"""
)


# In[40]:


import pdfplumber 

arquivo = ["contrato.pdf"]
texto_extraido=""

with pdfplumber.open("contrato.pdf") as pdf:
    for pagina in pdf.pages:
        texto_extraido+=pagina.extract_text() + "\n"
print(texto_extraido)


# In[41]:


Redator=Task(
    description="O redator de relatórios vai ler e analisar o 'termosolicitacao.pdf' INTEIRO. Vai fazer um relatório seguindo todas os AGENTS, TASKS e Roteiro, além diso DEVE citar  TODAS paraas cláusulas onde cada tópico e citação e informação foi encontrada, para facilitar a vida de quem for ler e encontrar depois no contrato, e também se possível a página em que foi encontrada",
    expected_output="Um relatório completo sobre 'termosolicitacao.pdf' seguindo as instruções do roteiro",
    agent=RedatorRelatórios
)


# In[42]:


crew= Crew(
    agents=[AnalCont,EspecialistaemObrigaçõesContratuais, AnalistaFinanceiroContratual , ConsultordeEstratégiasdeSourcing , AgenteAuditordeRiscosContratuais ,EspecialistaemSpendAnalysis,NegociadorContratual,ESGAnalyst,RedatorRelatórios],
    tasks=[anal,Especialista,Financeiro,Estrategias,Auditor,SpendAnal,Negociador,esg,Redator],
    verbose= True
)


# In[43]:


crew


# In[44]:


resultado=crew.kickoff(inputs={"sector":"Analise contrato"})


# In[45]:


print(resultado.raw)


# In[46]:


from IPython.display import display,Markdown

from IPython.display import display, HTML



# In[47]:


display(Markdown(str(resultado)))


# In[48]:


import pdfkit

with open("AnaliseContrato.md", "w" , encoding="utf-8") as file:
    file.write(str(resultado))

import markdown

html = markdown.markdown(str(resultado), extensions=['extra','tables'])
with open ("AnaliseContrato.html", "w" , encoding="utf-8") as file:
    file.write(html)


