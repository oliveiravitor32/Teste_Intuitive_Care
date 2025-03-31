import type { IOperator } from '@/interfaces/operator.interface'

// Type definition for field definition object
export interface IOperatorField {
  key: keyof IOperator
  label: string
  formatter: (value: string | undefined) => string
}

export const capitalizeText = (text: string | null | undefined): string => {
  if (!text) return '-'
  return text[0] + text.substring(1).toLowerCase()
}

const truncateAndCapitalizeTText = (text: string | null | undefined, maxLength = 35): string => {
  if (!text) return '-'
  return text.toLowerCase().length > maxLength
    ? text[0] + text.substring(1, maxLength).toLowerCase().trim() + '...'
    : text[0] + text.substring(1).toLowerCase().trim()
}

export const formatDate = (text: string | null | undefined): string => {
  if (!text) return '-'
  const date = new Date(text)
  return date.toLocaleDateString('pt-BR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}

// Operator field definitions
export const operatorFieldDefinitions: IOperatorField[] = [
  { key: 'registro_ans', label: 'Registro ANS', formatter: capitalizeText },
  { key: 'cnpj', label: 'CNPJ', formatter: capitalizeText },
  { key: 'razao_social', label: 'Razão Social', formatter: capitalizeText },
  { key: 'nome_fantasia', label: 'Nome Fantasia', formatter: capitalizeText },
  { key: 'modalidade', label: 'Modalidade', formatter: capitalizeText },
  { key: 'logradouro', label: 'Logradouro', formatter: capitalizeText },
  { key: 'numero', label: 'Número', formatter: capitalizeText },
  { key: 'complemento', label: 'Complemento', formatter: capitalizeText },
  { key: 'bairro', label: 'Bairro', formatter: capitalizeText },
  { key: 'cidade', label: 'Cidade', formatter: capitalizeText },
  { key: 'uf', label: 'UF', formatter: capitalizeText },
  { key: 'cep', label: 'CEP', formatter: capitalizeText },
  { key: 'ddd', label: 'DDD', formatter: capitalizeText },
  { key: 'telefone', label: 'Telefone', formatter: capitalizeText },
  { key: 'fax', label: 'Fax', formatter: capitalizeText },
  { key: 'endereco_eletronico', label: 'Endereço Eletrônico', formatter: capitalizeText },
  { key: 'representante', label: 'Representante', formatter: capitalizeText },
  { key: 'cargo_representante', label: 'Cargo do Representante', formatter: capitalizeText },
  {
    key: 'regiao_de_comercializacao',
    label: 'Região de Comercialização',
    formatter: capitalizeText,
  },
  { key: 'data_registro_ans', label: 'Data de Registro ANS', formatter: formatDate },
]

// Operator field definitions for shortened view
export const operatorFieldDefinitionsShortened: IOperatorField[] = [
  { key: 'registro_ans', label: 'Registro ANS', formatter: truncateAndCapitalizeTText },
  { key: 'razao_social', label: 'Razão Social', formatter: truncateAndCapitalizeTText },
  { key: 'modalidade', label: 'Modalidade', formatter: truncateAndCapitalizeTText },
  { key: 'cidade', label: 'Cidade', formatter: truncateAndCapitalizeTText },
  { key: 'data_registro_ans', label: 'Data de Registro ANS', formatter: formatDate },
]
