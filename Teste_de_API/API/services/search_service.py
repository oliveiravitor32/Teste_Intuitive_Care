import pandas as pd
from typing import List

from config import settings
from models.operator import Operator
from models.operators_response import OperatorsResponse
from models.search_params import SearchParams


class SearchService:
    def __init__(self):
        self.df = None
        self._load_data()

    def _load_data(self) -> None:
        """Load healthcare operators data from CSV"""
        try:

            print("Load data")
            self.df = pd.read_csv(
                settings.OPERADORAS_CSV,
                encoding='utf-8',
                dtype=str,  # Load all columns as strings initially
                delimiter= ';',
                low_memory=False,
                quoting=1
            )
            # Clean column names (remove spaces, lowercase)
            self.df.columns = [col.strip().lower().replace(' ', '_') for col in self.df.columns]

            # Clean data
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    self.df[col] = self.df[col].str.strip()

            print(f"Loaded {len(self.df)} operators from CSV")
        except Exception as e:
            print(f"Error loading CSV data: {e}")
            # Initialize with empty DataFrame if file not found
            self.df = pd.DataFrame()

    def search_operadoras(self, params: SearchParams) -> OperatorsResponse:
        """
        Search healthcare operators based on search parameters
        Returns the most relevant results
        """
        print("Query to search data: ", params.query)
        if self.df.empty:
            return []

        query = params.query.lower()

        # Create mask based on selected fields
        mask = pd.Series(False, index=self.df.index)

        if params.category  ==  "razao_social":
            razao_mask = self.df['razao_social'].str.lower().str.contains(query, na=False)
            mask = mask | razao_mask

        if params.category == "nome_fantasia":
            nome_mask = self.df['nome_fantasia'].str.lower().str.contains(query, na=False)
            mask = mask | nome_mask

        if params.category == "modalidade":
            nome_mask = self.df['modalidade'].str.lower().str.contains(query, na=False)
            mask = mask | nome_mask

        results = self.df[mask]

        # Limit results and convert to response model
        results = results.head(params.limit)

        return OperatorsResponse(
            data = [Operator(
                registro_ans=self._handle_nan(row.get('registro_ans', '')),
                cnpj=self._handle_nan(row.get('cnpj', '')),
                razao_social=self._handle_nan(row.get('razao_social', '')),
                nome_fantasia=self._handle_nan(row.get('nome_fantasia', '')),
                modalidade=self._handle_nan(row.get('modalidade', '')),
                logradouro=self._handle_nan(row.get('logradouro', '')),
                numero=self._handle_nan(row.get('numero', '')),
                complemento=self._handle_nan(row.get('complemento', '')),
                bairro=self._handle_nan(row.get('bairro', '')),
                cidade=self._handle_nan(row.get('cidade', '')),
                uf=self._handle_nan(row.get('uf', '')),
                cep=self._handle_nan(row.get('cep', '')),
                ddd=self._handle_nan(row.get('ddd', '')),
                telefone=self._handle_nan(row.get('telefone', '')),
                fax=self._handle_nan(row.get('fax', '')),
                endereco_eletronico=self._handle_nan(row.get('endereco_eletronico', '')),
                representante=self._handle_nan(row.get('representante', '')),
                cargo_representante=self._handle_nan(row.get('cargo_representante', '')),
                regiao_de_comercializacao=self._handle_nan(row.get('regiao_de_comercializacao', '')),
                data_registro_ans=self._handle_nan(row.get('data_registro_ans', ''))
            )
            for _, row in results.iterrows()
        ])

    def _handle_nan(self, value):
        """Convert NaN values to empty strings"""
        if pd.isna(value):
            return ""
        return value
