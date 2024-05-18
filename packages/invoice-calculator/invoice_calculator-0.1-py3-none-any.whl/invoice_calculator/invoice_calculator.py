# invoice_calculator.py

def calculate_invoice(HT):
    """
    Calculate the invoice details given the total price HT.
    
    Parameters:
    HT (float): The total price before tax.

    Returns:
    dict: A dictionary containing the HT, reduction, HT after reduction, TVA, and TTC.
    """
    # Calculations
    red = 0.15 * HT if HT > 200 else 0
    htred = HT - red
    tva = 0.2 * htred
    ttc = htred + tva

    # Return results in a dictionary
    return {
        "Prix total HT": HT,
        "Réduction": red,
        "Montant HT après réduction": htred,
        "TVA": tva,
        "Montant TTC": ttc
    }

# Example usage
if __name__ == "__main__":
    HT = float(input("Entrez le prix total HT : "))
    invoice_details = calculate_invoice(HT)
    for key, value in invoice_details.items():
        print(f"{key} : {value:.2f} DH")
