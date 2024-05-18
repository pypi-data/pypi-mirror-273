# Imports all the necessary libraries



import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors 
from rdkit.ML.Descriptors import MoleculeDescriptors
from tqdm import tqdm
from lightgbm import LGBMRegressor
import pickle


#============================================================================================================================================



def help():
    print_help= """
    This package contains 2 main functions:  predict_logS_smiles and predict_logS_csv
    
    ==========================================================================================================================================
    
    predict_logS_smiles(smiles_code)
    
    Description: Predicts the LogS value for one or more  SMILES.
    Usage: Provide one or more valid SMILES codes in a string as input
    Example: predict_logS_smiles("CC(=O)NC1=CC=C(C=C1)O","CN1C=NC2=C1C(=O)N(C(=O)N2C)C")
    
    ==========================================================================================================================================
    
    print("predict_logS_csv(csv_file_path):
    
    Description: Predicts LogS values for SMILES codes stored in a CSV file
    Usage: Provide the path to a CSV file containing SMILES codes in the 'SMILE' column (see Template.csv for an example of a valid csv file)
    Example: predict_logS_csv("/content/WSPP_Projectppchem/src/WSPP/Template.csv")

    ==========================================================================================================================================
    """
    print(print_help)



def print_space():
    """
    Description: Makes space for readability.
    """
    space =  """

    """
    print(space)



def print_ascii_art():
    """
    Description: print("Thank for using SWPP!) which stand for Solubility Water Prediction Project.
    """
    ascii_art = """
=================================================================================================================================================
=                                                                                                                                               =
=    _______ _                 _                             __                        _               __          _______ _____  _____    _    =
=   |__   __| |               | |                           / _|                      (_)              \ \        / / ____|  __ \|  __ \  | |   =
=      | |  | |__   __ _ _ __ | | __   _   _  ___  _   _   | |_ ___  _ __    _   _ ___ _ _ __   __ _    \ \  /\  / / (___ | |__) | |__) | | |   =
=      | |  | '_ \ / _` | '_ \| |/ /  | | | |/ _ \| | | |  |  _/ _ \| '__|  | | | / __| | '_ \ / _` |    \ \/  \/ / \___ \|  ___/|  ___/  | |   =
=      | |  | | | | (_| | | | |   <   | |_| | (_) | |_| |  | || (_) | |     | |_| \__ \ | | | | (_| |     \  /\  /  ____) | |    | |      |_|   =
=      |_|  |_| |_|\__,_|_| |_|_|\_\   \__, |\___/ \__,_|  |_| \___/|_|      \__,_|___/_|_| |_|\__, |      \/  \/  |_____/|_|    |_|      (_)   =
=                                     __/ |                                                   __/ |                                             =          
=                                    |___/                                                   |___/                                              =
=================================================================================================================================================                  
    """
    print(ascii_art)



def canonical_SMILES(smiles):
    """
    Generates canonical SMILES representations for a list of SMILES codes.

    Parameters:
    smiles (list): A list of SMILES codes.

    Returns:
    A list of canonical SMILES representations corresponding to the input SMILES codes.
    """
    
    canon_smiles = [Chem.CanonSmiles(smls) for smls in smiles]
    return canon_smiles



def RDkit_descriptors(smiles):
    """
    Calculates RDKit descriptors for a list of SMILES codes.

    Parameters:
    smiles (list): A list of SMILES codes.

    Returns:
    A tuple containing two lists:
        - Mol_descriptors: List of descriptor values for each molecule corresponding to the input SMILES codes.
        - desc_names: List of descriptor names.
    """
    
    mols = [Chem.MolFromSmiles(i) for i in smiles]
    calc = MoleculeDescriptors.MolecularDescriptorCalculator([x[0] for x in Descriptors._descList])
    desc_names = calc.GetDescriptorNames()

    Mol_descriptors = []
    for mol in tqdm(mols):
        mol = Chem.AddHs(mol)
        descriptors = calc.CalcDescriptors(mol)
        Mol_descriptors.append(descriptors)
    return Mol_descriptors, desc_names



