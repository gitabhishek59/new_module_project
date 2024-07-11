class IssuerModule:
    def __init__(self, df):
        self.df = df

    def get_ordinal_suffix(self, n):
        """Return the ordinal suffix for a given number."""
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"

    def get_issuer_stats(self, issuer_name, top_n):
        issuer_data = self.df[self.df['Issuer'] == issuer_name]

        issuer_payment_volume = issuer_data['Payment Volume'].sum()

        issuer_totals = self.df.groupby('Issuer')['Payment Volume'].sum()
        sorted_totals = issuer_totals.sort_values(ascending=False)
        try:
            issuer_position = list(sorted_totals.index).index(issuer_name) + 1  # +1 for 1-based index
            issuer_position = self.get_ordinal_suffix(issuer_position)
        except ValueError:
            issuer_position = None

        issuer_stats = {
            'issuer_position': issuer_position,
            'issuer_payment_volume': issuer_payment_volume,
            'number_of_buyers': issuer_data['Buyer'].nunique(),
            'number_of_suppliers': issuer_data['Supplier'].nunique(),
            'top_buyer_industry': issuer_data.groupby('Buyer Industry')['Payment Volume'].sum().nlargest(
                top_n).to_dict(),
            'top_buyers': issuer_data.groupby('Buyer')['Payment Volume'].sum().nlargest(top_n).to_dict(),
            'bottom_buyers': issuer_data.groupby('Buyer')['Payment Volume'].sum().nsmallest(top_n).to_dict(),
            'top_supplier_industry': issuer_data.groupby('Supplier Industry')['Payment Volume'].sum().nlargest(
                top_n).to_dict(),
            'top_suppliers': issuer_data.groupby('Supplier')['Payment Volume'].sum().nlargest(top_n).to_dict(),
            'bottom_suppliers': issuer_data.groupby('Supplier')['Payment Volume'].sum().nsmallest(top_n).to_dict(),
        }

        return issuer_stats
