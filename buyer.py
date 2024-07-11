import pandas as pd
class BuyerModule:
    def __init__(self,df):
        self.df = df

    def get_buyer_stats(self,buyer_name):
        buyer_data = self.df[self.df['Buyer'] == buyer_name]
        total_payment_volume = buyer_data['Payment Volume'].sum()

        overall_buyer_volume = self.df.groupby('Buyer')['Payment Volume'].sum()
        overall_buyer_rank = overall_buyer_volume.rank(ascending=False, method='min').to_dict()
        overall_position = overall_buyer_rank.get(buyer_name, 'N/A')

        issuer_name = buyer_data['Issuer'].iloc[0] if not buyer_data.empty else 'N/A'
        issuer_data = self.df[self.df['Issuer'] == issuer_name]
        issuer_buyer_volume = issuer_data.groupby('Buyer')['Payment Volume'].sum()
        issuer_buyer_rank = issuer_buyer_volume.rank(ascending=False, method='min').to_dict()
        issuer_position = issuer_buyer_rank.get(buyer_name, 'N/A')

        buyer_industry = buyer_data['Buyer Industry'].unique()
        buyer_industry = buyer_industry[0] if len(buyer_industry) == 1 else 'Multiple Industries'

        if buyer_industry != 'Multiple Industries':
            industry_data = self.df[self.df['Buyer Industry'] == buyer_industry]
            top_5_buyers_in_industry = industry_data.groupby('Buyer')['Payment Volume'].sum().nlargest(5).to_dict()
        else:
            top_5_buyers_in_industry = {}

        supplier_data = buyer_data.groupby(['Supplier', 'Supplier Industry'])['Payment Volume'].sum().reset_index()
        suppliers_info = supplier_data.to_dict('records')

        buyer_stats = {
            'total_payment_volume': total_payment_volume,
            'overall_position': int(overall_position),
            'issuer_name': issuer_name,
            'issuer_position': int(issuer_position),
            'buyer_industry': buyer_industry,
            'top_5_buyers_in_industry': top_5_buyers_in_industry,
            'suppliers_info': suppliers_info,
        }
        return buyer_stats

# df = pd.read_excel('Input.xlsx')
# buyer_module = BuyerModule(df)
# buyer_name = 'Timberland Group'  # Replace with the actual buyer name
# buyer_stats = buyer_module.get_buyer_stats(buyer_name)
#
# print(buyer_stats)