def load_model_and_scalers(model_path=None, scaler_path=None):
    """
    Loads a trained model and scalers from specified paths.

    Parameters:
    model_path (str, optional): Path to the trained model file (default is None).
    scaler_path (str, optional): Path to the scaler file (default is None).

    Returns:
    A tuple containing the loaded model and scaler objects.
    """
    
    model_full_path = "/content/WSPP_Projectppchem/Data/LGBMRegressor/model_LGBM.pkl"  # Provide the path to the model file
    scaler_full_path = "/content/WSPP_Projectppchem/Data/LGBMRegressor/scaler_LGBM.pkl"  # Provide the path to the scaler file
    
    if model_path:
        model_full_path = model_path
    if scaler_path:
        scaler_full_path = scaler_path

    with open(model_full_path, 'rb') as model_file:
        model = pickle.load(model_file)

    with open(scaler_full_path, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)

    return model, scaler



def predict_LogS(smiles):
    """
    Predicts LogS values for a given SMILES code using a trained model.

    Parameters:
    smiles (str): A valid SMILES code for a chemical compound.

    Returns:
    Predicted LogS value for the input SMILES code.
    """
    
    canonical_smiles = canonical_SMILES([smiles])
    descriptors, _ = RDkit_descriptors(canonical_smiles)

    model, scaler = load_model_and_scalers()
    scaled_descriptors = scaler.transform(descriptors)

    logS_prediction = model.predict(scaled_descriptors)
    return logS_prediction[0]

#==========================================================================================================================================

# Prediction functions

def predict_logS_smiles(*smiles_codes):
    """
    Predicts LogS values for a list of SMILES codes using a trained model.

    Parameters:
    *smiles_codes (str): Variable-length argument list of SMILES codes.

    Returns:
    The predicted logS value for each valid SMILES code.
    """
    
    logS_values = {}  # Dictionary to store LogS values for each SMILES code

    for smiles_code in smiles_codes:
        if not Chem.MolFromSmiles(smiles_code):
            print(f"Invalid SMILES code: {smiles_code}. Skipping.")
        else:
            try:
                float(smiles_code)  # Check if input is a float
                print(f"Invalid input: {smiles_code}. Skipping.")
            except ValueError:
                logS = predict_LogS(smiles_code)
                logS_values[smiles_code] = logS  # Store LogS value in dictionary
                print(f"Predicted LogS value for {smiles_code}: {logS} mol/L")

    # Print LogS values after processing all input SMILES codes
    print_space()
    print("\nLogS Values:")
    for smiles_code, logS in logS_values.items():
        print(f"The predicted logS value for {smiles_code} is: {logS} mol/L")
    print_ascii_art()



def predict_logS_csv(csv_file_path):
    """
    Predicts LogS values for SMILES codes stored in a CSV file and saves the predictions to a new CSV file.

    Parameters:
    csv_file_path (str): Path to the CSV file containing SMILES codes in the 'SMILE' column.

    Returns:
    A new CSV file named with '_predicted.csv' at the end containing the SMILES code and thei predicted LogS values.
    """
 
    # Read the CSV file into a DataFrame
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"File {csv_file_path} not found.")
        return

    # Check if the required columns are present
    if "SMILE" not in df.columns:
        print("CSV file must have 'SMILE' in the first column, check that your file matches the template")
        return

    # Iterate over each row and predict LogS value
    logS_predictions = []
    for index, row in df.iterrows():
        smiles = row['SMILE']
        logS_prediction = predict_LogS(smiles)
        logS_predictions.append(logS_prediction)

    # Add the predicted LogS values to the DataFrame
    df['Predicted_LogS mol/L'] = logS_predictions

    # Save the DataFrame with predicted LogS values to a new CSV file
    output_csv_file = csv_file_path.replace('.csv', '_predicted.csv')
    df.to_csv(output_csv_file, index=False)
    print_space()
    print(f"Predicted LogS values saved to: {output_csv_file}")
    print_ascii_art()
